=====
ThiccGaming.com
=====

This is the source code to ThiccGaming.com, we're powered by Python and Django along with Mezzanine and DjangoBB for the forums. Feel free to fix bugs or make improvements, or use this code for your own projects :)

My stack includes: Django, Sentry, Nginx, SteamCMD, MySQL (instead of postgres because i can integrate with game servers much easier,) Docker, Docker-compose, AWS S3, and AWS SES.

Quick start
-----------

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

*** Search 'spam domain text files' on google to find great templates. ***

6. Run `python manage.py migrate` to create the models.

7. Start the development server with `python manage.py runserver`
   and visit http://127.0.0.1:8000/

## Future Plans

* Make Thicc Bans its own package. Since it is a fully fledged custom django ban sytem which integrates with sourcemod servers, it is the best
  competitor to sourcebans, and the only competitor which works on django, removing the need to host any PHP on your stack.

* Create a custom Stats system
