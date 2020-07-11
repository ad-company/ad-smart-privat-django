# AD Smart Privat Project

## Heroku
Deploy          : ./heroku-push-deploy.sh
Create SU       : heroku run python3 manage.py createsuperuser --app <name_app>
Makemigrations  : heroku run python3 manage.py makemigrations --app <name_app>
Migrate         : heroku run python3 manage.py migrate --app <name_app>
