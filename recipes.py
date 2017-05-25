#use allrecipes.com to search for recipes 
def useAllRecipes():
    import fetcher # (JR) why not just import it above? 
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if not word:         continue
        if word[0] == '+':   includes.append(word)
        elif word[0] == '-': excludes.append(word)
        else:                keywords.append(word)
    recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
    from recipe import RecipeBook
    last_book = RecipeBook(recipes)
    return last_book


# search for recipes in json 
def useLocalCopy():
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if not word:         continue # (JR) what is the purpose of this line?
        if word[0] == '+':   includes.append(word)
        elif word[0] == '-': excludes.append(word)
        else:                keywords.append(word)

    good_recipes = []
    for i in range(book.size()):
        recipe = book.get_recipe_by_name(list(book.get_recipe_names())[i])
        okay_recipe = True # a way of checking if the recipe is valid 
        for word in keywords: # (JR): can iterate over all of these at the same time UPDATE: might not be able to, could be different sizes 
            if word.lower() not in recipe.descr.lower():
                okay_recipe = False
        for include in includes:
            if recipe.ingredients.contains_ingredient(include) == False:
                okay_recipe = False
        for exclude in excludes:
            if recipe.ingredients.contains_ingredient(exclude) == True:
                okay_recipe = False
        if okay_recipe:
            good_recipes.append(recipe)

    last_book = RecipeBook(good_recipes)
    print("Found {size} matching recipes.".format(size=last_book.size()))
    return last_book 


# handle what to do on (O)rganize depending on user action
def searchResultAction():
    # note: complexity means number of instructions. some recipes will have zero instructions
    user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
        user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

    if user_input == 'V':
        for i in range(last_book.size()):
            recipe = last_book.get_recipe_by_name( list(last_book.get_recipe_names())[i] )
            recipe.pretty_print()

    elif user_input == 'T':
        recipes = last_book.recipes.values()
        decorated = []
        for recipe in recipes:
            decorated.append((recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
        decorated.sort(key = lambda x: x[0])
        undecorated = [x[1] for x in decorated]
        for recipe in undecorated[::-1]:
            recipe.pretty_print()

    elif user_input == 'I':
        recipes = last_book.recipes.values()
        decorated = []
        for recipe in recipes:
            decorated.append((recipe.ingredients.size(), recipe))
        decorated.sort(key = lambda x: x[0])
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
        decorated.sort(key = lambda x: x[0])
        undecorated = [x[1] for x in decorated]
        for recipe in undecorated[::-1]:
            recipe.pretty_print()


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
    user_input = input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while not user_input == 'Y' and not user_input == 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        user_input = input('Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
    if user_input == 'Y':
        def should_use_all_recipes(): return True
    if user_input == 'N':
        from console import *  # loads static cached book and such
        def should_use_all_recipes(): return False

    last_book = None

    # handles the high-level function of the program
    while 1: # for the duration of the program
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in ['S','O']:
            action = input('(S)earch/(O)rganize? ')
        search = action[0].upper() == 'S' # a boolean telling if the action was S or not 
        if search: # if the user selected search 
            if should_use_all_recipes():
                last_book = useAllRecipes() 
            else:
                last_book = useLocalCopy()

        else:  # Organize (if the user selected organize) 
            if last_book == None or last_book.size() == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                searchResultAction()

        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = input('Couldn\'t process. Another round? (Y/N) ').strip().upper()

        if (not (do_continue == 'Y')):
            break

    print('Have a nice life!')
except:
    print('An unexpected error occured! Exiting.')
    raise