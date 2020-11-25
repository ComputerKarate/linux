# linux
#### Automatic directory cleaner

---
What if you had several directories to choose from for files that you may want to save for a few days?  
Just select a directory from the stock ones, /data/spool/{01|05|07|10|14|20|30} or add a new one  
By default the cleanup service runs at 3am daily.  

---
An example includes creating a report for a user to download.  
I can drop the report into /data/spool/01/report.csv and let the user download it.  
In this manner, I don't have to monitor the progress of the download to cleanup the file.  
  
If you decide to change the location, modify the line in system-cleanup.service that starts with "ExecStart" to the path where you located cleanup:  
ExecStart=/data/spool/bin/cleanup  
  
If you want it to run at some time other than 3am, modify the line in system-cleanup.timer that starts with "OnCalendar":  
OnCalendar=*-*-* 03:00:00  

---
#### Installation
I installed the executable script in "/data/spool/bin/cleanup"  
That is the default location in the systemd service.  

To install the systemd service, copy the two files with the prefix "system-cleanup" to wherever your system puts service files  
/lib/systemd/system/system-cleanup.service  
/lib/systemd/system/system-cleanup.timer  
  
To register your system-cleanup service and timer, run these commands:  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl enable system-cleanup.service  
Created symlink /etc/systemd/system/multi-user.target.wants/system-cleanup.service → /lib/systemd/system/system-cleanup.service.  
  
This will put it on the scheduler  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl enable system-cleanup.timer  
Created symlink /etc/systemd/system/timers.target.wants/system-cleanup.timer → /lib/systemd/system/system-cleanup.timer.  

### To start the system-cleanup service, run these commands:
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl start system-cleanup.service  
It will run immediately.  

To verify, check the service status:  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl status system-cleanup.service  
● system-cleanup.service - Temporary file housekeeping  
     Loaded: loaded (/lib/systemd/system/system-cleanup.service; enabled; vendor preset: enabled)  
     Active: inactive (dead) since Tue 2020-11-24 19:18:12 CST; 1min 8s ago  
TriggeredBy: ● system-cleanup.timer  
    Process: 150283 ExecStart=/data/spool/bin/cleanup (code=exited, status=0/SUCCESS)  
   Main PID: 150283 (code=exited, status=0/SUCCESS)  

Nov 24 19:18:12 racer-tower systemd[1]: Started Temporary file housekeeping.  
Nov 24 19:18:12 racer-tower systemd[1]: system-cleanup.service: Succeeded.  

If you want to go the extra mile, you can see the system log to see the results from the Linux perspective:  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo journalctl --since "10 minutes ago"  
-- Logs begin at Tue 2019-12-10 20:41:22 CST, end at Tue 2020-11-24 19:26:56 CST. --  
...  
Nov 24 19:18:12 racer-tower sudo[150280]: ComputerKarate : TTY=pts/1 ; PWD=/usr/lib/systemd/system ; USER=root ; COMMAND=/usr/bin/systemctl start>  
Nov 24 19:18:12 racer-tower sudo[150280]: pam_unix(sudo:session): session opened for user root by (uid=0)  
Nov 24 19:18:12 racer-tower systemd[1]: Started Temporary file housekeeping.  
Nov 24 19:18:12 racer-tower sudo[150280]: pam_unix(sudo:session): session closed for user root  
Nov 24 19:18:12 racer-tower systemd[1]: system-cleanup.service: Succeeded.  

Looks successful!  

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


