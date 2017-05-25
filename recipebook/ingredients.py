ASCII_0 = 48
ASCII_9 = 57
ASCCI_SPACE = 32

class IngredientList(object):
    def __init__(self, all_ingredient_data):
        if isinstance(all_ingredient_data, list):
            self.ingredients = [self.parse_ingredient(line) for line in all_ingredient_data]
        else:
            self.ingredients = [self.parse_ingredient(line) for line in all_ingredient_data.split('\n')]

    def parse_ingredient(self, ingredient_data):
        if ingredient_data == '':
            return

        if ord(ingredient_data[0]) >= ASCII_0 and ord(ingredient_data[0]) <= ASCII_9:
            split_ingred_data = ingredient_data.split(' ')
            quantity = split_ingred_data[0] + ' ' + split_ingred_data[1]
            food = ' '.join(split_ingred_data[2:])
        else:
            quantity = ''
            food = ingredient_data.strip()

        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(quantity, food)

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
            if my_ingredient != None and ingredient in my_ingredient:
                return True
        return False








# class Ingredient(object):
#     def __init__(self, ingredient_data):
#         # Let's assert that, if the first character is a number, then the first two words represent a quantity,
#         # i.e. 1 cup flour, 2 tablespoons sugar (for measurable quantities)
#         # If the first charcter isn't a number, then we assume it's an indivisble quantity "Pinch of Salt"
#         if ingredient_data == '':
#             self.quantity = 'None'
#             self.food = 'None'
#             return

#         if ord(ingredient_data[0]) >= ASCII_0 and ord(ingredient_data[0]) <= ASCII_9:
#             i = 0
#             count = 0
#             for i in range(len(ingredient_data)):
#                 character = ingredient_data[i]
#                 if ord(character) == 32:
#                     count += 1
#                     if count == 2:
#                         break
#             self.quantity = ingredient_data[0:i:1].strip()
#             self.food = ingredient_data[i:len(ingredient_data):1].strip()
#         else:
#             self.quantity = ''
#             self.food = ingredient_data.strip()

#     def __str__(self):
#         return "Ingredient(quantity=\"{}\", type=\"{}\")".format(self.quantity, self.food)

# class IngredientList(object):
#     def __init__(self, all_ingredient_data):
#         ingredients = []
#         for line in all_ingredient_data.split('\n'):
#             ingredients += [Ingredient(line)]
#         self.ingredients = ingredients

#     def how_many_of(self, ingredient_name):
#         for ingredient in self.ingredients:
#             if ingredient.food == ingredient_name:
#                 return ingredient.quantity

#     def size(self):
#         return len(self.ingredients)

#     def get_ingredient(self, index):
#         return self.ingredients[index]

#     def contains_ingredient(self, ingredient):
#         r = False
#         for my_ingredient in self.ingredients:
#             if ingredient in my_ingredient.food:
#                 r = True
#         return r
