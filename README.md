# Description

rsyncstats summarizes transfer logs produced by the rsync daemon. For each day transfers took place, the amount of transmitted data per operation (receive, send) is calculated.


# Installation

## From package

### Debian and derivatives (Ubuntu, Raspbian, etc.)

1. Download the latest .deb package from the [Releases](https://github.com/mskuta/rsyncstats/releases/latest) page.
2. Install it: `sudo dpkg --install rsyncstats_x.y.z_all.deb`

## From source

### As root user

1. Clone this repository: `git clone https://github.com/mskuta/rsyncstats.git`
2. Run the included installation script: `sudo rsyncstats/install.sh`
3. Make sure `/usr/local/bin` is in your `$PATH`.

### As unprivileged user

1. Clone this repository: `git clone https://github.com/mskuta/rsyncstats.git`
2. Run the included installation script: `PREFIX=$HOME/.local rsyncstats/install.sh`
3. Make sure `$HOME/.local/bin` is in your `$PATH`.


# Usage

```
Usage: rsyncstats [PATTERN]
```

Calculations are based on log entries in the systemd journal made by the rsync daemon. The journal must be fed via standard input in JSON format. To get correct values, the placeholder `%l` (length of file in bytes) has to be replaced by `%b` (number of bytes actually transferred) in the default setting of parameter `log format` in file `rsyncd.conf`. The time frame to be examined can be limited with journalctl options `--since` and `--until`. In addition, a regular expression can be specified to count only path names matching its pattern.

## Examples

Show statistics since the given date until today:
```shell
journalctl --output=json --since=2019-02-19 | rsyncstats
```

Display statistics for all files under the `bacula` directory:
```shell
journalctl --output=json | rsyncstats '^bacula/'
```


# License

This software is distributed under the ISC license.


