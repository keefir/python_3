import json

with open('games.json') as games:
    print(len(json.load(games)['survival']))