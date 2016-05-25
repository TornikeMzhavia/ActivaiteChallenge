import json

class Recipe(object):
    """Recipe object holds id containing of name and unique identifier string and set of ingredients"""
    def __init__(self, id, ingredients):
        self.id = id
        self.ingredients = ingredients
        self.similarity_score = 0

    def __str__(self):
        return str(self.id) + '\t' + str(self.similarity_score)

# Get list of ingredients in decreasing order of similarity with particular recipe
def get_similar_recipes(recipe_id):
    if(recipe_id not in recipes):
        raise ValueError('id not found!')

    # Get the seleted recipe
    selected_recipe = all_recipes[recipe_id]

    # Calculate similarity score for all recipes except selected one
    similar_recipes = []
    for id, recipe in recipes.items():
        if(id != recipe_id):
            recipe.similarity_score = len(selected_recipe.ingredients.intersection(recipe.ingredients))
            similar_recipes.append(recipe)
    
    # Sort by decreasing similarity score
    similar_recipes.sort(key=lambda r: r.similarity_score, reverse=True)

    return similar_recipes

# Load data from json
with open('Data\\recipes.json') as data_file:
    recipes_data = json.load(data_file)

# Store recipes as id - object dictionary
recipes = {}
for recipe in recipes_data:
    if(recipe['id'] not in recipes):
        recipes[recipe['id']] = Recipe(recipe['id'], set(recipe['ingredients']))

# Test with user input
while(True):
    try:
        recipe_id = input('Enter recipe id:\n')

        if(recipe_id == '0' or recipe_id.lower == 'exit'):
            break
        
        print('Similar recipes:')
        print('\n'.join((str(recipe) for recipe in get_similar_recipes(recipes, recipe_id))))
        print('\n')

    except ValueError as e:
        print('Error: {}'.format(e))