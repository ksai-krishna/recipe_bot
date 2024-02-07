import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation

class RecipeNode:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

class IngredientNode:
    def __init__(self, name):
        self.name = name
        self.recipes = []

class RecipeGraph:
    def __init__(self):
        self.ingredients = {}  # Ingredient name to IngredientNode mapping
        self.recipes = {}      # Recipe name to RecipeNode mapping

    def add_recipe(self, recipe_name, ingredients):
        recipe_node = RecipeNode(recipe_name)
        self.recipes[recipe_name] = recipe_node
        
        for ingredient_name in ingredients:
            if ingredient_name not in self.ingredients:
                ingredient_node = IngredientNode(ingredient_name)
                self.ingredients[ingredient_name] = ingredient_node
            else:
                ingredient_node = self.ingredients[ingredient_name]
            ingredient_node.recipes.append(recipe_node)
            recipe_node.ingredients.append(ingredient_node)

    def find_recipes(self, target_ingredients):
        recipes_found = set()
        queue = deque()

        # Enqueue recipes containing the target ingredients
        for ingredient_name in target_ingredients:
            if ingredient_name in self.ingredients:
                for recipe_node in self.ingredients[ingredient_name].recipes:
                    queue.append((recipe_node, [recipe_node]))

        # Perform BFS
        while queue:
            current_recipe, current_path = queue.popleft()
            recipes_found.add(current_recipe.name)

            # Enqueue recipes reachable from the current recipe
            for ingredient_node in current_recipe.ingredients:
                for recipe_node in ingredient_node.recipes:
                    if recipe_node.name not in recipes_found:
                        new_path = current_path + [recipe_node]
                        queue.append((recipe_node, new_path))
        
        return recipes_found

    def visualize_graph(self, save_path=None):
        G = nx.Graph()

        for ingredient_name, ingredient_node in self.ingredients.items():
            for recipe in ingredient_node.recipes:
                G.add_edge(ingredient_name, recipe.name)

        for recipe_name, recipe_node in self.recipes.items():
            for ingredient in recipe_node.ingredients:
                G.add_edge(recipe_name, ingredient.name)

        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=1500, font_size=10, font_weight='bold')
        
        if save_path:
            plt.savefig(save_path, format='jpg')
            print(f"Graph saved as {save_path}")
            plt.close()  # Close the plot window after saving
        
        if not save_path:
            plt.show()

    def generate_animation(self, target_ingredients, save_path=None):
        fig, ax = plt.subplots()
        G = nx.Graph()
        frames = []

        for ingredient_name, ingredient_node in self.ingredients.items():
            for recipe in ingredient_node.recipes:
                G.add_edge(ingredient_name, recipe.name)

        for recipe_name, recipe_node in self.recipes.items():
            for ingredient in recipe_node.ingredients:
                G.add_edge(recipe_name, ingredient.name)

        pos = nx.circular_layout(G)
        
        def update(frame):
            ax.clear()
            ax.set_title(f"Frame {frame+1}: BFS visiting {target_ingredients[frame]}")
            nx.draw(G, pos, with_labels=True, node_size=1500, font_size=10, font_weight='bold', ax=ax)
            
            # Highlight visited nodes in red
            if frame < len(target_ingredients):
                visited_node = target_ingredients[frame]
                nx.draw_networkx_nodes(G, pos, nodelist=[visited_node], node_color='r', node_size=1500, ax=ax)
        
        for ingredient in target_ingredients:
            frames.append(ingredient)
        
        ani = FuncAnimation(fig, update, frames=len(target_ingredients), interval=1000)
        
        if save_path:
            ani.save(save_path, writer='imagemagick', fps=1)
            print(f"Video saved as {save_path}")

def create_recipe_graph():
    recipe_graph = RecipeGraph()
    recipe_graph.add_recipe("Pasta2", ["Pasta", "Tomato Sauce", "Cheese"])
    recipe_graph.add_recipe("Pasta1", ["Pasta", "Cheese"])
    recipe_graph.add_recipe("raw pasta", ["Pasta"]) 
    # Add more recipes here as needed
    return recipe_graph

def main():
    recipe_graph = create_recipe_graph()
    
    available_ingredients = ["Pasta", "Tomato Sauce", "Cheese"]
    recipes_found = recipe_graph.find_recipes(available_ingredients)

    if recipes_found:
        print("Ingredients available:")
        print(available_ingredients)
        print("Recipes that can be made with the available ingredients:")
        for recipe_name in recipes_found:
            print(recipe_name)
    else:
        print("No recipes can be made with the available ingredients.")
    
    # Specify the path where you want to save the video
    #save_path = os.path.join(os.getcwd(), "recipe_animation.mp4")

    # Generate the animation and save it as a video
    #recipe_graph.generate_animation(available_ingredients, save_path)

if __name__ == "__main__":
    main()
