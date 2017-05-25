# Asks users for info and then does things with them
from recipe import *
import json


def ask_for_filename(prompt="Filename?", default='recipes.json'):
    raw = default
    try:
        raw = input(prompt) or default
        # See, it's easier to ask for forgiveness then permission
        open(raw, 'r').read()  # See if they gave us a file we can open
    except BaseException:
        raise Exception("Bad filename!")
    finally:
        return raw


userInput = ask_for_filename(
    'Where should we load the local recipes from'
    '(use recipes.json if you aren\'t sure)? ', default='recipes.json')
file = open(userInput, 'r+')
lines = file.read().split('\n')
recipes = [recipe_from_args(json.loads(l)) for l in lines]
book = RecipeBook(recipes)
file.close()
