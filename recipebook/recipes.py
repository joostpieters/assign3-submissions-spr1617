from recipe import RecipeBook

def word_lists(words):
    # Returns a tuple of keywords, exclude words, and include words filtered
    # by '+' and '-' characters.
    keywords = list(filter(lambda word: word and word[
                    0] not in ['+', '-'], words))
    excludes = list(filter(lambda word: word and word[0] == '-', words))
    includes = list(filter(lambda word: word and word[0] == '+', words))
    return keywords, excludes, includes


def print_instructions():
    # Prints instructions on how to use the recipe book to the console.
    print('Welcome to the Recipe Book!')
    print('I hope you\'re hungry, since we have a lot of recipes to look through!')
    print('First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.')
    print('Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.')
    print('The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2')
    print('For example, "dinner +chicken -nuts".')
    print('After you search, we\'ll keep the results of the most recent search around.')
    print('You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.')
    input('Got all that? [Press ENTER to continue...] ')


def organize_recipes(last_book):
    """ Organizes and displays recipes saved from the last search call by view, cooking time, ingredients,
    or complexity.
    """
    if last_book == None or last_book.size() == 0:
        print("Before you can organize some search results, try searching for something!")
    else:
        # note: complexity means number of instructions. some recipes will have
        # zero instructions
        user_input = input(
            "What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
        while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
            user_input = input(
                "That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
        if user_input == 'V':
            for i in range(last_book.size()):
                recipe = last_book.get_recipe_by_name(
                    list(last_book.get_recipe_names())[i])
                recipe.pretty_print()
        elif user_input == 'T':
            recipes = last_book.recipes.values()
            decorated = []
            for recipe in recipes:
                decorated.append(
                    (recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
            decorated.sort(key=lambda x: x[0])
            undecorated = [x[1] for x in decorated]
            for recipe in undecorated[::-1]:
                recipe.pretty_print()
        elif user_input == 'I':
            recipes = last_book.recipes.values()
            decorated = []
            for recipe in recipes:
                decorated.append((recipe.ingredients.size(), recipe))
            decorated.sort(key=lambda x: x[0])
            undecorated = [x[1] for x in decorated]
            for recipe in undecorated[::-1]:
                recipe.pretty_print()
        elif user_input == 'C':
            recipes = last_book.recipes.values()
            decorated = []
            for recipe in recipes:
                if recipe.instructions:
                    decorated.append((len(recipe.instructions), recipe))
                else:
                    print('Error! No instructions for recipe {}'.format(recipe))
            decorated.sort(key=lambda x: x[0])
            undecorated = [x[1] for x in decorated]
            for recipe in undecorated[::-1]:
                recipe.pretty_print()


def search_recipes():
    """ Searches recipes that include the keyword(s) in the description, include the
    include word(s) in the ingredients, and exclude the exclude word(s) from the ingredients.
    """
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords, excludes, includes = word_lists(words)
    if should_use_all_recipes():
        import fetcher
        recipes = fetcher.fetch_recipes(
            *keywords, includeIngredients=includes, excludeIngredients=excludes)
        return RecipeBook(recipes)
    else:
        good_recipes = []
        for recipeName in book.get_recipe_names():
            recipe = book.get_recipe_by_name(recipeName)
            okay_recipe = True
            keyword_list = [(word.lower() in recipe.descr.lower())
                            for word in keywords]
            include_list = [recipe.ingredients.contains_ingredient(
                include[1:]) for include in includes]
            exclude_list = [not recipe.ingredients.contains_ingredient(
                exclude[1:]) for exclude in excludes]
            okay_list = [all(keyword_list), all(
                include_list), all(exclude_list)]
            if all(okay_list):
                good_recipes.append(recipe)
        last_book = RecipeBook(good_recipes)
        print("Found {size} matching recipes.".format(size=last_book.size()))
        return last_book

# Main program, handles (almost) all user interaction
try:
    print_instructions()
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
        search = action[0].upper() == 'S'
        if search:
            last_book = search_recipes()
        else:  # Organize
            organize_recipes(last_book)
        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = input(
                'Couldn\'t process. Another round? (Y/N) ').strip().upper()
        if (do_continue != 'Y'):
            break

    print('Have a nice life!')
except:
    print('An unexpected error occured! Exiting.')
    raise
