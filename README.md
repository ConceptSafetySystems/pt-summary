#Pivotal Tracker - Projects summary report (written by Kelvin Leung for Locatrix Communications)
---

#### This python script is used to fetch all your current tasks of each project that you are involved in
* Only current tasks will be fetched.
* All tasks except delivered tasks and accepted tasks will be fetched.

#### Step of running python script for getting the summary report via email
1.	unzip and install the Pivotal API client library file - busyflow.pivotal-0.3.4.tar.gz
 a. tar zxvf busyflow.pivotal-0.3.4.tar.gz
 b. cd busyflow.pivotal-0.3.4
 c. python setup.py install
2.	unzip and install the Comprehensive HTTP client library - httplib2-0.8.tar.gz
 a. apt-get install httplib2 (If it's available - otherwise install it manually as below)
 b. tar zxvf httplib2-0.8.tar.gz
 c. cd httplib2-0.8
 d. python setup.py install
3.	open config.py and change the configuration settings
4.	run the python script - pt_summary.py
5.  setup a nightly cron job if you like
 a. crontab -e
 b. 0 0 * * * python /home/username/pt_summary/pt_summary.py 