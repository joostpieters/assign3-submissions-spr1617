# Main program, handles (almost) all user interaction
from recipe import RecipeBook
import getFile  # loads static cached book and such

def main():
    # try:
        do_continue = True
        last_book = None
        firstRound = True
        while do_continue:
            if firstRound:
                initialize()
                use_website = get_recipe_source()
                if not use_website:
                    book = get_book()
                firstRound = False
            search = search_or_organize()
            if search:
                print_search_message()
                if use_website:
                    last_book = search_website()
                else:
                    last_book = search_file(book)
            else:  # if the user wants to organize
                organize(last_book)
            do_continue = reprompt()
        print('Have a nice life!')
    # except:
    #     print('An unexpected error occured! Exiting.')


def initialize():
    print('Welcome to the Recipe Book!')
    print('I hope you\'re hungry, since we have a lot ofrecipes to look through!')
    print()


def get_recipe_source():
    user_input = input('Do you want to use allrecipes.com for your search instead of a local copy of recipes? Enter Y/N: ').strip().upper()
    while user_input != 'Y' and user_input != 'N':
        print('That wasn\'t either a Y or an N! Try again.')
        print()
        user_input = input('Do you want to use allrecipes.com for your search or a local copy of recipes? Enter Y/N: ').strip().upper()
    if user_input == 'Y':
        return True
    else:
        return False


def search_or_organize():
    print()
    action = input('(S)earch/(O)rganize? ')
    while not action or action[0].upper() not in ['S', 'O']:
        action = input('(S)earch/(O)rganize? ')
    search = action[0].upper() == 'S'
    return search


def print_search_message():
    print()
    print('We know how to search by keyword, and by including and excluding ingredients.')
    print('For example, to search for a dinner with chicken and without nuts, you would enter: "dinner +chicken -nuts".')
    print()
    print('After you search, we\'ll keep the results of the most recent search around.')
    print('You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.')
    input('[Press ENTER to continue...] ')


def search_website():
    import fetcher
    print()
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if not word:
            continue
        if word[0] == '+':
            includes.append(word)
        elif word[0] == '-':
            excludes.append(word)
        else:
            keywords.append(word)
    recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
    
    last_book = RecipeBook(recipes)
    return last_book


def get_book():
    book = getFile.get_recipe_book()
    return book


def search_file(book):
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords = []
    includes = []
    excludes = []
    for word in words:
        if not word:
            continue
        if word[0] == '+':
            includes.append(word)
        elif word[0] == '-':
            excludes.append(word)
        else:
            keywords.append(word)

    good_recipes = []
    for i in range(book.size()):
        recipe = book.get_recipe_by_name(list(book.get_recipe_names())[i])
        acceptable_recipe = True
        for word in keywords:
            if word.lower() not in recipe.descr.lower():
                acceptable_recipe = False
        for include in includes:
            if recipe.ingredients.contains_ingredient(include) is False:
                acceptable_recipe = False
        for exclude in excludes:
            if recipe.ingredients.contains_ingredient(exclude) is True:
                acceptable_recipe = False
        if acceptable_recipe:
            good_recipes.append(recipe)

    last_book = RecipeBook(good_recipes)
    print("Found {size} matching recipes.".format(size=last_book.size()))
    return last_book


def organize(last_book):
    if last_book is None or last_book.size() == 0:
        print("Before you can organize some search results, try searching for something!")
    else:
        # note: complexity means number of instructions. some recipes will have zero instructions
        user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
        while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
            user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
        if user_input == 'V':
            view(last_book)
        elif user_input == 'T':
            sort_by_time(last_book)
        elif user_input == 'I':
            sort_by_num_ingredients(last_book)
        elif user_input == 'C':
            sort_by_complexity(last_book)


def view(last_book):
    for i in range(last_book.size()):
        recipe = last_book.get_recipe_by_name(list(last_book.get_recipe_names())[i])
        recipe.pretty_print()


def sort_by_time(last_book):
    recipes = last_book.recipes.values()
    decorated = []
    for recipe in recipes:
        decorated.append((recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
    decorated.sort(key = lambda x:  x[0])
    undecorated = [x[1] for x in decorated]
    for recipe in undecorated[::-1]:
        recipe.pretty_print()


def sort_by_num_ingredients(last_book):
    recipes = last_book.recipes.values()
    decorated = []
    for recipe in recipes:
        decorated.append((recipe.ingredients.size(), recipe))
    decorated.sort(key = lambda x: x[0])
    undecorated = [x[1] for x in decorated]
    for recipe in undecorated[::-1]:
        recipe.pretty_print()


def sort_by_complexity(last_book):
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


def reprompt():
    anotherRound = input('Another round (Y/N)? ').strip().upper()
    while not anotherRound or anotherRound[0] not in 'YN':
        anotherRound = input('Couldn\'t process. Another round? (Y/N) ').strip().upper()
    if anotherRound == 'N':
        return False
    else:
        return True


if __name__ == '__main__':
    main()
