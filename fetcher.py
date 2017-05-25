'''
File: fetcher.py
Edited by Samantha Robertson
SUNet ID: srobert4

This file defines the fetch_recipes function,
which takes search parameters and returns a list
of matching recipes fetched from the web using
requests and BeautifulSoup.

It also defines two helper functions for fetch_recipes:
make_search_request and get_recipe.
'''

from recipe import Recipe
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Python 3 Recipe Book Client for CS41'
}

RECIPE_SOURCE = 'http://allrecipes.com/search/results/'


def fetch_recipes(
    *keywords,
    includeIngredients=[],
    excludeIngredients=[],
        sort='ra'):
    '''
    This function takes search parameters:
    keywords, a list of included ingredients,
    a list of excluded ingredients, and a
    sort parameter, and returns a list of Recipe
    objects representing the recipes requested
    from the RECIPE_SOURCE that match
    the search parameters.
    '''

    print('Loading...')
    recipe_endpoints = make_search_request(
        *keywords,
        includeIngredients=includeIngredients,
        excludeIngredients=excludeIngredients,
        sort=sort)

    return [get_recipe(recipe_endpoint)
            for recipe_endpoint in recipe_endpoints if recipe_endpoint]


def make_search_request(
    *keywords,
    includeIngredients=[],
    excludeIngredients=[],
        sort='ra'):
    '''
    This function takes search parameters -
    keywords, included ingredients, excluded ingredients
    and a sort parameter.
    It makes a request to the URL defined in
    RECIPE_SOURCE with the given parameters and returns a list
    of matching recipe endpoints.
    '''

    # build request params in data
    data = {
        'sort': sort  # defaults to 'ra' == by rating
    }

    if keywords:
        data['wt'] = ' '.join(keywords)
    if includeIngredients:
        data['ingIncl'] = ','.join(includeIngredients)
    if excludeIngredients:
        data['ingExcl'] = ','.join(excludeIngredients)

    # make request
    response = requests.get(RECIPE_SOURCE, params=data, headers=HEADERS)
    if not response.ok:
        raise Exception('A very bad thing happened!')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get list of recipe endpoints
    recipes = []
    for tag in soup.find_all('a'):
        endpoint = tag.attrs.get('href')
        if endpoint and endpoint not in recipes and endpoint[:8] == '/recipe/':
            recipes.append(endpoint)

    print('Found {} recipes... extracting data'.format(len(recipes)))
    return recipes


def get_recipe(recipe_endpoint):
    """
    This function takes a recipe endpoint,
    requests the recipe from web via beautifulsoup
    and returns new recipe object
    e.g. /recipe/56927/delicious-ham-and-potato-soup/ => Recipe object
    """
    print('Loading {}'.format(recipe_endpoint))

    # Request recipe
    response = requests.get(
        'http://allrecipes.com' +
        recipe_endpoint,
        headers=HEADERS)
    if not response.ok:
        raise Exception("Another bad thing happened!")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Build args as needed to pass to Recipe constructor
    args = {}

    # Get title
    title = soup.find(attrs={'class': 'recipe-summary__h1'})
    if title:
        args['name'] = title.string.strip()

    # Get description
    description = soup.find(attrs={'class': 'submitter__description'})
    if description:
        args['description'] = description.string.strip(
            " \"\'")  # get rid of leading and trailing quotes

    # Get ingredient list
    ingredients = [
        tag.string.strip() for tag in soup.find_all(
            attrs={
                'class': 'recipe-ingred_txt'})
        if tag.attrs.get('itemprop') is not None
        and tag.attrs['itemprop'] == 'ingredients']

    # Convert ingredient list to ingredient string
    args['ingredients'] = '\n'.join(ingredients)

    # Get times
    times = list(map(lambda tag: tag.attrs['datetime'], soup.find_all('time')))
    # Fill missing times with None to ensure all are at least length 3 and avoid
    # index errors
    times += [None] * (3 - len(times))
    args['prepTime'], args['cookTime'] = times[:2]

    # Get instruction list
    args['instructions'] = [tag.string.strip() for tag in soup.find_all(
        attrs={'class': 'recipe-directions__list--item'}) if tag.string]

    # Return Recipe object
    return Recipe(args)
