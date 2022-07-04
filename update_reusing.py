from argparse import ArgumentParser
from gdparchis.reusing.github import download_from_github

parser=ArgumentParser()
parser.add_argument('--local', help='Parses files without download', action="store_true", default=False)
args=parser.parse_args()      

if args.local==False:
    download_from_github("turulomio", "reusingcode", "django/request_casting.py", "gdparchis/reusing")
    download_from_github("turulomio", "reusingcode", "python/casts.py", "gdparchis/reusing")
    download_from_github("turulomio", "reusingcode", "python/datetime_functions.py", "gdparchis/reusing")
    download_from_github("turulomio", "reusingcode", "python/github.py", "gdparchis/reusing")
    download_from_github("turulomio", "reusingcode", "django/responses_json.py", "gdparchis/reusing")
