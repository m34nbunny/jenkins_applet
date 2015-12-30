# jenkins_applet
This applet is for Linux systems that are using Conky or another app 
to execute applet/jenkins_poll.py for reporting statuses of Jenkins jobs.

###Running Jenkins Applet
`nohup applet/jenkins_applet.py &`

###Running Jenkins Poller (I run this in Conky)
`${execpi 5 python /home/meanbunny/.jenkins_applet/jenkins_poll.py}`

###Running in Cron here
`5 * * * * /home/meanbunny/.jenkins_applet/jenkins_poll.py`

