'''
File: Ingredients.py
Edited by Samantha Robertson
SUNet ID: srobert4

This file contains the implementation of the
Ingredient class.
'''


class Ingredient(object):
    def __init__(self, ingredient_data):
        '''
        Assigns quantity and food attributes.
        Let's assert that, if the first character
        is a number, then the first two words represent a quantity,
        i.e. 1 cup flour, 2 tablespoons sugar (for measurable quantities)
        If the first charcter isn't a number, then we assume it's an
        indivisble quantity "Pinch of Salt"
        '''
        if ingredient_data == '':
            self.quantity = 'None'
            self.food = 'None'
            return

        words = ingredient_data.split(' ')
        if words[0].isnumeric():
            self.quantity = ' '.join(words[0:2])
            self.food = ' '.join(words[2:])
        else:
            self.quantity = ''
            self.food = ingredient_data.strip()

    def __str__(self):
        return "Ingredient(quantity=\"{}\", type=\"{}\")".format(
            self.quantity, self.food)
