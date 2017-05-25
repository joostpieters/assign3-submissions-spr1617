
# Downloads recipes from the internet
# Downloads recipe information from allrecipes.com

# A sample search might look like
# http://allrecipes.com/search/results/?wt=dinner&ingIncl=chicken,lemon&ingExcl=nuts&sort=ra

# any link out of here that uses
import recipe
import requests
from ingredients import *
from bs4 import BeautifulSoup
from duration import Duration

HEADERS = {
    'User-Agent': 'Python 3 Recipe Book Client for CS41'
}


def fetch_recipes(
    *keywords,
    includeIngredients=[],
    excludeIngredients=[],
        sort='ra'):
    print('Loading...')
    recipe_endpoints = make_search_request(
        *keywords,
        includeIngredients=includeIngredients,
        excludeIngredients=excludeIngredients,
        sort=sort)
    recipes = list(
        filter(
            lambda x: x is not None, map(
                get_recipe, recipe_endpoints)))
    return recipes


def make_search_request(
    *keywords,
    includeIngredients=[],
    excludeIngredients=[],
        sort='ra'):
    data = {
        'sort': sort  # defaults to 'ra' == by rating
    }
    if keywords:
        data['wt'] = ' '.join(keywords)
    if includeIngredients != []:
        data['ingIncl'] = ','.join(includeIngredients)
    if len(excludeIngredients) > 0:
        data['ingExcl'] = ','.join(excludeIngredients)

    response = requests.get(
        'http://allrecipes.com/search/results/',
        params=data,
        headers=HEADERS)
    if not response.ok:
        raise Exception('A very bad thing happened!')
    soup = BeautifulSoup(response.content, 'html.parser')

    recipes = []
    for tag in soup.find_all('a'):  # All outgoing links
        if 'href' in tag.attrs:
            href = tag.attrs['href']
            if href[:8] == '/recipe/':
                if href not in recipes:
                    recipes.append(href)

    print('Found {} recipes... extracting data'.format(len(recipes)))
    # now we have like all of the recipes == the things that all recipes says
    # are recipes
    return recipes


def get_recipe(recipe_endpoint):
    # e.g. /recipe/56927/delicious-ham-and-potato-soup/ => Recipe object
    print('Loading {}'.format(recipe_endpoint))
    response = requests.get(
        'http://allrecipes.com' +
        recipe_endpoint,
        headers=HEADERS)
    if not response.ok:
        raise Exception("Another bad thing happened!")
    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find(attrs={'class': 'recipe-summary__h1'})
    title = None
    if title_tag is not None:
        title = title_tag.string.strip()

    description_tag = soup.find(attrs={'class': 'submitter__description'})
    description = None
    if description_tag is not None:
        description = description_tag.string.strip()[
            1:-1]  # get rid of leading and trailing quotes

    ingredients = []
    for tag in soup.find_all(attrs={'class': 'recipe-ingred_txt'}):
        if tag.attrs.get(
                'itemprop') is not None and tag.attrs['itemprop'] == 'ingredients':
            ingredients.append(tag.string.strip())

    single_line_ingredient_string = '\n'.join(ingredients)

    prepTime, cookTime, totalTime = None, None, None
    for tag in soup.find_all('time'):
        if prepTime is None:
            prepTime = tag.attrs['datetime']
            continue
        if cookTime is None:
            cookTime = tag.attrs['datetime']
            continue
        if totalTime is None:
            totalTime = tag.attrs['datetime']
            continue

    instructions = []
    for tag in soup.find_all(attrs={'class': 'recipe-directions__list--item'}):
        if tag.string and len(tag.string.strip()) > 0:
            instructions.append(tag.string.strip())

    return recipe.Recipe(
        title,
        Duration(cookTime),
        Duration(prepTime),
        description,
        None,
        IngredientList(single_line_ingredient_string),
        instructions,
        None)
