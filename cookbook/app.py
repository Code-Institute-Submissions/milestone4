import os
from flask import Flask, render_template

app = Flask(__name__)

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