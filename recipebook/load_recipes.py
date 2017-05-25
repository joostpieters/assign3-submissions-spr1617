# Loads a static database of recipes into a recipe book called book at module level.
# Asks users for info and then does things with them
from recipe import *
import json

user_prompt = 'Where should we load the local recipes from (hit ENTER to use recipes.json by default)? '
user_input = input(user_prompt) or 'recipes.json'

try:
    with open(user_input, 'r') as input_file:
        data = input_file.read()
        lines = data.split('\n')

        recipes = []
        for line in lines:
            recipe = recipe_from_args(json.loads(line))
            recipes.append(recipe)

        book = RecipeBook(recipes)
except IOError:
    print("Could not read file:", user_input)
