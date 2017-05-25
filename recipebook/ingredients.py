class Ingredient(object):
    def __init__(self, ingredient_data):
        # Let's assert that, if the first character is a number, then the first two words represent a quantity,
        # i.e. 1 cup flour, 2 tablespoons sugar (for measurable quantities)
        # If the first charcter isn't a number, then we assume it's an indivisble quantity "Pinch of Salt"
        if ingredient_data == '':
            self.quantity = 'None'
            self.food = 'None'
            return

        if ingredient_data[0].isdigit():
            first = ingredient_data.find(' ')
            i = ingredient_data[first+1:].find(' ')
            self.quantity = ingredient_data[0:first+i+1].strip()
            self.food = ingredient_data[first+i+1:len(ingredient_data)].strip()
        else:
            self.quantity = ''
            self.food = ingredient_data.strip()

    def __str__(self):
        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(self.quantity, self.food)

class IngredientList(object):
    def __init__(self, all_ingredient_data):
        ingredientslst = all_ingredient_data.split('\n')
        self.ingredients = [Ingredient(ingredient) for ingredient in ingredientslst]

    def how_many_of(self, ingredient_name):
        for ingredient in self.ingredients:
            if ingredient.food == ingredient_name:
                return ingredient.quantity

    def size(self):
        return len(self.ingredients)

    def get_ingredient(self, index):
        return self.ingredients[index]

    def contains_ingredient(self, ingredient):
        return ingredient in (i.food for i in self.ingredients)
