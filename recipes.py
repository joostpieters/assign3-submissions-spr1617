# Main program, handles (almost) all user interaction

# MAIN CHANGES THAT I WANT TO MAKE - not including all of them right now!
'''
1. Create a basic main program and divide all aspects into sub-functions for easy understanding and coding
2. Include a way for the user to quit the program whenever they want to - currently, it gets stuck in Y/N or S/O loop and closing the terminal is the only way!
3. I have tried to replace user_input variables with better names to improve understanding - can do more there
4. I have tried to simply some if loops and for loops - want to do more on all the loops
5. I don't understand decorated vs undecorated properly to make those changes yet! 
'''
try:
    print('Welcome to the Recipe Book!', 
          "I hope you're hungry, since we have a lot of recipes to look through!",
          "First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.", 
          "Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.",
          'The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2" ',
          'For example, "dinner +chicken -nuts".',
          "After you search, we'll keep the results of the most recent search around.",
          "You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.", 
           sep = "\n")
    input('Got all that? [Press ENTER to continue...] ')

    # Decide if we're going to use allrecipes.com
    allrecipes_or_not = input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while allrecipes_or_not not in ['Y','N']:
        print("That wasn't either a Y or an N! Try again.")
        allrecipes_or_not = input('Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
    if allrecipes_or_not == 'Y':
        def should_use_all_recipes(): return True
    else:
        from console import *  # loads static cached book and such
        def should_use_all_recipes(): return False

    last_book = None

    while 1:
        search_or_organize = input('(S)earch/(O)rganize? ')
        while not search_or_organize or search_or_organize[0].upper() not in ['S','O']:
            search_or_organize = input('(S)earch/(O)rganize? ')
        #search = search_or_organize[0].upper() == 'S'
        if search_or_organize[0].upper() == 'S': #search
            if should_use_all_recipes():
                import fetcher

                # REPLACE the following block of 11 lines with a function named understand_user_preferences that returns includes, excludes and keywords lists. 
                # Reuse the function in the next else part
                user_preferences = input('What would you like to search for? ').strip()
                # assume user enters a line like dinner +chicken -nuts
                words = user_preferences.split(' ')
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

            else:
                # REPLACE the following 11 lines with the function named understand_user_preferences - as mentioned above
                user_preferences = input('What would you like to search for? ').strip()
                # assume user enters a line like dinner +chicken -nuts
                words = user_preferences.split(' ')
                keywords = []
                includes = []
                excludes = []
                for word in words:
                    if not word:         continue
                    if word[0] == '+':   includes.append(word)
                    elif word[0] == '-': excludes.append(word)
                    else:                keywords.append(word)
                
                # DEFINE the following as a function to test for good recipes and call when needed - to keep the main program clean.
                # Have tried to reduce the number of independent for loops to nested loops. It can be improved further!    
                good_recipes = []
                for i in range(book.size()):
                    recipe = book.get_recipe_by_name( list(book.get_recipe_names())[i] )
                    okay_recipe = True
                    for word in keywords:
                        if word.lower() not in recipe.descr.lower():
                            okay_recipe = False
                            break
                        else:
                            for include in includes:
                                if not recipe.ingredients.contains_ingredient(include):
                                    okay_recipe = False
                                    break
                                else:
                                    for exclude in excludes:
                                        if recipe.ingredients.contains_ingredient(exclude):
                                            okay_recipe = False
                                            break
                    if okay_recipe:
                        good_recipes.append(recipe)

                last_book = RecipeBook(good_recipes)
                print("Found {size} matching recipes.".format(size=last_book.size()))

        else:  # Organize
            if last_book == None or last_book.size() == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                # note: complexity means number of instructions. some recipes will have zero instructions
                how_to_organize = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
                while not how_to_organize or how_to_organize[0] not in ('V', 'T', 'I', 'C'):
                    how_to_organize = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

                if how_to_organize == 'V':
                    for i in range(last_book.size()):
                        recipe = last_book.get_recipe_by_name( list(last_book.get_recipe_names())[i] )
                        recipe.pretty_print()

                elif how_to_organize == 'T':
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        decorated.append((recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif how_to_organize == 'I':
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        decorated.append((recipe.ingredients.size(), recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif how_to_organize == 'C':
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


        do_continue = input('Another round (Y/N)? ').strip().upper()
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = input("Couldn't process. Another round? (Y/N) ").strip().upper()

        if do_continue != 'Y':
            break

    print('Have a nice life!')
except:
    print('An unexpected error occured! Exiting.')
    raise
