import create_graph
class RecipeSearch:
    def __init__(self, recipe_graph):
        self.recipe_graph = recipe_graph

    def find_recipes(self, available_ingredients):
        possible_recipes = set()
        for ingredient_name in available_ingredients:
            if ingredient_name in self.recipe_graph.ingredients:
                ingredient_node = self.recipe_graph.ingredients[ingredient_name]
                for recipe_node in ingredient_node.recipes:
                    recipe_ingredients = {ingredient.name for ingredient in recipe_node.ingredients}
                    if recipe_ingredients.issubset(available_ingredients):
                        possible_recipes.add(recipe_node.name)
        return possible_recipes

def main():
    
    recipe_graph = create_graph.create_recipe_graph()
    recipe_search = RecipeSearch(recipe_graph)

    available_ingredients = {"Basmati Rice", "Chicken", "Spices","Pizza Dough", "Tomato Sauce", "Cheese"}
    recipes = recipe_search.find_recipes(available_ingredients)

    if recipes:
        print("Ingredients available:")
        print(available_ingredients)
        print("Recipes that can be made with the available ingredients:")
        for recipe in recipes:
            print(recipe)
    else:
        print("No recipes can be made with the available ingredients.")

if __name__ == "__main__":
    main()
