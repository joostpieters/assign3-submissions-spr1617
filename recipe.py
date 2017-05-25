'''File: recipe.py
-----------------------------------------------------------
Defines the Recipe and RecipeBook classes, two important data structures for handling and querying
the scraped/stored recipe information.
'''

from ingredients import Ingredient
from duration import Duration

def recipe_from_args(args):
    '''
    Function for taking a dictionary containing the recipe information and turning
    it into a Recipe object
    '''
    return Recipe(args.get('name'), args.get('cookTime'), args.get('prepTime'), 
            args.get('description'), args.get('image'), args.get('ingredients'), 
            args.get('instructions', []), args.get('recipeYield'))

class Recipe(object):
    '''
    Data structure for consolidating all the pertinent information for a recipe.
    Supports a method for printing itself in a nice fashion
    '''
    def __init__(*args):
        self, *info = args
        self.name = info[0]
        self.cookingTime = Duration(info[1])
        self.preparationTime = Duration(info[2])
        self.descr = info[3]
        self.image = info[4]
        self.ingredients = [Ingredient(line) for line in info[5].split('\n')]
        self.instructions = info[6]
        self.recipe_yield = info[7]

    def pretty_print(self):
        print("\n\n********" + self.name + "********\n")
        print("Cooking Time: " + str(self.cookingTime) + "\tPreparation Time: " + str(self.preparationTime))
        print("Yield: " + str(self.recipe_yield) if self.recipe_yield else 'Recipe yield unknown')
        print("Description: " + str(self.descr))
        print("Ingredients:")
        for ing in self.ingredients:
            print("\t" + str(ing))
        print('Instructions')
        for instruction in self.instructions:
            print("\t" + instruction)


def contains_ingredient(inglist, ingredient):
    '''
    Helper function for checking if the ingredient list contains the given ingredient
    '''
    for my_ingredient in inglist:
        if ingredient in my_ingredient.food:
            return True
    return False


class RecipeBook(object):
    '''
    Builds a dictionary from recipe names to recipe objects
    '''

    def __init__(self, recipes_list):
        # recipes is a list, self.recipes is a dict from name to recipe
        self.recipes = {}
        for entry in recipes_list:
            self.recipes[entry.name] = entry

    def get_recipe_names(self):
        return self.recipes.keys()

    def size(self):
        return len(self.recipes)

    def get_recipe_by_name(self, recipe_name):
        return self.recipes[recipe_name]

    def add_recipe(self, recipe):
        self.recipes[recipe.name] = recipe

    def generate_recipes_containing(self, ingredient):
        for recipe_name in self.recipes:
            recipe = self.recipes[recipe_name]
            if contains_ingredient(recipe, ingredient):
                yield recipe