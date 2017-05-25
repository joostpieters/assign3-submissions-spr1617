
from ingredients import IngredientList
from duration import Duration
import collections


def recipe_from_args(args):
    return Recipe(
        args.get('name'),
        Duration(args.get('cookTime')),
        Duration(args.get('prepTime')),
        args.get('description'),
        args.get('image'),
        args.get('ingredients'),
        args.get(
            'instructions',
            []),
        args.get('recipeYield'))


class Recipe(object):
    def __init__(*args):
        Info = collections.namedtuple('INFO',
                                      ['name',
                                       'cookingTime',
                                       'preparationTime',
                                       'descr',
                                       'im',
                                       'ingredients',
                                       'instructions',
                                       'recipe_yield'])
        self = args[0]
        self.info = Info(*(args[1:]))
        if self.info.ingredients is None:
            self.info.ingredients = []

    def pretty_print(self):
        print("\n\n********" + self.info.name + "********\n")
        print("Cooking Time: " +
              str(self.info.cookingTime) +
              "\tPreparation Time: " +
              str(self.info.preparationTime))
        print("Yield: " + str(self.info.recipe_yield)
              if self.info.recipe_yield else 'Unknown')
        print("Description: " + str(self.info.descr))
        print("Ingredients:")
        print(self.info.ingredients)
        print('Instructions')
        for instruction in self.info.instructions:
            print("\t" + instruction)


# associates recipe names with recipes
class RecipeBook(object):

    def __init__(self, recipes):
        # recipes is a list, self.recipes is a dict from name to recipe
        self.recipes = {recipe.info.name: recipe for recipe in recipes}

    def get_recipe_names(self):
        return self.recipes.keys()

    def size(self):
        return len(self.recipes)

    def get_recipe_by_name(self, recipe_name):
        return self.recipes[recipe_name]

    def add_recipe(self, recipe):
        self.recipes[recipe.info.name] = recipe

    def generate_recipes_containing(self, ingredient):
        for recipe_name in self.recipes:
            recipe = self.recipes[recipe_name]
            if recipe.ingredients.contains_ingredient(ingredient):
                yield recipe
