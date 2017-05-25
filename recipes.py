#!/usr/bin/env python3 -tt
'''File: recipes.py
-----------------------------------------------------------
Main program, handles (almost) all user interaction. Takes the user's
input, finds the pertinent recipes, and organizes and displays the info for
the user in the main interaction loop
'''

import fetcher
import recipe
from recipe import RecipeBook

# Instructions to the user
print('Welcome to the Recipe Book!')
print('I hope you\'re hungry, since we have a lot of recipes to look through!')
print('First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.')
print('Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.')
print('The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2')
print('For example, "dinner +chicken -nuts".')
print('After you search, we\'ll keep the results of the most recent search around.')
print('You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.')
input('Got all that? [Press ENTER to continue...] ')

# Decide if we're going to use allrecipes.com
user_input = input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
while user_input not in ['Y','N']:
    print("That wasn't either a Y or an N! Try again.")
    user_input = input('Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
if user_input == 'Y':
    should_use_all_recipes = True
else:
    from writebook import book # loads static cached book and such
    should_use_all_recipes = False

last_book = None


def process_input():
    '''Function responsible for capturing the user's search string in a
    form usable by the program
    '''

    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if word[0] == '+':   includes.append(word)
        elif word[0] == '-': excludes.append(word)
        else:                keywords.append(word)
    return includes, excludes, keywords

def find_good_recipes(keywords, includes, excludes):
    ''' Searches a static file for recipes that match the user's
    desired search criteria
    '''
    good_recipes = []
    for entry in book.get_recipe_names():
        this_recipe = book.get_recipe_by_name(entry)
        compliant = True
        for word in keywords:
            if word.lower() not in this_recipe.descr.lower():
                compliant = False
        for include in includes:
            if not recipe.contains_ingredient(this_recipe.ingredients, include):
                compliant = False
        for exclude in excludes:
            if recipe.contains_ingredient(this_recipe.ingredients, exclude):
                compliant = False
        if compliant:
            good_recipes.append(book.get_recipe_by_name(entry))
    return good_recipes


# Main interactive loop
while True:

    action = input('(S)earch/(O)rganize? ')
    while action[0].upper() not in ['S','O']:
        action = input('(S)earch/(O)rganize? ')

    # User wants to search for recipes (either from allrecipes or a static file)
    if action[0].upper() == 'S':
        
        # Turn user input into search terms to filter by
        includes, excludes, keywords = process_input()
    
        if should_use_all_recipes:
            recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
            last_book = RecipeBook(recipes)

        else:
            good_recipes = find_good_recipes(keywords, includes, excludes)
            last_book = RecipeBook(good_recipes)
            print("Found {} matching recipes.".format(last_book.size()))

    else:  # Organize
        if not last_book:
            print("Before you can organize some search results, try searching for something!")
        else:
            # note: complexity means number of instructions. some recipes will have zero instructions
            user_input = input("What do you want to do with your search results? \n(V)iew / Sort By Cooking (T)ime / Sort by Number of (I)ngredients / Sort by (C)omplexity? ").strip().upper()
            while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
                user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew / Sort By (T)ime / Sort by Number of (I)ngredients / Sort by (C)omplexity? ").strip().upper()


            recipes = last_book.recipes.values()
            recipe_list = [recipe for recipe in recipes]

            # View in whatever order they're stored
            if user_input == 'V':
                for entry in recipes:
                    entry.pretty_print()

            # View by total time (prep + cooking) from most to least (ties broken arbitrarily)
            elif user_input == 'T':
                for entry in sorted(recipe_list, key=lambda rec: rec.preparationTime.duration + rec.cookingTime.duration, 
                                        reverse=True):
                    entry.pretty_print()

            # View by number of ingredients, from most to least
            elif user_input == 'I':
                for entry in sorted(recipe_list, key=lambda rec: len(rec.ingredients), reverse=True):
                    entry.pretty_print()

            # View by number of instructions (every newline is another instruction), 
            # prints an error instead if a recipe has none
            else:
                for entry in sorted(((recipe.instructions, recipe) for recipe in recipes), 
                                        key=lambda instr: len(instr[0]), reverse=True):
                    if not entry[0]:
                        print("Error! No instructions for recipe {}".format(entry[1]))
                    else:
                        entry[1].pretty_print()

                
    do_continue = input('Another round (Y/N)? ').strip().upper()
    while not do_continue or do_continue[0] not in ['Y','N']:
        do_continue = input('Couldn\'t process. Another round? (Y/N) ').strip().upper()

    if do_continue == 'N':
        break

print('Have a nice life!')