# slack-bot

I used OpenAI's API to convert natural language queries to sql queries. 

I have used SQLAlchemy here just to experiment a bit didnt want to use a database connector and there by using SQLAlchemy i was able to try ORM.
The query's resultset is turned into markdown table which i am sending as a file.
I am writing this at 2AM, I so wanted to add charts but could not work on it. A lot of yime went into trying to deploy.

Automated messages work using a cron job scheduled for every minute. Each minute it goes through the tbale anf if its time to send message sends it int he channel id which is also saved and updates the time for next message to next hour.
When bot is added to a channel a row with joining time, channel id and time for next mesage is added into job table

I tried python's schedulers here but for some reason it didnt work for me. I then tried running cronjob by directly running python file but tht was also very unreliable so i made a bash file that is run by the cronjob

* * * * * /bin/bash /home/gsl-ggn-lt-55/qa-bot/cron-file.sh > /home/gsl-ggn-lt-55/qa-bot/output.txt 2>&1
        
I wanted to do NLP queries on slash command but apparently slash commands need output in 3 seconds or less and i was timing out so i shifted to incoming message events        .
slash command is still there though

For CI/CD
I was unable to deploy the bot. It is currently hosted locally using ngrok's tunneling. I had this project in a virtual en. I was unable to push venv and hence deploying became tedious. I tried for hours on netlify but build only failed.


