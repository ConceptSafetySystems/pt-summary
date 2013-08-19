#!/usr/bin/python
# This python script is used to fetch all the user's current tasks in each projects

## Import Libraries ##
from busyflow.pivotal import PivotalClient  # Import the busyflow.pivotal api client library

import smtplib  # Enable to send email with an SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import thread
import threading
import time
from time import gmtime, strftime   # Enable to handle date & time

import config   as const # Configuration    

# The user has to provide the pivotal tracker api client in order to fetch the user's projects
# The cache directory is used to cache all stories fetched from user's request
client = PivotalClient(token = const.PT_API_TOKEN, cache= const.CACHE_DIR)

# Get all projects
projects = client.projects.all()['projects']


# Create email content
msg = MIMEMultipart()
htmlBody = []

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, counter, projectID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.counter = counter
        self.projectID = projectID
    
    def run(self):
        # Get lock to synchronize threads
        threadLock.acquire()
        try:
            print "Fetching project: %s" % self.projectID
            # Get all currents task from each project
            project = client.projects.get(self.projectID)   # Get specific project's details
        
            project_current = client.iterations.current(self.projectID) # Get current tasks from specific project
        
            # Show the project name 
            htmlBody.append('<p><b>')
            htmlBody.append(project['project']['name']);
            htmlBody.append('</p></b>')

            # Iterate current tasks of the specific project
            iterations = project_current['iterations']
            htmlBody.append('<ul>')     # Create a bulleted list
            for iteration in iterations:
                stories = iteration['stories']
                for story in stories:
                    try:
                        # Restriction of shown tasks
                        # Only get the task which is assigned to you
                        # Do not get the task which is either delivered or accepted
                        if(story['owned_by'] == const.PT_DISPLAY_NAME and story['current_state'] != 'delivered' and story['current_state'] != 'accepted'):
                            htmlBody.append('<li>')
                            htmlBody.append(story['name'])
                            htmlBody.append(' - ')
                            htmlBody.append(story['current_state'])
                            htmlBody.append(' - <a href="')
                            htmlBody.append(story['url'])
                            htmlBody.append('">')
                            htmlBody.append(story['url'])
                            htmlBody.append('</a></li>')
                    except:
                        pass
            htmlBody.append('</ul>')
            # Free lock to release next thread
            threadLock.release()
        except:
            print "Unable to fetch the project"
            threadLock.release()
            exitFlag = 1


threadLock = threading.Lock()
threads = []
count = 0

# Create new threads for each project
for p in projects:
    threads.append(myThread(count, count, p['id']))
    count += 1

# Start new threads
for thread in threads:
    thread.start()

#Wait for all threads to complete
for thread in threads:
    thread.join()

print "Succeed to summarise your tasks."

# Build email content
print "Sending summry to you via email."
msg.attach(MIMEText(''.join(htmlBody), _subtype="html"))
msg['Subject'] = "Summary of current tasks in PivotalTracker "+strftime("%a, %d/%m/%Y", gmtime())
msg['From'] = const.MY_EMAIL
msg['To'] = const.MY_EMAIL

# Send the summary via email
try:
    smtpObj = smtplib.SMTP(const.EMAIL_SERVER, const.EMAIL_PORT)
    if (const.EMAIL_TLS):
        smtpObj.starttls()
    if (const.MY_EMAIL_PASSWORD != ""):
        smtpObj.login(const.MY_EMAIL, const.MY_EMAIL_PASSWORD)
    smtpObj.sendmail(const.MY_EMAIL, const.MY_EMAIL, msg.as_string())
    smtpObj.quit()
    print "Successfully sent email"
except smtplib.SMTPException as error:
    print "Error: unable to send email :  {err}".format(err=error)


### async thread single html body then join once all thread excuted send email eventually
