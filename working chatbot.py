from nltk.tokenize import word_tokenize
import create_graph 
from recipe_search import RecipeSearch, Recipe_output

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

        #Wheat Flour,Potato,Spices,Butter,breakfast

def suggest_recipe(ingredients, dish_type=None):
    # Find recipes based on the provided ingredients and dish type
    if dish_type:
        recipes = recipe_search.find_recipes(ingredients, dish_type)
    else:
        recipes = recipe_search.find_recipes(ingredients)
    return recipes

def main():
    print("Welcome to the Recipe Bot!")
    while True:
        user_input = input("Please enter the ingredients and optionally the dish type (separated by commas), or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Thank you for using Recipe Bot. Goodbye!")
            break
        else:
            user_ingredients, user_dish_type = process_input(user_input)
            if user_ingredients:
                print("Searching for recipes with ingredients:", user_ingredients)
                if user_dish_type:
                    print("Searching for", user_dish_type, "recipes.")
                suggested_recipes = suggest_recipe(user_ingredients, user_dish_type)
                if suggested_recipes:
                    print("Here are some suggested recipes:")
                    for recipe in suggested_recipes:
                        print(recipe)
                else:
                    print("No recipes found with the provided ingredients and dish type.")
            else:
                print("No valid ingredients provided. Please try again.")

if __name__ == "__main__":
    main()
