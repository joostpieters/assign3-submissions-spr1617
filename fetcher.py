''' File: fetcher.py
-----------------------------------------------------------
Downloads recipes and recipe information from allrecipes.com
A sample search might look like:
http://allrecipes.com/search/results/?wt=dinner&ingIncl=chicken,lemon&ingExcl=nuts&sort=ra
'''

import recipe
import requests
import ingredients
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Python 3 Recipe Book Client for CS41'
}

def fetch_recipes(*keywords, includeIngredients=[], excludeIngredients=[], sort='ra'):
    ''' 
    Makes a list of all the recipes the user is searching for via the get_recipe function 
    '''
    print('Loading...')
    recipe_endpoints = make_search_request(*keywords, includeIngredients=includeIngredients, 
                                            excludeIngredients=excludeIngredients, sort=sort)
    return [get_recipe(endpoint) for endpoint in recipe_endpoints]

def make_search_request(*keywords, includeIngredients=[], excludeIngredients=[], sort='ra'):
    '''
    Organizes the user's search string and turns it into a url to search and scrape.
    '''

    data = {
        'sort': sort  # defaults to 'ra' == by rating
    }
    if keywords:
        data['wt'] = ' '.join(keywords)
    if includeIngredients:
        data['ingIncl'] = ','.join(includeIngredients)
    if excludeIngredients:
        data['ingExcl'] = ','.join(excludeIngredients)

    response = requests.get('http://allrecipes.com/search/results/', params=data, headers=HEADERS)
    if not response.ok:
        raise Exception('Server response from allrecipes.com is not ok')
    soup = BeautifulSoup(response.content, 'html.parser')

    recipes = []
    for tag in soup.find_all('a'):  # All outgoing links
        if 'href' in tag.attrs:
            href = tag.attrs['href']
            if href[:8] == '/recipe/' and href not in recipes:
                recipes.append(href)

    print('Found {} recipes... extracting data'.format(len(recipes)))
    # now we have all the entries that we've parsed as recipes
    return recipes

def get_recipe(recipe_endpoint):
    # e.g. /recipe/56927/delicious-ham-and-potato-soup/ => Recipe object
    print('Loading {}'.format(recipe_endpoint))
    response = requests.get('http://allrecipes.com' + recipe_endpoint, headers=HEADERS)
    if not response.ok:
        raise Exception("An error occured retrieving a recipe ")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Recipe Name
    title_tag = soup.find(attrs={'class':'recipe-summary__h1'})
    title = None
    if title_tag:
        title = title_tag.string.strip()

    # Recipe description
    description_tag = soup.find(attrs={'class' : 'submitter__description'}  )
    description = None
    if description_tag:
        description = description_tag.string.strip()[1:-1]  # get rid of leading and trailing quotes

    # Recipe ingredients
    ingredients = []
    for tag in soup.find_all(attrs={'class' :'recipe-ingred_txt'}):
        if tag.attrs.get('itemprop') and tag.attrs['itemprop'] == 'ingredients':
            ingredients.append(tag.string.strip())

    single_line_ingredient_string = '\n'.join(ingredients)

    # Assumes that the prep and cook times will be found in this order 
    prepTime, cookTime = None, None
    for tag in soup.find_all('time'):
        if not prepTime:
            prepTime = tag.attrs['datetime']
            continue
        if not cookTime:
            cookTime = tag.attrs['datetime']
            continue

    # Recipe instructions, if they exist
    instructions = [tag.string.strip() for tag in 
                    soup.find_all(attrs={'class': 'recipe-directions__list--item'}) if tag.string]

    return recipe.Recipe(title, cookTime, prepTime, description, None, single_line_ingredient_string, instructions, None)