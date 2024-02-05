#import nltk
from nltk.tokenize import word_tokenize
import create_graph 
from recipe_search import RecipeSearch,Recipe_output

# Initialize NLTK
#nltk.download('punkt')

# Create RecipeGraph instance
recipe_graph = create_graph.create_recipe_graph()
# Add recipes to the graph (you can add your own recipes here)

# Create RecipeSearch instance
recipe_search = RecipeSearch(recipe_graph)

def process_input(input_text):
    # Tokenize input text
    tokens = word_tokenize(input_text)
    # Extract ingredients from the input text
    ingredients = set()
    for word in tokens:
        if word.isalpha():  # Check if the word contains only alphabetic characters
            ingredients.add(word.title())  # Add the ingredient to the set of ingredients
    return ingredients

def suggest_recipe(ingredients):
    # Find recipes based on the provided ingredients
    
    recipes = Recipe_output.output(ingredients)
    print("recipes are ")
    return recipes

def main():
    print("Welcome to the Recipe Bot!")
    while True:
        user_input = input("Please enter the ingredients you have (separated by spaces), or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Thank you for using Recipe Bot. Goodbye!")
            break
        else:
            user_ingredients = process_input(user_input)
            if user_ingredients:
                print("Searching for recipes with ingredients:", user_ingredients)
                suggested_recipes = suggest_recipe(user_ingredients)
                if suggested_recipes:
                    print("Here are some suggested recipes:")
                    for recipe in suggested_recipes:
                        print(recipe)
                else:
                    print("No recipes found with the provided ingredients.")
            else:
                print("No valid ingredients provided. Please try again.")

if __name__ == "__main__":
    main()
