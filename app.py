from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
import create_graph 
from recipe_search import RecipeSearch

app = Flask(__name__)

# Create RecipeGraph instance
recipe_graph = create_graph.create_recipe_graph()

# Create RecipeSearch instance
recipe_search = RecipeSearch(recipe_graph)

def process_input(input_text):
    # Tokenize input text
    tokens = word_tokenize(input_text)
    ingredients = set()
    # Extract ingredients and dish type from the input text
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

def image_to_ingredients(image_file):
    # Here you should implement your logic to extract ingredients from the image
    # For now, let's assume it returns a set of ingredients
    ingredients = {"Basmati Rice", "Chicken", "chilly powder","cardmon","spices"}
    return ingredients

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    ingredients = set()  # Initialize ingredients to avoid UnboundLocalError
    if request.method == 'POST':
        if 'image_input' in request.files:
            # If an image file is uploaded
            image_file = request.files['image_input']
            ingredients = image_to_ingredients(image_file)
            
            if ingredients:
                result = suggest_recipe(ingredients)
                
        else:
            # If text input is provided
            input_text = request.form['input_text']
            ingredients, dish_type = process_input(input_text)
            if ingredients:
                result = suggest_recipe(ingredients, dish_type)
    return render_template('index.html', result=result, ingredients=ingredients)

def suggest_recipe(ingredients, dish_type=None):
    # Find recipes based on the provided ingredients and dish type
    if dish_type:
        recipes = recipe_search.find_recipes(ingredients, dish_type)
    else:
        recipes = recipe_search.find_recipes(ingredients)
    return recipes

if __name__ == '__main__':
    app.run(debug=True)
