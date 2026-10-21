# Credits and third-party projects

OSINT Sentinel is an independent dashboard, integration layer, and installer. The research tools and operating environment are the work of their original authors and contributors. Their names, copyright notices, and licenses remain theirs. Use of a project name does not imply affiliation, sponsorship, or endorsement.

## Research tools

- **[Sherlock](https://github.com/sherlock-project/sherlock)** — created by **Siddharth Dushantha**, maintained by the Sherlock Project and its contributors. Provides the username search engine and site-detection rules. [Upstream license](https://github.com/sherlock-project/sherlock/blob/master/LICENSE).
- **[Maigret](https://github.com/soxoj/maigret)** — by **soxoj and the Maigret contributors**. Provides username research and HTML reporting. [Upstream license](https://github.com/soxoj/maigret/blob/main/LICENSE). Maigret also acknowledges its own upstream projects; see its README and notices for that lineage.

Sentinel invokes these tools through their command-line interfaces. We do not claim authorship of their search engines, site databases, or detection logic. Please report tool-specific issues upstream with enough information to reproduce them, and consider supporting their maintainers.

## Android and Linux foundation

| Project and authors | How it is used | License / notices |
| --- | --- | --- |
| [Termux team and contributors](https://github.com/termux/termux-app) | Android terminal and package environment | [Upstream license](https://github.com/termux/termux-app#license) |
| [Termux:Widget contributors](https://github.com/termux/termux-widget) | Home-screen launcher for the startup script | [Upstream license](https://github.com/termux/termux-widget#license) |
| [PRoot-Distro contributors](https://github.com/termux/proot-distro) | Debian environment installation and login | [Upstream license](https://github.com/termux/proot-distro/blob/master/LICENSE) |
| [PRoot authors and contributors](https://github.com/proot-me/proot) | Rootless Linux environment support | [Upstream licensing](https://github.com/proot-me/proot#license) |
| [Debian Project and package maintainers](https://www.debian.org/) | Linux distribution and packages | [Debian licensing information](https://www.debian.org/legal/licenses/); installed package notices in `/usr/share/doc/*/copyright` |
| [Python authors and Python Software Foundation](https://www.python.org/) | Local server and search-tool runtime | [Python license and history](https://docs.python.org/3/license.html) |
| [pipx / Python Packaging Authority contributors](https://github.com/pypa/pipx) | Isolated search-tool installation | [Upstream license](https://github.com/pypa/pipx/blob/main/LICENSE) |
| [GNU Project and contributors](https://www.gnu.org/) | Bash, coreutils, tar and other shell utilities | [GNU licenses](https://www.gnu.org/licenses/); each package retains its own notices |
| [curl authors and contributors](https://curl.se/) | Local server readiness checks | [curl license](https://curl.se/docs/copyright.html) |
| [util-linux contributors](https://github.com/util-linux/util-linux) | `flock` for concurrent-start protection | [Upstream copying notices](https://github.com/util-linux/util-linux/blob/master/README.licensing) |

This is a practical list of direct integrations and foundations, not an exhaustive inventory of every transitive dependency. Installed packages retain their own author credits and license notices. Consult the installed version's license for its terms.

## Distribution and scope

The generated Sentinel installer embeds Sentinel application and setup files. It downloads third-party packages through Termux, Debian and PyPI during setup; it does not bundle those projects' source trees, APKs, root filesystems, or research datasets. This acknowledgments file travels with the application source bundle.

Third-party projects retain their own licenses. This file does not relicense them or replace their notices. If a future release vendors third-party source, binaries, datasets, or assets, include the corresponding license/copyright notices and meet the applicable distribution terms for that material.

SpiderFoot is not included or modified. The image-search links point to independent external services—Google Lens, Bing, TinEye, and Yandex. Those services and their names belong to their respective owners.
