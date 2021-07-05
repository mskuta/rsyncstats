# This file is part of rsyncstats, distributed under the ISC license.
# For full terms see the included COPYING file.

from invoke import task
from invoke.tasks import call
from pathlib import Path
from zipapp import create_archive

prjdir = Path(__file__).parent.resolve()
prjname = prjdir.name
prjvers = Path(prjdir, "VERSION").read_text().rstrip()
prjarch = "all"
blddir = prjdir / "build" / f"{prjname}_{prjvers}_{prjarch}"


@task
def clean(c):
    c.run(f"rm --force --recursive {blddir.parent}")


@task
def format(c):
    for pyfile in prjdir.rglob("*.py"):
        c.run(f"yapf --in-place '{pyfile}'")


@task
def install(c, prefix="/usr/local"):
    predir = Path(prefix).expanduser()

    # install app
    dstdir = predir / "bin"
    dstdir.mkdir(exist_ok=True, parents=True)
    create_archive(prjdir / "app", dstdir / prjname, "/usr/bin/env python3")

    # install docs
    dstdir = predir / "share" / "doc" / prjname
    dstdir.mkdir(exist_ok=True, parents=True)
    for docfile in (prjdir / "COPYING", prjdir / "README.md"):
        dstfile = dstdir / docfile.name
        with dstfile.open(mode="w") as f:
            f.write(docfile.read_text())
        dstfile.chmod(0o644)


@task(clean, call(install, prefix=str(blddir / "usr")))
def package(c):
    ctlfile = blddir / "DEBIAN" / "control"
    ctlfile.parent.mkdir(exist_ok=False, parents=False)
    with ctlfile.open(mode="w") as f:
        f.write(
            f"Package: {prjname}\nVersion: {prjvers}\nArchitecture: {prjarch}\nDepends: python3\nDescription: Summarize transfer logs\nHomepage: https://github.com/mskuta/{prjname}\nMaintainer: Martin Skuta (https://github.com/mskuta)\nPriority: optional\nSection: utils\n"
        )
        f.flush()
        c.run(f"dpkg-deb --build {blddir}")


# vim: et sw=4 ts=4
