# This file is part of rsyncstats, distributed under the ISC license.
# For full terms see the included COPYING file.

from collections import Counter, defaultdict, namedtuple
from datetime import date
from json import loads as jsonparse
from os.path import basename
from sys import argv, exit, stderr, stdin
import re


class UsageError(Exception):
    pass


ex = 0
try:
    optpat = None
    if len(argv) > 2:
        raise UsageError(basename(argv[0]) + " [PATTERN]")
    if len(argv) > 1:
        optpat = re.compile(argv[1])

    # pattern of relevant messages by the rsync daemon
    logpat = re.compile(
        r"""(?P<op>recv|send) \s  # operation
            \S+ \s                # host
            \[\S+\] \s            # address
            \S+ \s                # module
            \(\S*\) \s            # user
            (?P<file>.+) \s       # file
            (?P<length>\d+)       # length""", re.VERBOSE
    )
    sumlengths = defaultdict(Counter)  # amount per operation and date
    maxlength = 0  # highest amount ever reached
    dates = set()  # distinct dates at which transfers took place

    # output of `journalctl -o json` is expected as input
    for ln in stdin:
        logent = jsonparse(ln)
        if logent["SYSLOG_IDENTIFIER"] != "rsyncd":
            continue
        if not isinstance(logent["MESSAGE"], str):
            continue

        mat = logpat.fullmatch(logent["MESSAGE"])
        if mat is None:
            continue

        flds = mat.groupdict()
        if optpat is not None and not optpat.match(flds["file"]):
            continue

        date = date.fromtimestamp(int(logent["_SOURCE_REALTIME_TIMESTAMP"]) / 1000000.0)  # microseconds -> seconds
        dates.add(date)
        sumlengths[flds["op"]][date] += int(flds["length"])
        if maxlength < sumlengths[flds["op"]][date]:
            maxlength = sumlengths[flds["op"]][date]

    Unit = namedtuple("Unit", ("factor", "char"))
    scale = (
        Unit(1, "B"), Unit(1024, "K"), Unit(1024 * 1024, "M"), Unit(1024 * 1024 * 1024, "G"), Unit(1024 * 1024 * 1024 * 1024, "T"),
        Unit(1024 * 1024 * 1024 * 1024 * 1024, "P"), Unit(1024 * 1024 * 1024 * 1024 * 1024 * 1024, "E")
    )
    unit = 0
    while unit < len(scale) and maxlength / scale[unit].factor >= 1024:
        unit += 1
    print("DATE\t" + "\t".join(op.upper() for op in sumlengths.keys()))
    for date in sorted(dates):
        print(
            "{0}\t".format(date) + "\t".
            join("{0:>7.2f}{1}".format(sumlengths[op][date] / scale[unit].factor, scale[unit].char) for op in sumlengths.keys())
        )
except UsageError as e:
    print("Usage: " + str(e), file=stderr)
    ex = 2
except Exception as e:
    print("Error: " + str(e), file=stderr)
    ex = 1
exit(ex)

# vim: et sw=4 ts=4
