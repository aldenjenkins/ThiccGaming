# ThiccGaming.com

This is the source code to the ThiccGaming web app.

This stack includes: Docker-compose, Django, Sentry, reCAPTCHA, Nginx, SteamCMD, MySQL (Instead of PostgreSQL because I can integrate with game servers much easier,) Docker, Docker-compose, AWS S3, and AWS SES.

## Installation

Docker-compose makes the deployment for this very automatited and easy. There is no need to manually create a virtual environment with `mkvirtualenv thicc`, because the build spec of the site dockerfile automates that.

1. Copy mysql/environment.env.example to environment.env and fill it out with your variables. 

2. Repeat this step for site/environment.env.example and use the same info from mysql `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` into site's `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.

3. Create a file called spamdomains.txt in the main project directory which is a file that is made of all domains which you do not want to be allowed to be registered on the website with, each taking up its own line in the file. Each domain must have its top-level domain attached to it. For example:
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

4. __Docker time!__ 
  * Install [Docker](https://docs.docker.com/install/) and [Docker-compose](https://docs.docker.com/compose/install/). Run `docker-compose run django python manage.py migrate` from the main folder. 
      docker-compose creates a volume on the host machine so this only needs to be run once instead of everytime we start the django container. This will also need to be run again every time
      you create new migrations when you run `docker-compose run django python manage.py makemigrations`.
  * Run `docker-compose up` from the main folder.

5. Visit http://localhost/ and notice how there is no port specified on that url. Docker-compose is running
NginX which is listening on port 80. 80 is the default port for all http traffic so this is the same
thing as saying http://localhost:80. connecting to nginx will tell nginx to point your traffic to 
the django app specified in the `nginx/conf.d/local.conf` file.

## Future Plans

* Convert to Pipenv from virtualenvs.

* Make Thicc Bans its own package. Since it is a fully fledged custom Django ban sytem which integrates with sourcemod servers, it is the best
  competitor to sourcebans, and the only competitor which works with Django, removing the need to host any PHP on your stack.

* Create a custom Stats system
