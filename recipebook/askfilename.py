# Loads a static database of recipes
# into a recipe book called book at module level.
# Asks users for info and then does things with them
from recipe import recipe_from_args, RecipeBook
import json


def ask_for_filename(prompt, default='recipes.json'):
    try:
        raw = input(prompt) or default
        open(raw, 'r').read()  # See if they gave us a file we can open
    except BaseException:
        raise Exception("Bad filename!")
    finally:
        return raw

userask = ('Where should we load the local recipes from '
           '(use recipes.json if you aren\'t sure)? ')
userInput = ask_for_filename(userask)
with open(userInput, 'r+') as f:
    lines = f.read().split('\n')
    book = RecipeBook(
        [recipe_from_args(json.loads(line))for line in lines]
    )
