rsyncstats
==========

Description
-----------

rsyncstats summarizes transfer logs. For each day transfers took place, the amount of transmitted data per operation (receive, send) is determined. Calculations are based on log entries in the systemd journal made by the rsync daemon. To get correct values, the placeholder `%l` (length of file in bytes) has to be replaced by `%b` (number of bytes actually transferred) in the default setting of parameter `log format` in file `rsyncd.conf`. The timeframe to be examined can be limited with journalctl options `--since` and `--until`.

Example
-------

Show statistics since the given date until today:
```shell
journalctl --output=json --since=2019-02-19 | rsyncstats
```

