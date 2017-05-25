# Main program, handles (almost) all user interaction
from recipe import RecipeBook
import load_recipe  # loads static cached book and such
import fetcher

def getUserInput():
    user_input = input('What would you like to search for? ').strip()
        # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if not word:         continue
        if word[0] == '+':   includes.append(word[1:])
        elif word[0] == '-': excludes.append(word[1:])
        else:                keywords.append(word)
    return(keywords, includes, excludes)
def printIntro():
    print('''Welcome to the Recipe Book!
    I hope you\'re hungry, since we have a lot of recipes to look through!
    First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.
    Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.
    The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2
    For example, "dinner +chicken -nuts".
    After you search, we\'ll keep the results of the most recent search around.
    You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.''')

    input('Got all that? [Press ENTER to continue...] ')

def getSearch():
    action = input('(S)earch/(O)rganize? ')
    while not action or action[0].upper() not in ['S','O']:
        action = input('(S)earch/(O)rganize? ')
    return action[0].upper() == 'S'
def getRecipes():
        # Decide if we're going to use allrecipes.com
    user_input = input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while user_input != 'Y' and user_input != 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        user_input = input('Should we use allrecipes.com for recipes? Enter Y/N: ').strip().upper()
    if user_input == 'Y':
        book = {}
        should_use_all_recipes = True
    if user_input == 'N':
        book = load_recipe.get_local_recipe()
        should_use_all_recipes = False
    return (book, should_use_all_recipes)
def searchRecipes(keywords, includes, excludes, book):
    good_recipes = []
    for i in range(book.size()):
        recipe = book.get_recipe_by_name(list(book.get_recipe_names())[i] )
        okay_recipe = True
        if any (word.lower() not in recipe.descr.lower() for word in keywords) :
             continue
        for include in includes:
            if any(include in ingredient for ingredient in recipe.ingredientList):
                break
        for exclude in excludes:
            if any(exclude in ingredient for ingredient in recipe.ingredientList):
                okay_recipe = False
                break
        if okay_recipe:
            good_recipes.append(recipe)
    return good_recipes
def getContinue():
    do_continue = input('Another round (Y/N)? ').strip().upper()
    while not do_continue or do_continue[0] not in 'YN':
        do_continue = input('Couldn\'t process. Another round? (Y/N) ').strip().upper()
    return do_continue == 'Y'
def getOrganizeChoice() :
    # note: complexity means number of instructions. some recipes will have zero instructions
    user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
        user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    return user_input
def printAllRecipes(recipes):
    for recipe in recipes:
        recipe.pretty_print()

try:
    printIntro()
    (book, should_use_all_recipes) = getRecipes()
    last_book = None
    while True:
        search = getSearch()
        if search:
            (keywords,includes, excludes) = getUserInput()
            if should_use_all_recipes:
                recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)                
                last_book = RecipeBook(recipes)
            else:
                good_recipes = searchRecipes(keywords, includes, excludes, book)
                last_book = RecipeBook(good_recipes)
                print("Found {size} matching recipes.".format(size=last_book.size()))

        else:  # Organize
            if not last_book or last_book.size() == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                user_input = getOrganizeChoice()
                recipes = last_book.recipes.values()
                if user_input == 'V':
                    printAllRecipes(recipes)

                elif user_input == 'T':
                    decorated = sorted([(recipe.preparationTime.duration + recipe.cookingTime.duration, recipe) for recipe in recipes],  key = lambda x: x[0], reverse = True)
                    undecorated = [x[1] for x in decorated]
                    printAllRecipes(undecorated)

                elif user_input == 'I':
                    decorated = sorted([(len(recipe.ingredients), recipe) for recipe in recipes], key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    printAllRecipes(undecorated)

                elif user_input == 'C':
                    decorated = []
                    for recipe in recipes:
                        if recipe.instructions:
                            decorated.append((len(recipe.instructions), recipe))
                        else:
                            print('Error! No instructions for recipe {}'.format(recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    printAllRecipes(undecorated)


        
        do_continue = getContinue()
        if not do_continue:
            break

    print('Have a nice life!')
except:
    print('An unexpected error occured! Exiting.')
    raise