import ingredients
import duration


def recipe_from_args(args):
    return Recipe(
        args.get('name'),
        args.get('cookTime'),
        args.get('prepTime'),
        args.get('description'),
        args.get('image'),
        args.get('ingredients'),
        args.get(
            'instructions',
            []),
        args.get('recipeYield'))


class Recipe(object):

    def __init__(*args):
        self, *info = args
        self.name = info[0]
        self.cookingTime = duration.Duration(info[1])
        self.preparationTime = duration.Duration(info[2])
        self.descr = info[3]
        self.im = info[4]
        self.ingredients = ingredients.IngredientList(info[5])
        self.instructions = info[6]
        self.recipe_yield = info[7]

    def pretty_print(self):
        print("\n\n********" + self.name + "********\n")
        print("Cooking Time: " + str(self.cookingTime) +
              "\tPreparation Time: " + str(self.preparationTime))
        print("Yield: " + str(self.recipe_yield)
              if self.recipe_yield else 'Unknown')
        print("Description: " + str(self.descr))
        print("Ingredients:")
        for i in range(self.ingredients.size()):
            print("\t" + str(self.ingredients.get_ingredient(i)))
        print('Instructions')
        for instruction in self.instructions:
            print("\t" + instruction)


# associates recipe names with recipes
class RecipeBook(object):

    def __init__(self, recipes):
        # Changed to dict compression
        self.recipes = {recipe.name: recipe for recipe in recipes}

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
            if recipe.ingredients.contains_ingredient(ingredient):
                yield recipe
