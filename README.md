# jenkins_applet
This applet is for Linux systems that are using Conky or another app 
to execute applet/jenkins_poll.py for reporting statuses of Jenkins jobs.

###Applet
![alt tag](https://github.com/meanbunny/jenkins_applet/blob/master/screenshots/jenkins_applet_ss.png)

###Conky
![alt tag](https://github.com/meanbunny/jenkins_applet/blob/master/screenshots/jenkins_conky_ss.png)

###Adding in jobs
Navigate to your source directory and find the file called servers.json. Make
sure not to put a comma at the end of the last job, otherwise it will complain.
`
{\r\n
  "jobs" : [
   { "name": "Job1", "job" : "https://mybuildserver/job/MyJobName1/" },
   { "name": "Job2", "job" : "https://mybuildserver/job/MyJobName2/" }
 ]
}
`

###Running Applet
`nohup applet/jenkins_applet.py &`

###Running Poller in Conky
`${execpi 5 python /home/meanbunny/.jenkins_applet/jenkins_poll.py}`

###Running Poller in Cron
`5 * * * * /home/meanbunny/.jenkins_applet/jenkins_poll.py`

