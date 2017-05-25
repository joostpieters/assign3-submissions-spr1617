#!/usr/bin/env python3 -tt
"""
File: recipe.py
-----------------------
Assignment 3: Stylize
Course: CS 41
Name: Grant Spellman
SUNet: gshamus

Defines the Recipe class that holds information about a recipe's name, time, description, image url, ingredients, and more. 
"""

from ingredients import IngredientList
from duration import Duration

def recipe_from_args(args):
    """ Returns a Recipe object by unpacking the dict args

    To fill out the attributes of the recipe class, we "get" each attribute from the dict passed in.
    """
    return Recipe(args.get('name'), args.get('cookTime'), args.get('prepTime'), args.get('description'), args.get('image'), args.get('ingredients'), args.get('instructions', []), args.get('recipeYield'))

class Recipe(object):
    def __init__(*args):
        self, *info = args
        self.name = info[0]
        self.cookingTime = Duration(info[1])
        self.preparationTime = Duration(info[2])
        self.descr = info[3]
        self.im = info[4]
        self.ingredients = IngredientList(info[5])
        self.instructions = info[6]
        self.recipe_yield = info[7]

    def pretty_print(self):
        """ Print function for recipe object, displaying all relevant inforamtion"""

        print("\n\n********" + self.name + "********\n")
        print("Cooking Time: " + str(self.cookingTime) + "\tPreparation Time: " + str(self.preparationTime))
        print("Yield: " + str(self.recipe_yield) if self.recipe_yield else 'Unknown')
        print("Description: " + str(self.descr))
        print("Ingredients:")
        for i in range(self.ingredients.size()):
            print("\t" + str(self.ingredients.get_ingredient(i)))
        print('Instructions')
        for instruction in self.instructions:
            print("\t" + instruction)







