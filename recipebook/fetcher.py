# Downloads recipes from the internet
# Downloads recipe information from allrecipes.com

# A sample search might look like
# http://allrecipes.com/search/results/?wt=dinner&ingIncl=chicken,lemon&ingExcl=nuts&sort=ra

# any link out of here that uses
import recipe
import requests
import ingredients
from bs4 import BeautifulSoup

# Eliminated magic number
RECIPE_IDX = 8

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
        includeIngredients, excludeIngredients, sort, *keywords)
    return [get_recipe(recipe_endpoint)
            for recipe_endpoint in recipe_endpoints if recipe is not None]


def append_data(includeIngredients, excludeIngredients, keywords, data):
    if keywords:
        data['wt'] = ' '.join(keywords)
    if includeIngredients:
        data['ingIncl'] = ','.join(includeIngredients)
    if excludeIngredients:
        data['ingExcl'] = ','.join(excludeIngredients)


def make_search_request(includeIngredients=[],
                        excludeIngredients=[], sort='ra', *keywords):
    data = {
        'sort': sort  # defaults to 'ra' == by rating
    }
    append_data(includeIngredients, excludeIngredients, keywords, data)
    response = requests.get('http://allrecipes.com/search/results/',
                            params=data, headers=HEADERS)
    if not response.ok:
        raise Exception('Could not read from allrecipes.com!')
    soup = BeautifulSoup(response.content, 'html.parser')

    recipes = []
    for tag in soup.find_all('a'):  # All outgoing links
        if 'href' in tag.attrs:
            href = tag.attrs['href']
            if href[:8] == '/recipe/' and href not in recipes:
                    recipes.append(href)

    print('Found {} recipes... extracting data'.format(len(recipes)))
    return recipes


def get_recipe(recipe_endpoint):
    # e.g. /recipe/56927/delicious-ham-and-potato-soup/ => Recipe object
    print('Loading {}'.format(recipe_endpoint))
    response = requests.get(
        'http://allrecipes.com' +
        recipe_endpoint,
        headers=HEADERS)
    if not response.ok:
        raise Exception("Error loading from allrecipes.com!")
    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag, description_tag = soup.find(
        attrs={'class': 'recipe-summary__h1'}), soup.find(
        attrs={'class': 'submitter__description'})
    title, description = None, None
    if title_tag:
        title = title_tag.string.strip()
    if description_tag:
        description = description_tag.string.strip()[
            1:-1]  # get rid of leading and trailing quotes

    ingredients = []
    for tag in soup.find_all(attrs={'class': 'recipe-ingred_txt'}):
        if tag.attrs.get(
                'itemprop') and tag.attrs['itemprop'] == 'ingredients':
            ingredients.append(tag.string.strip())

    single_line_ingredient_string = '\n'.join(ingredients)
    prepTime, cookTime, totalTime = None, None, None

    for tag in soup.find_all('time'):
        if not prepTime:
            prepTime = tag.attrs['datetime']
        elif not cookTime:
            cookTime = tag.attrs['datetime']
        elif not totalTime:
            totalTime = tag.attrs['datetime']
    rec_dir = soup.find_all(attrs={'class': 'recipe-directions__list--item'})
    instructions = [tag.string.strip() for tag in rec_dir if tag.string]
    return recipe.Recipe(
        title,
        cookTime,
        prepTime,
        description,
        None,
        single_line_ingredient_string,
        instructions,
        None)
