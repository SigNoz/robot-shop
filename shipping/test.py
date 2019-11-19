import requests
from random import choice 

# country codes
codes = requests.get('http://localhost:8080/codes')
code = choice(codes.json())
print (codes.json())
print (code)


# cities = requests.get('http://localhost:8080/cities/au')
# print (cities.json())