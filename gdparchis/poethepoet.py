from gdparchis.reusing.github import download_from_github
from os import system
from sys import argv

def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local==False:
        download_from_github("turulomio", "reusingcode", "python/github.py", "gdparchis/reusing")
        download_from_github("turulomio", "django_calories_tracker", "calories_tracker/tests_helpers.py", "gdparchis/reusing")

def cypress_test_server():
    print("- Dropping test_calories_tracker database...")
    system("dropdb -U postgres -h 127.0.0.1 test_calories_tracker")
    print("- Launching python manage.py test_server with user 'test' and password 'test'")
    system("python manage.py testserver calories_tracker/fixtures/all.json calories_tracker/fixtures/test_server.json --addrport 8011")
