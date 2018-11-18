import os
import db_config
from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = db_config.database_name
app.config["MONGO_URI"] = db_config.database_uri

mongo = PyMongo(app)


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
  
@app.route('/add-recipe')
def add_recipe():
  return render_template('recipes/add.html')
  
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