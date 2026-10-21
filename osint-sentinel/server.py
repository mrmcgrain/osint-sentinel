#!/usr/bin/env python3
import csv, base64, datetime, html, json, os, pathlib, re, secrets, shutil, subprocess, threading, time, urllib.parse, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path.home()/"osint-sentinel"
DATA=ROOT/'data'; FILES=DATA/'images'; CASES=DATA/'cases'; JOBS={}; LOCK=threading.Lock()
for d in (FILES,CASES):d.mkdir(parents=True,exist_ok=True)
TOKEN=secrets.token_urlsafe(24)
TOOLS={'sherlock':{'label':'Sherlock','pkg':'sherlock-project','bin':'sherlock'},'maigret':{'label':'Maigret','pkg':'maigret','bin':'maigret'}}
MAX_IMAGE=8*1024*1024

def safe_username(s):
    s=s.strip().lstrip('@')
    if not re.fullmatch(r'[A-Za-z0-9_.-]{2,64}',s):raise ValueError('Use 2–64 username characters: letters, numbers, _ . -')
    return s

def sherlock_summary(report):
    counts={'checked':0,'found':0,'not_found':0,'errors':0,'skipped':0}
    with open(report, newline='', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            status=row['exists']
            if status=='Illegal':counts['skipped']+=1
            else:
                counts['checked']+=1
                key={'Claimed':'found','Available':'not_found'}.get(status,'errors')
                counts[key]+=1
    return counts

def job(kind,name,args,report=None):
    jid=uuid.uuid4().hex[:12]
    with LOCK:JOBS[jid]={'id':jid,'kind':kind,'name':name,'status':'queued','output':'','created':datetime.datetime.now().isoformat(timespec='seconds')}
    def worker():
        with LOCK:JOBS[jid]['status']='running'
        try:
            p=subprocess.run(args, cwd=str(DATA),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600,env={**os.environ,'PATH':str(pathlib.Path.home()/'.local/bin')+':'+os.environ.get('PATH','')})
            out=p.stdout[-100000:]
            summary=None
            if report and pathlib.Path(report).exists():summary=sherlock_summary(report)
            with LOCK:JOBS[jid]['summary']=summary
            with LOCK:JOBS[jid].update(status='done' if p.returncode==0 else 'error',output=out,exit_code=p.returncode)
        except subprocess.TimeoutExpired as e:
            partial=e.stdout or ''
            if isinstance(partial,bytes):partial=partial.decode('utf-8',errors='replace')
            with LOCK:JOBS[jid].update(status='error',output=partial[-100000:]+'\nSearch timed out after 10 minutes. Results are incomplete.',summary=None)
        except Exception as e:
            with LOCK:JOBS[jid].update(status='error',output=str(e))
    threading.Thread(target=worker,daemon=True).start()
    return jid

class H(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def send(self,obj,code=200):
        b=json.dumps(obj).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def check(self):
        if self.headers.get('X-OSINT-Token')!=TOKEN:return False
        origin=self.headers.get('Origin','')
        return not origin or origin in ('http://127.0.0.1:8765','http://localhost:8765')
    def post_data(self):
        ln=int(self.headers.get('Content-Length',0));
        if ln<=0 or ln>12*1024*1024:raise ValueError('Request size not allowed')
        return json.loads(self.rfile.read(ln))
    def do_GET(self):
        p=urllib.parse.urlparse(self.path).path
        if p=='/healthz':
            b=b'osint-sentinel-ready-v1'
            self.send_response(200);self.send_header('Content-Type','text/plain');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
        if p=='/':
            b=(ROOT/'index.html').read_text().replace('__TOKEN__',TOKEN).encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
        if p.startswith('/images/'):
            fn=p.rsplit('/',1)[-1]
            if not re.fullmatch('[a-f0-9]{32}\\.(png|jpg|webp)',fn):self.send({'error':'Not found'},404);return
            f=FILES/fn
            if not f.exists():self.send({'error':'Not found'},404);return
            b=f.read_bytes();mime='image/png' if fn.endswith('png') else 'image/webp' if fn.endswith('webp') else 'image/jpeg'
            self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
        if p.startswith('/api/') and not self.check():self.send({'error':'Unauthorized'},403);return
        if p=='/api/status':self.send({'tools':{k:bool(shutil.which(v['bin'],path=str(pathlib.Path.home()/'.local/bin')+':'+os.environ.get('PATH',''))) for k,v in TOOLS.items()},'jobs':list(JOBS.values())[-15:]});return
        if p=='/api/cases':
            vals=[]
            for f in sorted(CASES.glob('*.json'),reverse=True):
                try:vals.append(json.loads(f.read_text()))
                except Exception:pass
            self.send({'cases':vals});return
        if p.startswith('/api/case/'):
            cid=p.rsplit('/',1)[-1]
            if not re.fullmatch('[a-f0-9]{32}',cid):self.send({'error':'Not found'},404);return
            f=CASES/(cid+'.json')
            if not f.exists():self.send({'error':'Not found'},404);return
            self.send(json.loads(f.read_text()));return
        if p.startswith('/api/job/'):
            jid=p.rsplit('/',1)[-1];self.send(JOBS.get(jid,{'error':'Not found'}),200 if jid in JOBS else 404);return
        self.send({'error':'Not found'},404)
    def do_POST(self):
        if not self.check():self.send({'error':'Unauthorized'},403);return
        p=urllib.parse.urlparse(self.path).path
        try:
            d=self.post_data()
            if p=='/api/install':
                tool=d.get('tool');action=d.get('action','install')
                if tool not in TOOLS or action not in ('install','upgrade','uninstall'):raise ValueError('Invalid package/action')
                command=['pipx',action,TOOLS[tool]['pkg']]
                self.send({'job':job('package',tool,command)});return
            if p=='/api/run':
                tool=d.get('tool');username=safe_username(d.get('username',''))
                if tool not in TOOLS:raise ValueError('Unknown tool')
                runid=uuid.uuid4().hex[:8]
                report=None
                if tool=='sherlock':
                    folder=DATA/('sherlock-'+runid)
                    folder.mkdir()
                    report=folder/(username+'.csv')
                    cmd=['sherlock',username,'--nsfw','--print-all','--no-color','--csv','--txt','--folderoutput',str(folder)]
                else:cmd=['maigret',username,'--html','--folderoutput',str(DATA/('maigret-'+runid))]
                self.send({'job':job('search',tool,cmd,report)});return
            if p=='/api/upload':
                data=d.get('data','');mime=d.get('mime','');ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}.get(mime)
                if not ext:raise ValueError('Only JPEG, PNG, WebP are supported')
                raw=base64.b64decode(data,validate=True)
                if len(raw)>MAX_IMAGE:raise ValueError('Maximum image size: 8 MB')
                sig={'jpg':raw.startswith(b'\xff\xd8\xff'),'png':raw.startswith(b'\x89PNG\r\n\x1a\n'),'webp':raw.startswith(b'RIFF') and raw[8:12]==b'WEBP'}[ext]
                if not sig:raise ValueError('Image file signature invalid')
                fn=uuid.uuid4().hex+'.'+ext;(FILES/fn).write_bytes(raw);self.send({'image':'/images/'+fn});return
            if p=='/api/case':
                cid=uuid.uuid4().hex;rec={'id':cid,'created':datetime.datetime.now().isoformat(timespec='seconds'),'title':str(d.get('title',''))[:120],'username':str(d.get('username',''))[:120],'notes':str(d.get('notes',''))[:15000],'indicators':d.get('indicators',[])[:20],'image':str(d.get('image',''))[:120]}
                if not rec['title']:raise ValueError('Case title required')
                if not isinstance(rec['indicators'],list) or any(not isinstance(x,str) for x in rec['indicators']):raise ValueError('Invalid indicators')
                if rec['image'] and not re.fullmatch(r'/images/[a-f0-9]{32}\.(jpg|png|webp)',rec['image']):raise ValueError('Invalid image path')
                (CASES/(cid+'.json')).write_text(json.dumps(rec,indent=2));self.send({'id':cid});return
            raise ValueError('Unknown API route')
        except Exception as e:self.send({'error':str(e)},400)

if __name__=='__main__':
    print('OSINT Sentinel running on http://127.0.0.1:8765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
