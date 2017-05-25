''' File: ingredients.py
-----------------------------------------------------------
Defines the Ingredient and IngredientList classes. Processes text data representing ingredients into
an Ingredient class with a quantity and a type, and can put ingredients into an IngredientList, which
is a dictionary from ingredient names to the associated ingredient object
'''

ASCII_ONE = 48
ASCII_NINE = 57
ASCII_SPACE = 32

class Ingredient(object):
    def __init__(self, ingredient_data):
        '''Let's assert that, if the first character is a number, then the first two words represent a quantity,
        i.e. 1 cup flour, 2 tablespoons sugar (for measurable quantities)
        If the first charcter isn't a number, then we assume it's an indivisble quantity "Pinch of Salt"
        '''
        if not ingredient_data:
            self.quantity = 'None'
            self.food = 'None'
            return

        if ord(ingredient_data[0]) >= ASCII_ONE and ord(ingredient_data[0]) <= ASCII_NINE:
            count = 0
            for i in range(len(ingredient_data)):
                character = ingredient_data[i]
                if ord(character) == ASCII_SPACE:
                    count += 1
                    if count == 2:
                        break
            self.quantity = ingredient_data[0:i].strip()
            self.food = ingredient_data[i:].strip()
        else:
            self.quantity = ''
            self.food = ingredient_data.strip()

    def __str__(self):
        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(self.quantity, self.food)