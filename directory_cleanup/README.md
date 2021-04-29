# linux
#### Automatic directory cleaner

---
What if you had several directories to choose from for files that you may want to save for only a few days and then make them disappear?  
What if you have a habit of forgetting to go back and perform the housekeeping after a few days to remove the files?  
Just save your file to a directory from the stock ones, /data/spool/{01|05|07|10|14|20|30} or add a new one and your files will just disappear  
  
Adding a new directory is as easy as editing the line in "cleanup" that contains:  
CLEANUP_LIST=( 01 02 05 07 10 14 20 30 )
Just add a new entry  
The new entry must be an integer
If you remove an entry, you will need to manually remove the directory  

By default the cleanup service runs at 3am daily  
  
NOTE: The files/directories under /data/spool will have permissions enirely relaxed so that ANYONE can read/write ANY file  
This process is specifically for mundane logs and files that have no personal or sensitive data  
Except my personal Linux system, only admins login to my Linux servers so it is in a trusted/closed environment  
  
---
This functionality is in two parts  
There is a systemd service that calls a script  
By default the systemd service runs at 3am and it expects the script "cleanup" to be in "/usr/local/bin"  

If you decide to change the location of the script that performs the housekeeping, modify the line in system-cleanup.service that starts with "ExecStart" to the path where you located the file "cleanup":  
ExecStart=/usr/local/bin/cleanup  
  
If you want it to run at some time other than 3am, modify the line in system-cleanup.timer that starts with "OnCalendar":  
OnCalendar=*-*-* 03:00:00  

---
#### Installation
##### Install the cleanup script
It is necessary to create a basic directory structure to begin with  
Run these commands to create that:  
sudo mkdir -p /data/spool/30 
sudo chmod -R 777 /data/spool
  
Now manually copy the file "cleanup" to /usr/local/bin/
   
##### Install the systemd service
To install the systemd service, copy the two files from the repo with the prefix "system-cleanup" to wherever your system puts service files  
/lib/systemd/system/system-cleanup.service  
/lib/systemd/system/system-cleanup.timer  
  
To register your system-cleanup service and timer, run these commands:  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl enable system-cleanup.service  
Created symlink /etc/systemd/system/multi-user.target.wants/system-cleanup.service → /lib/systemd/system/system-cleanup.service.  
  
This will put it on the scheduler  
ComputerKarate@racer-tower:/lib/systemd/system$ sudo systemctl enable system-cleanup.timer  
Created symlink /etc/systemd/system/timers.target.wants/system-cleanup.timer → /lib/systemd/system/system-cleanup.timer.  

#### Starting the system-cleanup service:
Run the following command:  
sudo systemctl start system-cleanup.service  

To verify, check the service status with this command:  
sudo systemctl status system-cleanup.service  

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


