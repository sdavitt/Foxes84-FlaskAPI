# Additional classes and functions I wrote to make my routes easier
# must install the requests package in our venv to use it
from re import X
import requests as r

def getActorImages(): 
    response = r.get('https://foxes71api.herokuapp.com/api/actors')
    if response.status_code == 200:
        data = response.json()
    else:
        return response.status_code
    # [(<actor_name>,<image_url>),] list of tuples containing actor names and image urls
    actors=[]
    for name in data:
        if data[name]['image'] and name != 'Danny DeVito':
            actors.append((name, data[name]['image']))
    return actors

