import os
import db_config
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_DBNAME"] = db_config.database_name
app.config["MONGO_URI"] = db_config.database_uri

mongo = PyMongo(app)

####################
# HELPER FUNCTIONS #
####################

#Get Recipe Titles
def get_recipe_titles():
  titles = dumps(mongo.db.recipes.find({}, {"_id": 0, "recipe_title": 1}))
  return titles
  
# Check Main Ingredients and Add if Needed
def check_main_ingredients(x):
  ingredient = x.lower() 
  if mongo.db.main_ingredients.find({"main_ingredient_name": ingredient}).count() == 0:
    mongo.db.main_ingredients.insert_one({"main_ingredient_name": ingredient})
    
# Allergens will be made into an array and stored in collection as main_allergens
# This will make it easier to display on frontend
def make_allergen_array(form_results):
  db_allergen_list = mongo.db.allergens.find({}, {"_id": 0, "main_allergen_name": 1})
  main_allergen_list = []
  for a in db_allergen_list:
    allergen = str(a["main_allergen_name"])
    if allergen in form_results:
      main_allergen_list.append(allergen)
      
  return main_allergen_list
  
###############################################################################




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
  titles=get_recipe_titles()
  allergens = mongo.db.allergens.find()
  main_ingredients = mongo.db.main_ingredients.find()
  return render_template('recipes/results.html', recipes=recipes, titles=titles, allergens=allergens, main_ingredients=main_ingredients)
  
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
  main_allergen_array = make_allergen_array(form_results)
  form_results["main_allergens"] = main_allergen_array
  recipes = mongo.db.recipes
  this_id = recipes.insert_one(form_results)
  recipe_id = this_id.inserted_id
  return redirect(url_for('view_recipe', recipe_id=recipe_id))

# The two function below render the edit recipe page and update the recipe in the database 
@app.route('/edit/<recipe_id>')
def edit_recipe(recipe_id):
  recipe_entry = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  titles = get_recipe_titles()
  allergens = mongo.db.allergens.find()
  return render_template('recipes/edit.html', recipe=recipe_entry, titles=titles, allergens=allergens)
  
  
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
  form_results = request.form.to_dict()
  check_main_ingredients(form_results["main_ingredient"])
  main_allergen_array = make_allergen_array(form_results)
  form_results["main_allergens"] = main_allergen_array
  
  mongo.db.recipes.update(
        {'_id': ObjectId(recipe_id)},
        form_results
        )
  return redirect(url_for('view_recipe', recipe_id=recipe_id))
  

# For the liking / upvoting system I decided to use oven mitts to fi the theme
# If the app had authentication I would limit the number of upvotes a user could give a recipe to one
# This would stop them repeatedly hiting the like button. I would also make it that they couldn't
# upvote their own recipe.
@app.route('/plus_one_score/<recipe_id>')
def plus_one_score(recipe_id):
  recipe_entry = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  score = int(recipe_entry["oven_mitt_score"])
  score += 1
  mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, { '$set': { "oven_mitt_score": str(score) }})
  return redirect(url_for('view_recipe', recipe_id=recipe_id))



###################
# SEARCH SECTION #
##################

# There are two search functions
# The first is to search for the recipe title
# The second is an advanced search, that filters out results
# To search for a recipe title, I created an index in mongodb
# This lets me search within the recipe_title strng
@app.route('/search_results', methods=["POST"])
def search_title():
  search_word = request.form.get("search_word")
  mongo.db.recipes.create_index([("recipe_title", pymongo.TEXT)])
  recipes = mongo.db.recipes.find({'$text': {'$search': search_word }})
  titles=get_recipe_titles()
  allergens = mongo.db.allergens.find()
  main_ingredients = mongo.db.main_ingredients.find()
  return render_template('recipes/results.html', recipes=recipes, titles=titles, allergens=allergens, main_ingredients=main_ingredients)
  


###############################################################################
 
@app.route('/stats')
def view_stats():
  return render_template('stats.html')

    
    
if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)