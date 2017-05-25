''' File: writebook.py
-----------------------------------------------------------
Loads a static database of recipes into a recipe book called book at module level.
Asks user what file to load from and checks to make sure it will work
'''

import recipe
import json

userInput = input("Where should we load the local recipes from (use recipes.json if you aren't sure)? ")
if not userInput:
    userInput = 'recipes.json'
with open(userInput, 'r+') as file:
    recipes = [recipe.recipe_from_args(entry) for entry in json.load(file)]
    book = recipe.RecipeBook(recipes)
