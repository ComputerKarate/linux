# linux
#### Automatic directory cleaner

---
This is intended to create a place where you can place files or directories and they would automatically be removed after a certain period of time.
I use it for web and log related items.

---
An example includes creating a report for a user to download.
I can drop the report into /data/spool/01/report.csv and let the user download it.
In this manner, I don't have to monitor the progress of the download to cleanup the file.
We certainly don't want the file around until we get around to removing it manually since it may have sensitive data in it.

Another example includes daily logging related to a DB backup.
I will put some logs into /data/spool/30/ since I may actually care to look at them later.
If/when there is an issue, I can go take a look at the log since my backup process logs errors.

---
#### Installation
You can clone the repo and add the script location to your path or copy the script somewhere convenient to you.
To effectively take advantage of the script, you need to schedule it to run daily.


---
#### Example log output:
2020-03-30 13:42:32 	**** Starting the file cleanup process ****
2020-03-30 13:42:32 Processing directories under: /data/spool/
2020-03-30 13:42:32 	Purging file: /data/spool/01/locale.alias
2020-03-30 13:42:32 	Purging file: /data/spool/01/magic.mime
2020-03-30 13:42:32 	Purging file: /data/spool/01/magic
2020-03-30 13:42:32 	Purging file: /data/spool/01/bash.bashrc
2020-03-30 13:42:32 	Purging file: /data/spool/01/mke2fs.conf
2020-03-30 13:42:32 	Purging file: /data/spool/01/xattr.conf
2020-03-30 13:42:32 	Purging file: /data/spool/01/appstream.conf
2020-03-30 13:42:32 	Purging file: /data/spool/01/lsb-release
2020-03-30 13:42:32 	Purging file: /data/spool/01/debconf.conf
2020-03-30 13:42:32 	Purging file: /data/spool/01/wgetrc
2020-03-30 13:42:32 	Purging file: /data/spool/01/rsyslog.conf
2020-03-30 13:42:32 	Purging file: /data/spool/01/securetty
2020-03-30 13:42:32 	Purging file: /data/spool/01/login.defs
2020-03-30 13:42:32 	Purging file: /data/spool/01/lintianrc
2020-03-30 13:42:32 Processing directories older than 01 days
2020-03-30 13:42:32 	Purging directory: /data/spool/01/update-notifier
2020-03-30 13:42:32 	Purging directory: /data/spool/01/tmpfiles.d
2020-03-30 13:42:32 	Purging directory: /data/spool/01/binfmt.d
2020-03-30 13:42:32 Processing directories older than 02 days
2020-03-30 13:42:32 Processing directories older than 05 days
2020-03-30 13:42:32 Processing directories older than 07 days
2020-03-30 13:42:32 Processing directories older than 10 days
2020-03-30 13:42:32 NOTE: /data/spool/14 does not exist, creating now
2020-03-30 13:42:32 	Successfully created /data/spool/14
2020-03-30 13:42:32 Processing directories older than 20 days
2020-03-30 13:42:32 Processing directories older than 30 days
2020-03-30 13:42:32 Setting permissions on all files and directories under: /data/spool/


