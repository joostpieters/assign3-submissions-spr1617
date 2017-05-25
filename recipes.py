# Main program, handles (almost) all user interaction
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
        should_use_all_recipes = True
    if user_input == 'N':
        from console import *  # loads static cached book and such
        should_use_all_recipes = False

    last_book = None

    while True:
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in {'S', 'O'}:
            action = input('(S)earch/(O)rganize? ')

        if action[0].upper() == 'S':

            user_input = input('What would you like to search for? ').strip()
            # assume user enters a line like dinner +chicken -nuts
            words = user_input.split(' ')
            keywords = list(filter(lambda x: x[0] not in '+-', words))
            includes = list(filter(lambda x: x[0] == '+', words))
            excludes = list(filter(lambda x: x[0] == '-', words))

            if should_use_all_recipes:
                import fetcher
                recipes = fetcher.fetch_recipes(
                    *keywords, includeIngredients=includes, excludeIngredients=excludes)
                from recipe import RecipeBook
                last_book = RecipeBook(recipes)

            else:

                good_recipes = []
                for recipe in book.recipes.values():
                    okay_recipe = True
                    for word in keywords:
                        if word.lower() not in recipe.descr.lower():
                            okay_recipe = False
                    for include in includes:
                        if recipe.ingredients.contains_ingredient(
                                include) == False:
                            okay_recipe = False
                    for exclude in excludes:
                        if recipe.ingredients.contains_ingredient(exclude):
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
                while not user_input or user_input[0] not in {
                        'V', 'T', 'I', 'C'}:
                    user_input = input(
                        "That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

                if user_input == 'V':
                    for recipe in last_book.recipes.values():
                        recipe.pretty_print()

                elif user_input == 'T':
                    recipes = last_book.recipes.values()
                    decorated = [
                        (recipe.info.preparationTime.duration +
                         recipe.info.cookingTime.duration,
                         recipe) for recipe in recipes]
                    decorated.sort(key=lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif user_input == 'I':
                    recipes = last_book.recipes.values()
                    decorated = [(recipe.info.ingredients.size(), recipe)
                                 for recipe in recipes]
                    decorated.sort(key=lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif user_input == 'C':
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        if recipe.info.instructions:
                            decorated.append(
                                (len(recipe.info.instructions), recipe))
                        else:
                            print(
                                'Error! No instructions for recipe {}'.format(recipe))
                    decorated.sort(key=lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in {'Y', 'N'}:
            do_continue = input(
                'Couldn\'t process. Another round? (Y/N) ').strip().upper()

        if do_continue == 'N':
            break

    print('Have a nice life!')
except BaseException:
    print('An unexpected error occured! Exiting.')
    raise
