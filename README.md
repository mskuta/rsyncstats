Description
===========

rsyncstats summarizes transfer logs produced by the rsync daemon. For each day transfers took place, the amount of transmitted data per operation (receive, send) is calculated.


Installation
============

- Clone this repository.
- Run the included installation script by entering `sudo ./install.sh`. The default target directory for the executable is `/usr/local/bin`. Use the environment variable `PREFIX` to change this. For example, to install the software under your home directory, type `PREFIX=$HOME/.local ./install.sh` and make sure `$HOME/.local/bin` is in your `$PATH`.

Debian and derivatives (f. e. Ubuntu) 
-------------------------------------

- Download the latest .deb package from the Releases page.
- Install it by entering `sudo dpkg --install <.deb file name>`.


Usage
=====

```shell
Usage: rsyncstats [PATTERN]
```

Calculations are based on log entries in the systemd journal made by the rsync daemon. The journal must be fed via standard input in JSON format. To get correct values, the placeholder `%l` (length of file in bytes) has to be replaced by `%b` (number of bytes actually transferred) in the default setting of parameter `log format` in file `rsyncd.conf`. The time frame to be examined can be limited with journalctl options `--since` and `--until`. In addition, a regular expression can be specified to count only path names matching its pattern.

Examples
--------

Show statistics since the given date until today:
```shell
journalctl --output=json --since=2019-02-19 | rsyncstats
```

Display statistics for all files under the `bacula` directory:
```shell
journalctl --output=json | rsyncstats '^bacula/'
```


License
=======

This software is distributed under the ISC license.


