import os
import db_config
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_DBNAME"] = db_config.database_name
app.config["MONGO_URI"] = db_config.database_uri

mongo = PyMongo(app)


# HELPER FUNCTIONS

#Get Recipe Titles
def get_recipe_titles():
  titles = dumps(mongo.db.recipes.find({}, {"_id": 0, "recipe_title": 1}))
  return titles
  
# Check Main Ingredients and Add if Needed
def check_main_ingredients(x):
  ingredient = x.lower() 
  if mongo.db.main_ingredients.find({"main_ingredient_name": ingredient}).count() == 0:
    mongo.db.main_ingredients.insert_one({"main_ingredient_name": ingredient})




# The homepage will render home.html template
# I decided to show the top three recipes by oven mitt score
# This lets the user, not only see the top three recipes, but also familiarises
# them with how the recipe cards are laid out.
@app.route('/')
def home():
  recipes = mongo.db.recipes.find()
  return render_template('home.html', recipes=recipes)
  
@app.route('/recipes')
def recipes():
  recipes = mongo.db.recipes.find()
  return render_template('recipes/results.html', recipes=recipes)
  
@app.route('/recipes/<recipe_id>')
def view_recipe(recipe_id):
  recipe_entry = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  return render_template('recipes/entry.html', recipe=recipe_entry)
  

# To Insert the recipe there are a few things to do before the data can be added to the collection
# Because of this I can't just use "recipes.insert_one(request.form.to_dict())"

# The recipe title must be unique, this will stop confusion and help with the search.
# It also means there is something to tell two recipes apart even if they are for the same dish.
# This happens on the client side.
@app.route('/add-recipe')
def add_recipe():
  titles = get_recipe_titles()
  allergens = mongo.db.allergens.find()
  return render_template('recipes/add.html', titles=titles, allergens=allergens)

# For the prep time and cook time, I couldn't just have a text input as ther are many ways to add time
# For example some users might just insert minutes, while others might use hours and minutes
# So that there is no confusion they will have to insert hours and minutes.

# I have added a field called 'main ingedient'. The will help with search and data visualisation
# Before Adding it to the collection I will check the main_ingredients collection to see if it is unique
# If it doesn't already appear in main_ingredients I will add it.

# To save the user time, instead of having to type a list of allergens, there will be  a pre-made list
# In another collection "allergens", there will be a list of the most common. These appear as checkboxes
# As allergic reactions can be very serious, I have inserted a text field for other allergens
# This will cover any I have missed.

# Adding the vegan friendly switch, means I can display clearly if the recipe is suitable for vegans.
# This will help with the overall User experience.
@app.route('/insert-recipe', methods=["POST"])
def insert_recipe():
  form_results = request.form.to_dict()
  check_main_ingredients(form_results["main_ingredient"])

  
  
  form_results["recipe_title"] = "new title"
  element = form_results
  
  recipes = mongo.db.recipes
  recipes.insert_one(request.form.to_dict())
  # recipe_id = this_id.inserted_id
  return render_template('test.html', element=element)
  # return redirect(url_for('view_recipe', recipe_id=recipe_id ))
  
@app.route('/edit')
def edit_recipe():
  return render_template('recipes/edit.html')
  
  
@app.route('/stats')
def view_stats():
  return render_template('stats.html')

    
    
if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)