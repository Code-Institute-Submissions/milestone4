import os
import db_config
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = db_config.database_name
app.config["MONGO_URI"] = db_config.database_uri

@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/recipes')
def recipes():
  return render_template('recipes/results.html')
  
@app.route('/recipes/entry')
def view_recipe():
  return render_template('recipes/entry.html')
  
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