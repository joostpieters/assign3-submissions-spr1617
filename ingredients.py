class Ingredient(object):
    def __init__(self, ingredient_data):
        # Let's assert that, if the first character is a number, then the first two words represent a quantity,
        # i.e. 1 cup flour, 2 tablespoons sugar (for measurable quantities)
        # If the first charcter isn't a number, then we assume it's an
        # indivisble quantity "Pinch of Salt"
        if ingredient_data == '':
            self.quantity = 'None'
            self.food = 'None'
            return

        if ord(ingredient_data[0]) >= 48 and ord(ingredient_data[0]) <= 57:
            count = 0
            for character in ingredient_data:
                if ord(character) == 32:
                    count += 1
                    if count == 2:
                        break
            self.quantity = ingredient_data[:count].strip()
            self.food = ingredient_data[count:].strip()
        else:
            self.quantity = ''
            self.food = ingredient_data.strip()

    def __str__(self):
        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(
            self.quantity, self.food)


class IngredientList(object):
    def __init__(self, all_ingredient_data):
        self.ingredients = [Ingredient(line)
                            for line in all_ingredient_data.split('\n')]

    def how_many_of(self, ingredient_name):
        for ingredient in self.ingredients:
            if ingredient.food == ingredient_name:
                return ingredient.quantity

    def size(self):
        return len(self.ingredients)

    def get_ingredient(self, index):
        return self.ingredients[index]

    def contains_ingredient(self, ingredient):
        for my_ingredient in self.ingredients:
            if ingredient in my_ingredient.food:
                return True
        return False
