# Main program, handles (almost) all user interaction
from console import *  # loads static cached book and such
import fetcher
from recipe import RecipeBook



def printInstructions():
    print('Welcome to the Recipe Book!')
    print('I hope you\'re hungry, since we have a lot of recipes to look through!')
    print('First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.')
    print('Then, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.')
    print('The format for such a query is "keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2')
    print('For example, "dinner +chicken -nuts".')
    print('After you search, we\'ll keep the results of the most recent search around.')
    print('You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.')
    input('Got all that? [Press ENTER to continue...] ')


def getUserInput(output, tryAgain):
    user_input = input(output).strip().upper()
    if user_input[0] == 'Y':
        return True
    if user_input[0] == 'N':
        return False
    else:
        return getUserInput(tryAgain, tryAgain)




def canAppend(recipe, keywords, includes, excludes):

    anyFalse_1 = any(lambda word: word.lower not in recipe.descr.lower for word in keywords)
    anyFalse_2 = any(lambda include: not recipe.ingredients.contains_ingredient(include) for include in includes)
    anyFalse_3 = any(lambda exclude: recipe.ingredients.contains_ingredient(exclude) for exclude in excludes)
    if anyFalse_1 or anyFalse_2 or anyFalse_3:
        return False

    return True


def executeSearch(should_use_all_recipes):
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
    
    if should_use_all_recipes:
        recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
        last_book = RecipeBook(recipes)
            
    else:
        good_recipes = []
        for i in range(book.size()):
            recipe = book.get_recipe_by_name( list(book.get_recipe_names())[i] )
            if canAppend(recipe, keywords, includes, excludes):
                good_recipes.append(recipe)
            
        last_book = RecipeBook(good_recipes)
        print("Found {size} matching recipes.".format(size=last_book.size()))

    return last_book

def getOrganizingInstructions(output, tryAgain):
    user_input = input(output).strip().upper()
    if user_input and user_input[0] in ('V', 'T', 'I', 'C'):
        return user_input
    else:
        return getOrganizingInstructions(tryAgain, tryAgain)


if __name__ == '__main__':

    printInstructions()
    # Decide if we're going to use allrecipes.com
    should_use_all_recipes = getUserInput("Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ","That wasn\'t either a Y or an N! Try again.")
    
    last_book = None

    while True:
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in ['S','O']:
            action = input('(S)earch/(O)rganize? ')
        search = action[0].upper() == 'S'
        if search:
            last_book = executeSearch(should_use_all_recipes)
        
        else:  # Organize
            if last_book == None or last_book.size() == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                user_input = getOrganizingInstructions("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ", "That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity?")

                if user_input == 'V':
                    for i in range(last_book.size()):
                        recipe = last_book.get_recipe_by_name( list(last_book.get_recipe_names())[i] )
                        recipe.pretty_print()

                else:
                    for recipe in recipes:
                        if user_input == 'T':
                            instructions = recipe.preparationTime.duration + recipe.cookingTime.duration
                        elif user_input == 'I':
                            instructions = recipe.ingredients.size()
                        elif user_input == 'C':
                            if recipe.instructions:
                                instructions = len(recipe.instructions)
                            else:
                                print('Error! No instructions for recipe {}'.format(recipe))
                                continue

                        decorated.append((instructions, recipe))

                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()



        if getUserInput("Another round (Y/N)?", "Couldn\'t process. Another round? (Y/N)") == False:
            break


    print('Have a nice life!')


