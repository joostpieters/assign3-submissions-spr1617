# Main program, handles (almost) all user interaction

from recipe import *
import fetcher
from recipe import RecipeBook
import json



def ask_for_filename(prompt="Filename?", default="recipes.json"):
    raw = default
    try:
        raw = input(prompt) or default
        # See, it"s easier to ask for forgiveness then permission
        open(raw, "r").read()  # See if they gave us a file we can open
    except:
        raise Exception("Bad filename!")
    finally:
        return raw

def main():
    print("Welcome to the Recipe Book! I hope you're hungry, since we have a lot of recipes to look through!",
          "First, tell us whether we should use a local cache of recipes, or if we should instead go to allrecipes.com to answer your queries.",
          "",
          sep = "\n\n")

    # Decide if we"re going to use allrecipes.com
    allrecipes_input = input("Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: ").strip().upper()
    while True:
        if allrecipes_input in {"Y", "N"}:
            break
        allrecipes_input = input("That wasn't either a Y or an N! Try again. Enter Y/N: ")

    local_copy = None
    if allrecipes_input == "N":
        filename_input = ask_for_filename("Where should we load the local recipes from (use recipes.json if you aren't sure)? ", default="recipes.json")
        file = open(filename_input, "r+")
        data = file.read()
        lines = data.split("\n")
        recipes = []
        for i in range(len(lines)):
            recipe = recipe_from_args(json.loads(lines[i]))
            recipes.append(recipe)
        local_copy = RecipeBook(recipes)
        file.close()


    print("",
        "There are two options: (S)earch through a book of recipes or (O)rganize your last book of recipes. In order to Organize, you must have Searched at least once before!",
        "To (S)earch for a given recipe: we use keywords, and inclusions / exclusions of ingredients. The format for such a query is 'keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2'. For example, 'dinner +chicken -nuts'.",
        "After you Search, we'll keep the results of the most recent search around.",
        "You can then (O)rganize your last book as follows: by preparation time, number of distinct ingredients, or number of instructions.",
        "Have fun!",
        "",
        sep = "\n\n")


    last_book = None

    while True:

        # Decide if we"re going to Search or Organize on this round
        search_input = input("Should we Search or Organize? Enter S/O: ").strip().upper()
        while True:
            if search_input in {"S", "O"}:
                break
            search_input = input("That wasn't either an S or an O! Try again. Enter S/O: ")

        # Search allrecipes.com
        if allrecipes_input == "Y" and search_input == "S":
            user_input = input("What would you like to search for? ").strip()
            # assume user enters a line like dinner +chicken -nuts
            words = user_input.split(" ")
            keywords = []
            includes = []
            excludes = []
            for word in words:
                if not word:         continue
                if word[0] == "+":   includes.append(word)
                elif word[0] == "-": excludes.append(word)
                else:                keywords.append(word)
            recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
            last_book = RecipeBook(recipes)



        # Search local copy
        elif allrecipes_input == "N" and search_input == "S":
            book = local_copy

            user_input = input("What would you like to search for? ").strip()
            # assume user enters a line like dinner +chicken -nuts
            words = user_input.split(" ")
            keywords = []
            includes = []
            excludes = []
            for word in words:
                if not word:         continue
                if word[0] == "+":   includes.append(word)
                elif word[0] == "-": excludes.append(word)
                else:                keywords.append(word)

            good_recipes = []
            for i in range(book.size()):
                recipe = book.get_recipe_by_name( list(book.get_recipe_names())[i] )
                okay_recipe = True
                for word in keywords:
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


        # Organize last book
        else:
            if last_book == None or last_book.size() == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                # note: complexity means number of instructions. some recipes will have zero instructions
                user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
                while not user_input or user_input[0] not in ("V", "T", "I", "C"):
                    user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

                if user_input == "V":
                    for i in range(last_book.size()):
                        recipe = last_book.get_recipe_by_name( list(last_book.get_recipe_names())[i] )
                        recipe.pretty_print()

                elif user_input == "T":
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        decorated.append((recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif user_input == "I":
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        decorated.append((recipe.ingredients.size(), recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

                elif user_input == "C":
                    recipes = last_book.recipes.values()
                    decorated = []
                    for recipe in recipes:
                        if recipe.instructions:
                            decorated.append((len(recipe.instructions), recipe))
                        else:
                            print("Error! No instructions for recipe {}".format(recipe))
                    decorated.sort(key = lambda x: x[0])
                    undecorated = [x[1] for x in decorated]
                    for recipe in undecorated[::-1]:
                        recipe.pretty_print()

        # Decide if we're going to do another round
        round_input = input("Should we do another round? Enter Y/N: ").strip().upper()
        while True:
            if round_input in {"Y", "N"}:
                break
            round_input = input("That wasn't either Y or N! Try again. Enter Y/N: ")


        if round_input == "N":
            break

    print("Hope you enjoyed the recipe!")

    # should_use_all_recipes = allrecipes_input == "Y"

    # if not should_use_all_recipes:
    #     filename_input = ask_for_filename("Where should we load the local recipes from (use recipes.json if you aren't sure)? ", default="recipes.json")
    #     file = open(filename_input, "r+")
    #     data = file.read()
    #     lines = data.split("\n")
    #     recipes = []
    #     for i in range(len(lines)):
    #         recipe = recipe_from_args(json.loads(lines[i]))
    #         recipes.append(recipe)
    #     book=RecipeBook(recipes)
    #     file.close()

    # print("Now, ask us to search for a given recipe. We know how to search by keyword, and by including and excluding ingredients.")
    # print("The format for such a query is 'keyword1 keyword2 +ingredientToInclude1 +ingredientToInclude2 -ingredientToExclude1 -ingredientToExclude2'")
    # print("For example, 'dinner +chicken -nuts'.")
    # print("After you search, we'll keep the results of the most recent search around.")
    # print("You can ask to see these results in an order sorted by preparation time, number of distinct ingredients, or number of instructions.")

    # last_book = None

    # while True:
    #     action = input("(S)earch/(O)rganize? ")
    #     while not action or action[0].upper() not in ["S","O"]:
    #         action = input("(S)earch/(O)rganize? ")
    #     search = action[0].upper() == "S"
    #     if search:
    #         if should_use_all_recipes:
    #             user_input = input("What would you like to search for? ").strip()
    #             # assume user enters a line like dinner +chicken -nuts
    #             words = user_input.split(" ")
    #             keywords = []
    #             includes = []
    #             excludes = []
    #             for word in words:
    #                 if not word:         continue
    #                 if word[0] == "+":   includes.append(word)
    #                 elif word[0] == "-": excludes.append(word)
    #                 else:                keywords.append(word)
    #             recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
    #             last_book = RecipeBook(recipes)

    #         else:
    #             user_input = input("What would you like to search for? ").strip()
    #             # assume user enters a line like dinner +chicken -nuts
    #             words = user_input.split(" ")
    #             keywords = []
    #             includes = []
    #             excludes = []
    #             for word in words:
    #                 if not word:         continue
    #                 if word[0] == "+":   includes.append(word)
    #                 elif word[0] == "-": excludes.append(word)
    #                 else:                keywords.append(word)

    #             good_recipes = []
    #             for i in range(book.size()):
    #                 recipe = book.get_recipe_by_name( list(book.get_recipe_names())[i] )
    #                 okay_recipe = True
    #                 for word in keywords:
    #                     if word.lower() not in recipe.descr.lower():
    #                         okay_recipe = False
    #                 for include in includes:
    #                     if recipe.ingredients.contains_ingredient(include) == False:
    #                         okay_recipe = False
    #                 for exclude in excludes:
    #                     if recipe.ingredients.contains_ingredient(exclude) == True:
    #                         okay_recipe = False
    #                 if okay_recipe:
    #                     good_recipes.append(recipe)

    #             last_book = RecipeBook(good_recipes)
    #             print("Found {size} matching recipes.".format(size=last_book.size()))

    #     else:  # Organize
    #         if last_book == None or last_book.size() == 0:
    #             print("Before you can organize some search results, try searching for something!")
    #         else:
    #             # note: complexity means number of instructions. some recipes will have zero instructions
    #             user_input = input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()
    #             while not user_input or user_input[0] not in ("V", "T", "I", "C"):
    #                 user_input = input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? ").strip().upper()

    #             if user_input == "V":
    #                 for i in range(last_book.size()):
    #                     recipe = last_book.get_recipe_by_name( list(last_book.get_recipe_names())[i] )
    #                     recipe.pretty_print()

    #             elif user_input == "T":
    #                 recipes = last_book.recipes.values()
    #                 decorated = []
    #                 for recipe in recipes:
    #                     decorated.append((recipe.preparationTime.duration + recipe.cookingTime.duration, recipe))
    #                 decorated.sort(key = lambda x: x[0])
    #                 undecorated = [x[1] for x in decorated]
    #                 for recipe in undecorated[::-1]:
    #                     recipe.pretty_print()

    #             elif user_input == "I":
    #                 recipes = last_book.recipes.values()
    #                 decorated = []
    #                 for recipe in recipes:
    #                     decorated.append((recipe.ingredients.size(), recipe))
    #                 decorated.sort(key = lambda x: x[0])
    #                 undecorated = [x[1] for x in decorated]
    #                 for recipe in undecorated[::-1]:
    #                     recipe.pretty_print()

    #             elif user_input == "C":
    #                 recipes = last_book.recipes.values()
    #                 decorated = []
    #                 for recipe in recipes:
    #                     if recipe.instructions:
    #                         decorated.append((len(recipe.instructions), recipe))
    #                     else:
    #                         print("Error! No instructions for recipe {}".format(recipe))
    #                 decorated.sort(key = lambda x: x[0])
    #                 undecorated = [x[1] for x in decorated]
    #                 for recipe in undecorated[::-1]:
    #                     recipe.pretty_print()


    #     do_continue = input("Another round (Y/N)? ").strip().upper()
    #     while not do_continue or do_continue[0] not in "YN":
    #         do_continue = input("Couldn't process. Another round? (Y/N) ").strip().upper()

    #     if (not (do_continue == "Y")):
    #         break

    # print("Have a nice life!")

if __name__ == "__main__":

    main()
