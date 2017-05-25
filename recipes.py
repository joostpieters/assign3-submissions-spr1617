#Xinlan Emily Hu
#SUNet ID: xehu
#File: recipes.py
#Modified with style changes and pythonic simplifications.

# Main program, handles (almost) all user interaction


def parse_keywords(keywords, includes, excludes, requested_recipe):
    for word in requested_recipe:
        if not word:
            continue
        if word[0] == '+':
            includes.append(word.lower())
        elif word[0] == '-':
            excludes.append(word.lower())
        else:
            keywords.append(word.lower())

def get_request_type(user_input):
    if user_input == 'T': return 0
    elif user_input == 'I': return 1
    elif user_input == 'C': return 2

def print_request(recipes, request_type):
    decorated = []
    for recipe in recipes:
        if request_type == 2 and not recipe.instructions:
            print(
                'Error! No instructions for recipe {}'.format(recipe))
        else:
            argument = [(recipe.preparationTime.duration + recipe.cookingTime.duration), recipe.ingredients.size(), len(recipe.instructions)]
            decorated.append((argument[request_type], recipe))
    decorated.sort(key=lambda x: x[0])
    undecorated = [x[1] for x in decorated]
    for recipe in undecorated[::-1]:
        recipe.pretty_print()

try:
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
    user_input = input(
        'Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while not user_input == 'Y' and not user_input == 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        user_input = input(
            'Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
    if user_input == 'Y':
        def should_use_all_recipes(): return True
    if user_input == 'N':
        from console import *  # loads static cached book and such
        def should_use_all_recipes(): return False

    last_book = None

    while True:
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in ['S', 'O']:
            action = input('(S)earch/(O)rganize? ')
        if action[0].upper() == 'S':
            if should_use_all_recipes():
                import fetcher
                user_input = input(
                    'What would you like to search for? ').strip()
                # assume user enters a line like dinner +chicken -nuts
                requested_recipe = user_input.split(' ')
                keywords = []
                includes = []
                excludes = []
                parse_keywords(keywords, includes, excludes, requested_recipe)
                recipes = fetcher.fetch_recipes(
                    *keywords, includeIngredients=includes, excludeIngredients=excludes)
                from recipe import RecipeBook
                last_book = RecipeBook(recipes)

            else:
                user_input = input(
                    'What would you like to search for? ').strip()
                # assume user enters a line like dinner +chicken -nuts
                requested_recipe = user_input.split(' ')
                keywords = []
                includes = []
                excludes = []
                parse_keywords(keywords, includes, excludes, requested_recipe)

                good_recipes = []
                for i in range(book.size()):
                    recipe = book.get_recipe_by_name(
                        list(book.get_recipe_names())[i])
                    okay_recipe = True

                    if not ''.join(keywords) in str(recipe.descr.lower()) or not recipe.ingredients.contains_ingredient(''.join(includes)) or (excludes and recipe.ingredients.contains_ingredient(''.join(excludes))):
                       okay_recipe = False 

                    if okay_recipe:
                        good_recipes.append(recipe)

                last_book = RecipeBook(good_recipes)
                print(
                    "Found {size} matching recipes.".format(
                        size=last_book.size()))

        else:  # Organize
            if last_book is None or last_book.size() == 0:
                print(
                    "Before you can organize some search results, try searching for something!")
            else:
                # note: complexity means number of instructions. some recipes
                # will have zero instructions
                user_input = input(
                    "What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
                while not user_input or user_input[0] not in (
                        'V', 'T', 'I', 'C'):
                    user_input = input(
                        "That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

                if user_input == 'V':
                    for i in range(last_book.size()):
                        recipe = last_book.get_recipe_by_name(
                            list(last_book.get_recipe_names())[i])
                        recipe.pretty_print()

                elif user_input in ('T', 'I','C'):

                    # 0 for T, 1 for I, and 2 for C
                    request_type = get_request_type(user_input)

                    recipes = last_book.recipes.values()
                    print_request(recipes, request_type)

        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = input(
                'Couldn\'t process. Another round? (Y/N) ').strip().upper()

        if ((do_continue != 'Y')):
            break

    print('Have a nice life!')
except BaseException:
    print('An unexpected error occured! Exiting.')
    raise
