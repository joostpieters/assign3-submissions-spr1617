#!/usr/bin/env python3 -tt
"""
File: recipes.py
-----------------------
Assignment 3: Stylize
Course: CS 41
Name: Grant Spellman
SUNet: gshamus
Handles user interaction with the Recipe book program. Allows the user to search
for recipes off of allrecipes.com, or from a local .json file of recipes. This
module manages the user's queries, filtering their search results, as well as
organizing them and displaying them. 


**************************************************************
ASSIGNMENT NOTE: I focused on editing recipes.py, recipe.py, and console.py. I made  
comments and minimal edits to fetcher.py, ingredients.py and duration.py. 
"""
import fetcher
import recipe
import json

## CONSTANTS
default_local_book = 'recipes.json'


def get_recipes_from_file():
    """ Creates a list of recipes from a local .json file"""
    
    filename = input('Where should we load the local recipes from (hit enter for default file recipes.json)? ')
    if filename == '':
        filename = default_local_book
    try:
        with open(filename,'r') as file:
            data = json.load(file) #load as .json file
    except:
        print("Bad filename!")
        raise

    recipes = [recipe.recipe_from_args(x) for x in data]
    return recipes

def build_recipebook(recipes):
    """ Build a dictionary to represent a recipebook 

    Using a list of recipe objects, map their names to recipe objects
    """
    book = {}
    for recipe in recipes:
        book[recipe.name] = recipe

    return book


def filter_recipes(recipe, keywords, includes, excludes):
    """ Filters a given recipe to see if it matches user criteria

    For a given recipe object "recipe", we check to see if the users keywords
    appear in its description, if their liked and ingredients are included, 
    and if their disliked ingredients are exclude 
    """
    for word in keywords:
        if word.lower() not in recipe.descr.lower():
            return False
    for include in includes:
        if recipe.ingredients.contains_ingredient(include) == False:
            return False
    for exclude in excludes:
        if recipe.ingredients.contains_ingredient(exclude) == True:
            return False
    
    return True


def categorize_search(words, keywords, includes, excludes):
    """ Categorizes the strings in the list "words"

    Assume user enters a line like dinner +chicken -nuts. Words prefaced with
    + are includes, - are excludes, and words without a preface are keywords.
    """
    for word in words:
        if not word:         continue
        if word[0] == '+':   includes.append(word)
        elif word[0] == '-': excludes.append(word)
        else:                keywords.append(word)    

def fix_input(str):
    # Adjust user input for response checking

    return str.strip().upper()

def should_use_website():
    """ Let's user decide to use allrecipes.com or local recipe source

    Returns true for using allrecipes.com and false for using recipe.
    """

    user_input = fix_input(input('Should we use allrecipes.com for recipes instead of a local copy of recipes? Enter Y/N: '))
    while not (user_input == 'Y' or user_input == 'N'):
        print('That was neither a Y nor an N! Try again.')
        user_input = fix_input(input('Should we use allrecipes.com for recipes? Enter Y/N: '))
    if user_input == 'Y':
        return True
    if user_input == 'N':
        return False

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
    use_website = should_use_website() 

    if not use_website:
        local_recipes = get_recipes_from_file()
        local_book = build_recipebook(local_recipes)

    last_book = None

    while True:
        action = input('(S)earch/(O)rganize? ')
        while not action or action[0].upper() not in ['S','O']:
            action = input('(S)earch/(O)rganize? ')

        search = action[0].upper() == 'S' # Decide to search or organize
        if search:
            keywords,includes,excludes = [],[],[]
            user_input = input('What would you like to search for? ')
            words = user_input.split()
            categorize_search(words, keywords,includes,excludes)

            if use_website:    
                recipes = fetcher.fetch_recipes(*keywords, includeIngredients=includes, excludeIngredients=excludes)
                last_book = build_recipebook(recipes)

            else:
                acceptable_recipes = []
                for recipe in local_book.values():
                    if filter_recipes(recipe, keywords, includes, excludes):
                        acceptable_recipes.append(recipe)

                last_book = build_recipebook(acceptable_recipes)
                print("Found {size} matching recipes.".format(size=len(last_book)))

        else:  # Organize
            if last_book == None or len(last_book) == 0:
                print("Before you can organize some search results, try searching for something!")
            else:
                # note: complexity means number of instructions. some recipes will have zero instructions
                user_input = fix_input(input("What do you want to do with your search results? \n(V)iew/Sort By Cooking (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? "))
                while not user_input or user_input[0] not in ('V', 'T', 'I', 'C'):
                    user_input = fix_input(input("That wasn't a legal choice. What do you want to do with your search results? \n(V)iew/Sort By (T)ime/Sort by Number of (I)ngredients/Sort by (C)omplexity? "))
    
                if user_input == 'V':
                    result = list(last_book.keys()) # Can display the results in any order 
            
                elif user_input == 'T':
                    result = sorted(last_book, key = lambda k: (last_book[k]).preparationTime.duration + (last_book[k]).cookingTime.duration)

                elif user_input == 'I':
                    result = sorted(last_book, key = lambda k: (last_book[k]).ingredients.size())

                elif user_input == 'C':
                    result = sorted(last_book, key = lambda k: len(last_book[k].instructions))
                
                for recipe_name in result[::-1]: # Reverse to display in order of least to greatest
                        last_book[recipe_name].pretty_print()

        do_continue = fix_input(input('Another round (Y/N)? '))
        while not do_continue or do_continue[0] not in 'YN':
            do_continue = fix_input(input('Couldn\'t process. Another round? (Y/N) '))

        if (not (do_continue == 'Y')):
            break

    print('Have a nice life!')
except:
    print('An unexpected error occured! Exiting.')
    raise