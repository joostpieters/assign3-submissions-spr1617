# Loads a static database of recipes into a recipe book called book at module level.
# Asks users for info and then does things with them
from recipe import *
import json

def ask_for_filename(prompt="Filename?", default='recipes.json'):
    raw = default
    try:
        raw = input(prompt) or default
        # See, it's easier to ask for forgiveness then permission
        open(raw, 'r').read()  # See if they gave us a file we can open
    except:
        raise Exception("Bad filename!")
    finally:
        return raw

def get_book():
    userInput = ask_for_filename('Where should we load the local recipes from (use recipes.json if you aren\'t sure)? ', default='recipes.json')
    recipefile = open(userInput, 'r+')
    recipes = json.load(recipefile)
    recipefile.close()
    recipelst = [recipe_from_args(r) for r in recipes]
    return RecipeBook(recipelst)