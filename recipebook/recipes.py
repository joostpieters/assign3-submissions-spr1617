import fetcher
from recipe import RecipeBook


# Main program, handles (almost) all user interaction
print('Welcome to the Recipe Book!')
print('I hope you\'re hungry,',
      'since we have a lot of recipes to look through!')
print('First, tell us whether we should use a local cache of recipes,',
      'or if we should instead go to allrecipes.com to answer your queries.')
print('Then, ask us to search for a given recipe. We know how',
      'to search by keyword, and by including and excluding ingredients.')
print('The format for such a query is "keyword1 keyword2',
      '+ingredientToInclude1 +ingredientToInclude2 ',
      '-ingredientToExclude1 -ingredientToExclude2')
print('For example, "dinner +chicken -nuts".')
print('After you search, we\'ll keep the',
      ' results of the most recent search around.')
print('You can ask to see these results in an order sorted by',
      'preparation time, number of distinct',
      ' ingredients, or number of instructions.')
input('Got all that? [Press ENTER to continue...] ')


# Decide if we're going to use allrecipes.com
request = ('Should we use allrecipes.com for recipes '
           'instead of a local copy of recipes? Enter Y/N: ')
user_input = input(
    request).strip().upper()
while not user_input == 'Y' and not user_input == 'N':
    print('That wasn\'t either a Y or an N! Try again.')
    user_input = input(request).strip().upper()
should_use_all_recipes = False
if user_input == 'Y':
    should_use_all_recipes = True
if user_input == 'N':
    from askfilename import book
    should_use_all_recipes = False

last_book = None


def create_keyword_lists(words):
    keywords, includes, excludes = [], [], []
    for word in words:
        # checks for blank words
        if not word:
            continue
        if word[0] == '+':
            includes.append(word)
        elif word[0] == '-':
            excludes.append(word)
        else:
            keywords.append(word)
    return keywords, includes, excludes


def search_recipes():
    user_input = input('What would you like to search for? ').strip()
    # assume user enters a line like dinner +chicken -nuts
    words = user_input.split(' ')
    keywords, includes, excludes = create_keyword_lists(words)
    if should_use_all_recipes:
        recipes = fetcher.fetch_recipes(
            *keywords,
            includeIngredients=includes,
            excludeIngredients=excludes)
        last_book = RecipeBook(recipes)
    else:
        good_recipes = []
        for recipename in book.get_recipe_names():
            recipe = book.get_recipe_by_name(recipename)
            okay_recipe = True
            for word in keywords:
                if word.lower() not in recipe.descr.lower():
                    okay_recipe = False
            for include in includes:
                if not recipe.ingredients.contains_ingredient(include):
                    okay_recipe = False
            for exclude in excludes:
                if recipe.ingredients.contains_ingredient(exclude):
                    okay_recipe = False
            if okay_recipe:
                good_recipes.append(recipe)

        last_book = RecipeBook(good_recipes)
        print("Found {} matching recipes.".format(last_book.size()))

    return last_book


def organize_recipes():
        # note: complexity means number of instructions. some recipes
        # will have zero instructions
        request = ("What do you want to do with your search results?"
                   " \n(V)iew/Sort By Cooking"
                   " (T)ime/Sort by Number of"
                   " (I)ngredients/Sort by (C)omplexity? ")
        user_input = input(request).strip().upper()
        while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
            new_req = "That wasn't a legal choice. " + request
            user_input = input(new_req).strip().upper()
        if user_input == 'V':
            for i in range(last_book.size()):
                recipe = last_book.get_recipe_by_name(
                    list(last_book.get_recipe_names())[i])
                recipe.pretty_print()
        else:
            decorated = []
            recipes = last_book.recipes.values()
            if user_input == 'T':
                decorated = [
                    (recipe.preparationTime.duration +
                     recipe.cookingTime.duration,
                     recipe) for recipe in recipes]
            elif user_input == 'I':
                # recipes = last_book.recipes.values()
                decorated = [(recipe.ingredients.size(), recipe)
                             for recipe in recipes]
            elif user_input == 'C':
                # recipes = last_book.recipes.values()
                for recipe in recipes:
                    if recipe.instructions:
                        decorated.append(
                            (len(recipe.instructions), recipe))
                    else:
                        print(
                            'Error! No instructions ',
                            'for recipe {}'.format(recipe))
            decorated.sort(key=lambda x: x[0])
            undecorated = [x[1] for x in decorated]
            for recipe in undecorated[::-1]:
                recipe.pretty_print()


while True:
    action = input('(S)earch/(O)rganize? ')
    while not action or action[0].upper() not in ['S', 'O']:
        action = input('(S)earch/(O)rganize? ')
    search = action[0].upper() == 'S'
    if search:
        last_book = search_recipes()
    else:  # Organize
        if not last_book:
            print(
                "Before you can organize some"
                " search results, try searching for something!")
        else:
            organize_recipes()
    do_continue = input('Another round (Y/N)? ').strip().upper()
    while not do_continue or do_continue[0] not in ('Y', 'N'):
        do_continue = input(
            'Couldn\'t process. Another round? (Y/N) ').strip().upper()
    if (not (do_continue == 'Y')):
        break
print('Have a nice life!')
