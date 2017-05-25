'''
File: recipes.py
Edited by Samantha Robertson
SUNet ID: srobert4

This file handles the main functionality of the recipes program.
When run as a script, the main function handles the loading of
a static or web recipe book, and then repeatedly prompts the user
to search the recipe book or organize the search results.
'''

from recipe import Recipe
import fetcher
import json


def ask_for_filename(prompt="Filename? ", default='recipes.json'):
    '''
    This function repeatedly prompts the user using the given prompt
    until they enter a valid filename, and returns this filename.
    If they do not enter a filename, the given default filename is
    returned.
    '''
    while True:
        try:
            raw = input(prompt) or default
            open(raw, 'r').read()
            break
        except BaseException:
            print('Bad filename try again...')

    return raw


def get_local_recipes():
    '''
    This function opens the given local filename
    and returns a RecipeBook object containing the
    recipes specified in the file.
    '''
    userInput = ask_for_filename(
        'Where should we load the local recipes from ' +
        '(Press ENTER to use recipes.json)? ')

    with open(userInput, 'r+') as f:
        data = f.read()

    lines = data.split('\n')

    # Use list comprehension here
    return [Recipe(json.loads(line)) for line in lines]
    # return RecipeBook(recipes)


def print_welcome():
    '''
    Prints the initial welcome message for the user
    '''
    print('Welcome to the Recipe Book!')
    print('I hope you\'re hungry, since we have ' +
          'a lot of recipes to look through!')
    print('First, tell us whether we should use a ' +
          'local cache of recipes, or if we should ' +
          'instead go to allrecipes.com to answer your queries.')
    print('Then, ask us to search for a given recipe. ' +
          'We know how to search by keyword, and by ' +
          'including and excluding ingredients.')
    print('The format for such a query is "keyword1 keyword2 ' +
          '+ingredientToInclude1 +ingredientToInclude2 ' +
          '-ingredientToExclude1 -ingredientToExclude2')
    print('For example, "dinner +chicken -nuts".')
    print('After you search, we\'ll keep the results ' +
          'of the most recent search around.')
    print('You can ask to see these results in an order ' +
          'sorted by preparation time, number of distinct ' +
          'ingredients, or number of instructions.')
    input('Got all that? [Press ENTER to continue...] ')


def get_recipe_source():
    '''
    Prompts the user to choose to use allrecipes.com for recipes or
    to use a local file. Repeatedly prompts user until valid YN input
    received.
    Returns True if the user wants to use allrecipes.com, else returns
    False.
    '''
    user_input = input(
        'Should we use allrecipes.com for recipes instead ' +
        'of a local copy of recipes? Enter Y/N: ').strip().upper()

    while not user_input == 'Y' and not user_input == 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        user_input = input(
            'Should we use allrecipes.com for recipes? ' +
            'Enter Y/N: ').strip().upper()

    return user_input == 'Y'


def search_book(book, should_use_all_recipes):
    '''
    This function prompts the user for search terms,
    then searches either the local recipebook, given as
    the first argument if the second
    argument passed is False, else allrecipes.com for
    recipes matching the search terms.

    Returns a RecipeBook object containing matching
    recipes.
    '''

    # Get search terms
    user_input = input('What would you like to search for? ').strip()
    # If user enters an invalid search string, the
    # search will return no recipes, but the program
    # will not crash, so good input is not asserted.

    # Sort words from search input into keywords, included ingredients
    # and excluded ingredients
    words = user_input.split(' ')
    keywords = list(filter(lambda word: word[0] not in '+-', words))
    includes = list(filter(lambda word: word[0] == '+', words))
    excludes = list(filter(lambda word: word[0] == '-', words))

    if should_use_all_recipes:
        # Fetch recipes from allrecipes.com
        good_recipes = fetcher.fetch_recipes(
            *keywords,
            includeIngredients=includes,
            excludeIngredients=excludes)

    else:
        # Use local RecipeBook passed as parameter
        good_recipes = list(
            filter(
                lambda recipe: recipe.good_recipe(
                    keywords,
                    includes,
                    excludes),
                book))

    print("Found {size} matching recipes.".format(size=len(good_recipes)))
    return good_recipes


def org_results(last_book, sort_value):
    '''
    This function takes a recipe book and a callback that
    returns the value by which to sort the recipes.
    It prints the recipes in sorted order in descending
    order by the value returned by sort_value
    '''
    decorated = [(sort_value(recipe), recipe)
                 for recipe in last_book if sort_value(recipe)]
    decorated.sort(key=lambda x: x[0])

    undecorated = [x[1] for x in decorated]
    for recipe in undecorated[::-1]:
        recipe.pretty_print()


def organize(last_book):
    '''
    This function takes a RecipeBook, prompts the user for
    input indicating how to organize the recipes, and prints
    the organized result.
    '''

    '''
    org_funcs is a map from user input values to lambda functions
    that retrieve the value from each recipe by which
    the recipes should be sorted.
    '''
    org_funcs = {
        'V': None,
        'T': lambda recipe: recipe.preparationTime.duration
        + recipe.cookingTime.duration,
        'I': lambda recipe: len(
            recipe.ingredients),
        'C': lambda recipe: len(
            recipe.instructions)}

    if not last_book:
        # No search results to organize
        print("Before you can organize some " +
              "search results, try searching for something!")
    else:
        # note: complexity means number of instructions. some recipes will have
        # zero instructions
        user_input = input(
            "What do you want to do with your search results? " +
            "\n(V)iew/Sort By Cooking (T)ime/Sort by Number of " +
            "(I)ngredients/Sort by (C)omplexity? ").strip().upper()
        while not user_input or user_input[0] not in 'VTIC':
            user_input = input(
                "That wasn't a legal choice. " +
                "What do you want to do with your search results? " +
                "\n(V)iew/Sort By (T)ime/Sort by Number of " +
                "(I)ngredients/Sort by (C)omplexity? ").strip().upper()

        sort_lambda = org_funcs[user_input]

        if not sort_lambda:
            # Print recipes in last_book without sorting
            for recipe in last_book:
                recipe.pretty_print()

        else:
            # Sort and print recipes
            org_results(last_book, sort_lambda)


if __name__ == '__main__':
    '''
    Main program runs recipes program. Prints
    welcome message, prompts for all user input
    and repeatedly searches and organizes recipes
    until user decides to quit.
    '''
    try:
        local_recipes = get_local_recipes()
        print_welcome()
        should_use_all_recipes = get_recipe_source()
        last_book = []  # Will hold last search results to organize

        # Repeatedly offers to Search or Organize until user exits
        while True:
            # Get action - Search or Organize
            action = input('(S)earch/(O)rganize? ')
            while not action or action[0].upper() not in 'SO':
                action = input('(S)earch/(O)rganize? ')
            search = action[0].upper() == 'S'

            # Perform action
            if search:
                # Set last_book to search results
                last_book = search_book(local_recipes, should_use_all_recipes)
            else:
                # Organize last_book and print organized
                # recipes
                organize(last_book)

            # Decide whether to repeat or quit
            do_continue = input('Another round (Y/N)? ').strip().upper()
            while not do_continue or do_continue[0] not in 'YN':
                do_continue = input(
                    'Couldn\'t process. Another round? (Y/N) ').strip().upper()

            # User has decided to exit
            if do_continue != 'Y':
                break

        print('Have a nice life!')

    except BaseException:
        print('An unexpected error occured! Exiting.')
        raise
