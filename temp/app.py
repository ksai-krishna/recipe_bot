from flask import Flask, render_template, request
import openai
import create_graph 
from recipe_search import RecipeSearch

# Set up OpenAI API key
openai.api_key = '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'

app = Flask(__name__)

# Create RecipeGraph instance
recipe_graph = create_graph.create_recipe_graph()

# Create RecipeSearch instance
recipe_search = RecipeSearch(recipe_graph)

def process_input(input_text):
    # Tokenize input text
    tokens = input_text.split(',')
    ingredients = set(tokens)
    return ingredients

def generate_recipes_text(recipes):
    recipe_list = ", ".join(recipes)
    return f"These are the result recipes: {recipe_list}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_text = request.form['input_text']
        ingredients = process_input(input_text)        
        prompt = "Find a good Indian recipe with these ingredients: " + ", ".join(ingredients)        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        result = generate_recipes_text(response.choices[0].text.strip())
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)