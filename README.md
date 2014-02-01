aprsis-archiver
===============

This script archives reports distributed globally via the
[Automatic Packet Reporting System Internet System](http://www.aprs-is.net/).
The underlying amateur radio-based
[Automatic Packet Reporting System (APRS)](http://en.wikipedia.org/wiki/Automatic_Packet_Reporting_System)
system resembles a set of sensor networks in which amateur
radio operators can locally or globally distribute GPS-based location
reports, messages, telemetry, or weather data. The distributed data
is often displayed on maps either by dedicated clients or by web sites
such as http://aprs.fi/

The purpose of this script is to archive the globally reported ARPS
data for further offline processing.

## Usage

The archiver script fetches APRS reports from the APRS-IS network and stores
its output to a bz2 compressed file. The resulting output can be limited by
specifying server side filters, or by requesting the full feed.

To use the software, you need to specify an APRS-IS server that provides the
feed you desire (e.g., roate.aprs.net).
You can get a list of APRS-IS servers [here](http://aprs-is.net/APRSServers.aspx).

### Filtered Feed

APRS-IS servers allow the specification of
[server-side filters](http://www.aprs-is.net/javAPRSFilter.aspx) to customize
the requested feed to only contain desired reports. Examples include position
reports only or a restriction to certain geographic areas. Filter strings are
specified via the `--filter=` option. Filters thus reduce the data rate and
limited the disk space occupied by the archive.

Filters are available when connection to port 14580.
To only get traffic containing position reports specify the `t/p` filter as follows:
`./aprsis-archiver.py --file=aprsis-archive-positions.bz2 --host rotate.aprs.net --port 14580 --filter="t/p"`

### Unfiltered Feed

Some servers provide the full, unfiltered APRS feed by connecting to port 10152:
`./aprsis-archiver.py --file=aprsis-archive.bz2 --host rotate.aprs.net --port 10152`

When archiving unfiltered feeds, expect about 80MB of compressed data to be
created daily, each containing 2M reports on average. This corresponds to as
much as 30GB of compressed data per year. To limit the required disk space
and reduce the used network bandwidth, specify filters (see above).

## Automation via crontab

Daily archives can be generated by executing `run-cron.sh` on a daily basis
via the systems' crontab.

## Output File Format

The created archive file begins with four comments listing the specified
filter setting (see above), the timestamp (as UNIX timestamp) when the
logging started and two server-side comments. An example header looks
as follows.

```
# APRS filter: None
# Logging start: 1391271292.24
1391271292 # aprsc 2.0.12-gb6dff42
1391271292 # logresp N0CALL unverified, server FOURTH
```

The subsequent lines contain APRS position reports in the APRS-IS format.
Please find a description of the format [here](https://github.com/n2ygk/aprs-bigdata/wiki).
The first field contains the time the report was received, specified as
UNIX timestamp (seconds since Jan 1st, 1970).

```
1391271292 K4PLT-2>APNU3B,WIDE2-1,qAR,N8DEU-5:!3444.13NS08643.65W#PHG5670/W2,ALn    Rainbow Mt AL 1150ft
```

Please find an example parser [here](https://github.com/n2ygk/aprs-bigdata/blob/master/aprspig.py).

## Project examples

* Creating digipeater coverage maps (see example code and documentation [here](https://github.com/n2ygk/aprs-bigdata/))
