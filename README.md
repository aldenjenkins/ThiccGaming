# ThiccGaming.com

This is the source code to the ThiccGaming web app.

This stack includes: Docker-compose, Django, Sentry, Nginx, SteamCMD, MySQL (instead of postgres because I can integrate with game servers much easier,) Docker, Docker-compose, AWS S3, and AWS SES.

## Quick start

1. Create a virtual environment with `mkvirtualenv thicc` (requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) be installed)

2. `cd thiccgaming/site` then install the dependent packages with `pip install -r requirements.txt`

3. Copy environment.env.example to environment.env and fill it out with your variables. 

4. Create a file called spamdomains.txt in the main project directory which is a file that is made of all domains which you do not want to be allowed to be registered on the website with, each taking up its own line in the file. Each domain must have its top-level domain attached to it. For example:
   ```
   derp.com
   herp.org
   foo.net
   bar.ai
   slurp.mail.com
   test.com
   etcetera.com
   ```

   __Search 'spam domain text files' on google to find great templates.__

5. _Docker time!_ install docker and docker-compose. run `docker-compose up` from the root folder.

6. visit http://localhost/ and notice how there is no port specified on that url. Docker is running
NginX which is listening on port 80. 80 is the default port for all http traffic so this is the same
thing as saying http://localhost:80. connecting to nginx will tell nginx to point your traffic to 
the django app specified in the `nginx/conf.d/local.conf` file.

## Future Plans

* Make Thicc Bans its own package. Since it is a fully fledged custom Django ban sytem which integrates with sourcemod servers, it is the best
  competitor to sourcebans, and the only competitor which works with Django, removing the need to host any PHP on your stack.

* Create a custom Stats system
