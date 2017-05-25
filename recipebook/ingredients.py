class IngredientList(object):
    def __init__(self, all_ingredient_data):
        ingredients = [self.get_quantity_and_food(
            line) for line in all_ingredient_data.split('\n')]
        self.ingredients = ingredients

    def how_many_of(self, ingredient_name):
        for ingredient in self.ingredients:
            if ingredient[1] == ingredient_name:
                return ingredient[0]

    def size(self):
        return len(self.ingredients)

    def get_ingredient(self, index):
        ingr = self.ingredients[index]
        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(
            ingr[0], ingr[1])

    def contains_ingredient(self, ingredient):
        return True in [ingredient in my_ingredient[1]
                        for my_ingredient in self.ingredients]

    def get_quantity_and_food(self, ingredient_data):
        if ingredient_data == '':
            return('None', 'None')

        if ord(ingredient_data[0]) >= 48 and ord(ingredient_data[0]) <= 57:
            i = 0
            count = 0
            for i in range(len(ingredient_data)):
                character = ingredient_data[i]
                if ord(character) == 32:
                    count += 1
                    if count == 2:
                        break
            quantity = ingredient_data[0:i:1].strip()
            food = ingredient_data[i:len(ingredient_data):1].strip()
        else:
            quantity = ''
            food = ingredient_data.strip()
        return (quantity, food)
