# Loads a static database of recipes into a recipe book called book at module level.
# Asks users for info and then does things with them
import recipe
import json

def get_file():
    filename = input('Where should we load the local recipes from? Enter a blank line to use recipes.json ')
    if not filename:
        filename = "recipes_fixed.json"
    with open(filename, 'r+') as infile:
        return infile.read()
recipes = []
json_data = json.loads(get_file())
for r in json_data:
    recipes.append(recipe.recipe_from_args(r))
book = recipe.RecipeBook(recipes)
