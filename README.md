# Purpose
Gather statistics from a running Sauce Labs VM.  Intended for Sauce Labs support only and offered with _no guarantees_ of any kind.  Customers: Don't use this.  It might use all your minutes, exceed your concurrency, fail your tests and be mean to your dog, and you'll have bought it upon yourself.

(Also don't write to support asking about this they'll give you blank looks and ask me about it and I'll say it's unsupported and they'll close your ticket and you'll be sad.  I don't want you to be sad.)

# Description
Navi consists of two parts; the server and the script.

## Server
The server is run on a known address and serves the script.  It also listens for results and displays them in its log.

The server is all ready to run on Heroku; This is often the easiest way to get it publicaly routable.  You don't even need a sane Ruby runtime to push the script to Heroku.

## Script
The script is a python script that runs as a prerun executable.  Because it needs to run for the duration of the test, it has to run in the background.  Because it runs in the background, it can't write information to the test logs (ask Miketwo for why if you'd like some shouty despair).

The script runs a terminal command at a regular interval.  The results of that command are then POSTed back to the webserver along with a timestamp.

The script configured currently will ping a domain 5 times every 5 seconds.  You'll need to pass the domain as the first argument to the prerun executable.  Load `ping_script.py`

The script can also check `active`, `free` and `in use` memory for Mac every second; load `memory_script.py`

# Requirements
## To run on Heroku
1. A free Heroku account
2. The [Heroku CMD installed](https://devcenter.heroku.com/articles/heroku-cli)
3. Being logged into the Heroku CMD with `heroku login`

## To run on another server
1. Ruby 2.x installed
2. Bundler installed (with `gem install bundler`)
3. The host IP or URL known
4. Possibly some SSL stuffs?  IDK I didn't try this way.

# Operating
## Establishing the server
1. Add an app on the [Heroku dashboard](https://dashboard.heroku.com/new?org=personal-apps)
2. Checkout this repo
3. CD into the repo directory
4. `heroku git:remote -a your_app_name`
5. `git push heroku master`
6. The app should be running on `https://your_app_name.herokuapp.com`

If it deployed successfully, your git output will include:

```
remote:        https://your_app_name.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
```

Check the application logs at `https://dashboard.heroku.com/apps/your_app_name/logs` and you should see output like this:

```
2017-03-31T01:14:48.245418+00:00 heroku[web.1]: State changed from down to starting
2017-03-31T01:14:50.249406+00:00 heroku[web.1]: Starting process with command `bundle exec thin start -R config.ru -e production -p 8398`
2017-03-31T01:14:54.563892+00:00 heroku[web.1]: State changed from starting to up
```

## Setting up the Sauce Labs test
Set the `prerun` desired capability, ensuring it runs in the background:

`caps['prerun'] = {executable: 'https://your_app_name.heroku.com/memory_script', background: true}`
(Example for Ruby)

## Run It
1. Open the log viewer for your app at `https://dashboard.heroku.com/apps/your_app_name/logs`
2. Run your Sauce Labs test

## Logs

Heroku's webapp allows you to see application logs at `https://dashboard.heroku.com/apps/your_app_name/logs`.

### Verify your app fetched the prerun script
`2017-03-31T01:17:27.599052+00:00 app[web.1]: 162.222.73.110 - - [31/Mar/2017:01:17:27 +0000] "GET /memory_script.py HTTP/1.1" 200 1814 0.0064`

### Verify your app is sending _something_ for logging
`2017-03-31T01:17:30.042449+00:00 app[web.1]: 162.222.73.110 - - [31/Mar/2017:01:17:30 +0000] "POST /stat/memory HTTP/1.1" 200 - 0.0008`

### Actual log data
```
2017-03-31T01:17:30.041904+00:00 app[web.1]: Thu Mar 30 18:17:22 2017 - active:656
2017-03-31T01:17:30.041930+00:00 app[web.1]: Thu Mar 30 18:17:22 2017 - free:255
2017-03-31T01:17:30.041931+00:00 app[web.1]: Thu Mar 30 18:17:22 2017 - total:1341.06640625
```

## Customizing the script
The python script is served from `logstats.py` and is currently hardwired to only send memory statistics.  This is because the webserver only knows how to nicely display memory stats.

To log different data, you will need to:
1. Create a new method that executes whatever commandline command you need data from, returning it either as a dictionary of interesting values or a single text blob
2. Change `send_memory_to_server` to call your new method
3. Change `create_post_params` to properly encode your data
4. Add a new route in `routing.rb` to accept your new data
5. Change the URL posted too on line 11 of `logstats.py` to match the new URL
 
# Future plans
## Other statistic scripts
I can immediately think of how to gather MTR, traceroute and ping data during tests.

We could also track CPU usage & open files.

logstats.py should be an ERB file so the servername is populated automagically.
## Parameterized scripts
Allow the parameters of the prerun URL to re-configure the supplied script, eg:

`https://your_app_name/script?interval=20` where `interval` changes the frequency of logging
`https://your_app_name/script?statistic=cpu` logs CPU usage instead of memory

## Better Output
Output as a downloadable log file.
Output as a page in the web app.
Graphed output

## Probably OTT: Sending statistics to an actual logging engine