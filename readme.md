![alt text](https://github.com/dudekmichal/django-kudosbot/blob/master/img/kudos.png?raw=true)

# kudosbot
Bot for giving kudos to activities of other people on Strava.

![alt text](https://github.com/dudekmichal/django-kudosbot/blob/master/img/list_of_kudos.png?raw=true)

# Table of content
- [Setup](#setup)
    + [Create virtualenv](#create-virtualenv)
    + [Create database](#create-database)
    + [Migrate the database](#migrate-the-database)
    + [Create an administrative account](#create-an-administrative-account)
    + [Enabling bot](#enabling-bot)
    + [Apache2 configuration](#apache2-configuration)
- [Other/optional](#other-optional)
  * [Migrate data from SQLite to PostgreSQL](#migrate-data-from-sqlite-to-postgresql)

# Setup

### Create virtualenv
    $ sudo apt install python3-pip postgresql postgresql-contrib chromium-chromedriver apache2 libapache2-mod-wsgi-py3
    $ sudo pip3 install virtualenv
    $ cd django-kudosbot
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

### Create database
    $ psql
    $ CREATE DATABASE <db_name>;
    $ CREATE USER <db_user> WITH PASSWORD '<db_pass>';
    $ ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    $ ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    $ ALTER ROLE myprojectuser SET timezone TO 'UTC';
    $ GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
    $ \q
    $ exit

### Migrate the database
    $ python manage.py makemigrations
    $ python manage.py migrate

### Create an administrative account
    $ python manage.py createsuperuser

### Enabling bot
  1. Add clubs in given format:

  ![alt text](https://github.com/dudekmichal/django-kudosbot/blob/master/img/adding_club.png?raw=true)

  2. Click on "Enable bot" button.

### Apache2 configuration
    $ python3 manage.py collectstatic
    Adjust django-kudosbot/000-default.conf file for your settings.    
    $ sudo cp 000-default.conf /etc/apache2/sites-available/000-default.conf
    $ vim kudosbot/kudosbot/.env
    Adjust constants.
    $ python manage.py check --deploy
    Fix printed warnings.
    $ sudo systemctl restart apache2

# Other/optional

## Migrate data from SQLite to PostgreSQL
    $ (venv) python3 manage.py dumpdata > datadump.json
    <configuration of PostgreSQL server>
    $ python3 manage.py migrate --run-syncdb
    $ python3 manage.py shell
    >>> from django.contrib.contenttypes.models import ContentType
    >>> ContentType.objects.all().delete()
    >>> quit()
    python3 manage.py loaddata datadump.json