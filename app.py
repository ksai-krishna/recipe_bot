from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from recipe_search import RecipeSearch, Recipe_output
import create_graph

app = Flask(__name__)

# Create RecipeGraph instance
recipe_graph = create_graph.create_recipe_graph()

# Create RecipeSearch instance
recipe_search = RecipeSearch(recipe_graph)

def process_input(input_text):
    # Tokenize input text
    tokens = word_tokenize(input_text)
    # Extract ingredients and dish type from the input text
    ingredients = set()
    dish_type = None
    dishtypes = ['dinner food', 'snack', 'breakfast', 'sweet', 'beverage', 'lunch food', 'healthy']
    ingredient_buffer = ""
    for word in tokens:
        if word.lower() in dishtypes:
            dish_type = word.lower()
        elif word == ',':
            if ingredient_buffer:
                ingredients.add(ingredient_buffer.strip().title())
                ingredient_buffer = ""  # Clear ingredient buffer after adding ingredient
        else:
            ingredient_buffer += word + " "
    # Add the last ingredient if there's any remaining in the buffer
    if ingredient_buffer:
        ingredients.add(ingredient_buffer.strip().title())
    return ingredients, dish_type

def suggest_recipe(ingredients, dish_type=None):
    # Find recipes based on the provided ingredients and dish type
    if dish_type:
        recipes = recipe_search.find_recipes(ingredients, dish_type)
    else:
        recipes = recipe_search.find_recipes(ingredients)
    return recipes

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = None
    if request.method == 'POST':
        input_text = request.form['input_text']
        ingredients, dish_type = process_input(input_text)
        if ingredients:
            recipes = suggest_recipe(ingredients, dish_type)
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
