import json
import numpy as np

class Recipe(object):
    """Recipe object holds id containing of name and unique identifier string and set of ingredients"""
    def __init__(self, id, ingredients):
        self.id = id
        self.ingredients = np.unique(ingredients)
        self.similarity_score = 0

    def __str__(self):
        return '{0} \t\t {1}'.format(self.id, self.similarity_score)#str(self.id) + '\t\t' + str(self.similarity_score)

    def set_similarity_score(self, other):
        self.similarity_score = len(np.intersect1d(self.ingredients, other.ingredients))


class RecipeManager(object):
    # Load data from json file
    def get_recipes_from_file(self, directory):
        with open(directory) as data_file:
            recipes_data = json.load(data_file)
        
        # Store recipes as id - object dictionary
        self.recipes = { recipe['id']:  Recipe(recipe['id'], recipe['ingredients']) for recipe in recipes_data }

        print('Data loaded from file: {}'.format(directory))

    # Get list of ingredients in decreasing order of similarity with particular recipe
    def get_similar_recipes(self, selected_recipe_id):
        if(selected_recipe_id not in self.recipes):
            raise ValueError('id not found!')
    
        # Get the seleted recipe
        selected_recipe = self.recipes[selected_recipe_id]
    
        # Calculate similarity score for all recipes except the selected one
        similar_recipes = []#{recipe: recipe.get_similarity_score(selected_recipe) for id, recipe in recipes.items() if id != selected_recipe_id}
        for id, recipe in self.recipes.items():
            if(id != selected_recipe_id):
                recipe.set_similarity_score(selected_recipe)
                similar_recipes.append(recipe)
        
        # Sort by decreasing similarity score
        similar_recipes.sort(key=lambda r: r.similarity_score, reverse=True)
    
        return similar_recipes

# Test with user input
recipe_manager = RecipeManager()
recipe_manager.get_recipes_from_file('Data\\recipes.json')

while(True):
    try:
        recipe_id = input('Enter recipe id:\n')

        if(recipe_id == '0' or recipe_id.lower == 'exit'):
            break
        
        print( 'Similar recipes \t\t Similarity score' )
        print( '\n'.join(map(str, recipe_manager.get_similar_recipes(recipe_id))) )
        print( '\n')

    except ValueError as e:
        print('Error: {}'.format(e))