# jenkins_applet
This applet is for Linux systems that are using Conky or another app 
to execute applet/jenkins_poll.py for reporting statuses of Jenkins jobs.

###Applet
![alt tag](https://github.com/meanbunny/jenkins_applet/blob/master/screenshots/jenkins_applet_ss.png)

###Conky
![alt tag](https://github.com/meanbunny/jenkins_applet/blob/master/screenshots/jenkins_conky_ss.png)

###Running Applet
`nohup applet/jenkins_applet.py &`

###Running Poller in Conky
`${execpi 5 python /home/meanbunny/.jenkins_applet/jenkins_poll.py}`

###Running Poller in Cron
`5 * * * * /home/meanbunny/.jenkins_applet/jenkins_poll.py`

