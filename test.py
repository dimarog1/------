from requests import delete, get
from pprint import pprint

print(get('http://localhost:5000/api/films/1').json())
