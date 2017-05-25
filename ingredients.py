
def getIngredient(ingredient_data):
    if not ingredient_data:
        return dict()
    if ingredient_data[0].isdigit():
        i = ingredient_data.find(" ")
        food_start = ingredient_data.find(" ", i + 1)
        return {"quantity": ingredient_data[:food_start], "food": ingredient_data[food_start + 1:]}
    else:
        return {"quantity" : "N/A" , "food": ingredient_data}

def getIngredientList(all_ingredient_data) :
    ingredients = []
    for line in all_ingredient_data.split('\n'):
        ingredients += [getIngredient(line)]
    return ingredients
