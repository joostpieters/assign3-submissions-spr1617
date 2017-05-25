'''
File: Recipe.py
Edited by Samantha Robertson
SUNet ID: srobert4

This file contains the implementation of the
Recipe class.
'''

from ingredients import Ingredient
from duration import Duration


class Recipe(object):
    def __init__(self, args):
        self.name = args.get('name')
        self.cookingTime = Duration(args.get('cookTime'))
        self.preparationTime = Duration(args.get('prepTime'))
        self.descr = args.get('description')
        self.im = args.get('image')
        self.ingredients = [Ingredient(line) for line in args.get(
            'ingredients').strip().split('\n')]
        self.instructions = args.get('instructions', [])
        self.recipe_yield = args.get('recipeYield')

    def pretty_print(self):
        print("\n\n********" + self.name + "********\n")
        print("Cooking Time: " +
              str(self.cookingTime) +
              "\tPreparation Time: " +
              str(self.preparationTime))
        print("Yield: " + str(self.recipe_yield)
              if self.recipe_yield else 'Unknown')
        print("Description: " + str(self.descr))
        print("Ingredients:")
        for ingredient in self.ingredients:
            print("\t" + str(ingredient))
        print('Instructions')
        for instruction in self.instructions:
            print("\t" + instruction)

    def contains_ingredient(ingredient):
        '''
        Checks whether the given ingredient
        is found anywhere in the ingredient list
        for this recipe
        '''
        for my_ingredient in self.ingredients:
            if ingredient in my_ingredient.food:
                return True
        return False

    def good_recipe(self, keywords, includes, excludes):
        '''
        Takes three lists: one of keywords; one of ingredients to include;
        and one of ingredients to exclude. Returns bool indicating whether
        or not this recipe matches these search terms
        '''
        for word in keywords:
            if word.lower() not in self.descr.lower():
                return False

        for include in includes:
            if not self.contains_ingredient(include):
                return False

        for exclude in excludes:
            if self.contains_ingredient(exclude):
                return False

        return True
