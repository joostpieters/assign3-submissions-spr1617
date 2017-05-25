#!/usr/bin/env python3 -tt
""" File: recipes.py """

from recipe import RecipeBook
import loadrecipes  # loads static cached book and such

def okay_recipe(recipe, keywords, includes, excludes):
    """Function to determine whether or not a recipe meets criteria"""
    for word in keywords:
        if word.lower() not in recipe.descr.lower():
            return False
    for include in includes:
        if not recipe.ingredients.contains_ingredient(include):
            return False
    for exclude in excludes:
        if recipe.ingredients.contains_ingredient(exclude):
            return False
    return True

def search(should_use_all_recipes):
    """searches for recipes"""
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

    recipes = []
    if should_use_all_recipes:
        import fetcher 
        recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
    else:
        book = loadrecipes.get_book()
        for recipe_name, recipe in book.recipes.items():     
            if okay_recipe(recipe, keywords, includes, excludes):
                recipes.append(recipe)
    last_book = RecipeBook(recipes)
    return last_book

def organize(last_book):
    """organizes recipes"""
    # note: complexity means number of instructions. some recipes will have zero instructions
    user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
        user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    recipes = last_book.recipes.values()
    if user_input == 'V':
        for recipe in recipes:
            recipe.pretty_print()
        return
    decorated = []
    if user_input == 'T':
        decorated = [(recipe.preparationTime.duration + recipe.cookingTime.duration, recipe) for recipe in recipes]
    elif user_input == 'I':
        decorated = [(recipe.ingredients.size(), recipe) for recipe in recipes]
    elif user_input == 'C':
        decorated = [(recipe.instructions, recipe) if recipe.instructions else print('Error! No instructions for recipe {}'.format(recipe)) for recipe in recipes]

    decorated.sort(key = lambda x: x[0])
    undecorated = [x[1] for x in decorated]
    for recipe in undecorated[::-1]:
        recipe.pretty_print()

# Main program, handles (almost) all user interaction
def main():
    # Decide if we're going to use allrecipes.com
    user_input = input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while not user_input == 'Y' and not user_input == 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        user_input = input('Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
    should_use_all_recipes = (user_input == 'Y')
    last_book = None

    while True:
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in ['S','O']:
            action = input('(S)earch/(O)rganize? ')
        if action[0].upper() == 'S':
            last_book = search(should_use_all_recipes)
            print("Found {size} matching recipes.".format(size=last_book.size()))
        elif last_book == None or last_book.size() == 0:
            print("Before you can organize some search results, try searching for something!")
        else:
            organize(last_book)
        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = input('Couldn\'t process. Another round? (Y/N) ').strip().upper()
        if (not (do_continue == 'Y')):
            break
    print('Have a nice life!')


if __name__ == '__main__':
    print('Welcome to the Recipe Book!')
    print('I hope you\'re hungry, since we have a lot of recipes to look through!')
    print('First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.')
    print('Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.')
    print('The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2')
    print('For example, "dinner +chicken -nuts".')
    print('After you search, we\'ll keep the results of the most recent search around.')
    print('You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.')
    input('Got all that? [Press ENTER to continue...] ')

    try:
        main()
    except:
        print('An unexpected error occured! Exiting.')
        raise
