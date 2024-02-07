import networkx as nx
import matplotlib.pyplot as plt



class IngredientNode:
    def __init__(self, name):
        self.name = name
        self.recipes = []

class RecipeNode:
    def __init__(self, name):
        self.name = name
        self.ingredients = []


class RecipeGraph:
    def __init__(self):
        self.ingredients = {}  # Ingredient name to IngredientNode mapping
        self.recipes = {}      # Recipe name to RecipeNode mapping

    def add_recipe(self, recipe_name, ingredients, dish_type=None):  # Modified to accept dish_type
        recipe_node = RecipeNode(recipe_name)
        recipe_node.dish_type = dish_type  # Set the dish_type attribute
        self.recipes[recipe_name] = recipe_node
        
        for ingredient_name in ingredients:
            if ingredient_name not in self.ingredients:
                ingredient_node = IngredientNode(ingredient_name)
                self.ingredients[ingredient_name] = ingredient_node
            else:
                ingredient_node = self.ingredients[ingredient_name]
            ingredient_node.recipes.append(recipe_node)
            recipe_node.ingredients.append(ingredient_node)

def create_recipe_graph():
    recipe_graph = RecipeGraph()    
    recipe_graph.add_recipe("Pasta without sauce", ["Pasta", "Tomato Sauce"], dish_type="lunch food")
    recipe_graph.add_recipe("Raw Pasta", ["Pasta"], dish_type="lunch food")
    recipe_graph.add_recipe("Pasta", ["Pasta", "Tomato Sauce", "Cheese"], dish_type="lunch food")
    recipe_graph.add_recipe("Butter Chicken", ["Chicken", "Butter", "Tomato", "Cream", "Spices"], dish_type="dinner food")
    return recipe_graph 




class RecipeGraphVisualizer:
    def __init__(self, recipe_graph):
        self.recipe_graph = recipe_graph
        self.G = nx.Graph()

    def add_nodes(self):
        for ingredient_name, ingredient_node in self.recipe_graph.ingredients.items():
            self.G.add_node(ingredient_name, type='ingredient')

        for recipe_name, recipe_node in self.recipe_graph.recipes.items():
            self.G.add_node(recipe_name, type='recipe')

    def add_edges(self):
        for recipe_name, recipe_node in self.recipe_graph.recipes.items():
            for ingredient_node in recipe_node.ingredients:
                self.G.add_edge(recipe_name, ingredient_node.name)

    def visualize_graph(self):
        self.add_nodes()
        self.add_edges()
        pos = nx.spring_layout(self.G)  # Layout for the graph

        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=700)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)

    def save_as_image(self, filename):
        plt.savefig(filename, format="PNG")
        plt.close()

# Usage
recipe_graph = create_recipe_graph()
visualizer = RecipeGraphVisualizer(recipe_graph)
visualizer.visualize_graph()
visualizer.save_as_image("recipe_graph.png")
