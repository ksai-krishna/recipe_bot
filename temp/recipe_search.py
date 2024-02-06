from create_graph import create_recipe_graph
class RecipeSearch:
    def __init__(self, recipe_graph):
        self.recipe_graph = recipe_graph

    def find_recipes(self, available_ingredients, dish_type=None):  # Default value for dish_type is None
        
        possible_recipes = set()
        for ingredient_name in available_ingredients:
            if ingredient_name in self.recipe_graph.ingredients:
                ingredient_node = self.recipe_graph.ingredients[ingredient_name]
                for recipe_node in ingredient_node.recipes:
                    if dish_type is None or recipe_node.dish_type == dish_type or recipe_node.dish_type is None:  # Check if the dish type matches or is None
                        recipe_ingredients = {ingredient.name for ingredient in recipe_node.ingredients}
                        if recipe_ingredients.issubset(available_ingredients):
                            possible_recipes.add(recipe_node.name)
        return possible_recipes
class Recipe_output:
    def output(available_ingredients , dish_type=None):
        recipe_graph = create_recipe_graph()
        recipe_search = RecipeSearch(recipe_graph)          
        recipes = recipe_search.find_recipes(available_ingredients, dish_type)
        return recipes