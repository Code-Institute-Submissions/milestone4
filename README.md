Phil Surgenor - Milestone Project 4
===

<br>

## Data Centric Development
[visit the project website here](https://ficoea-cookbook.herokuapp.com/)

For this project, I had to create an online cookbook.

I called my application FiCoEa - Find it, Cook it, Eat it!

Below is a list of features that make up the application.



1 - Homepage:

            - Two Call to action buttons; View Recipes and Add recipe.
            - Three recipe cards are displayed,
              these are the three most popular recipes
            
2 - Recipes page:

            - This page displays all the recipes in card form.
            - The recipes are ordered again by popularity
            - There is a call to action button to add a recipe.
            - To make is easy to find the recipe you want,
              there are two options.
              
              The first is to search by recipe title. It searches
              all the recipe titles for matching words or phrases.
              There is also an autocomplete function to help with
              your search.
              
              The second option is to use the advanced search.
              By clicking the advanced search link, a modal appears
              form the bottom, with a range of search options,
              to help filter the results, this includes filtering out
              recipes with allergens, and finding vegetarian only
              dishes.

3 - Recipe Entry page

            - This is where the detailed version of the recipe
              is displayed.
            - The page is split into two sections, a side panel,
              and a main section.
              
              The side panel displays important infomation about
              the recipe. Including prep and cook times, allergens,
              who submitted it, and the oven mitt score.
              
              The oven mitt score is the 'likes' a recipe can get. If you
              like the recipe you can hit the +1 button near the bottom.
              
              The main section displays the recipe title, ingredients,
              and method for making the dish.
              
              Below the +1 button there is a link to edit the recipe.
              
            
4 - Add recipe page:

            - This page consists of mainly of a form for adding a recipe.
              
              There is some form validation, including the function to 
              stop a user from entering the same recipe title as someone else.
            

5 - Edit recipe page

            - Very similar to the add recipe page. The form fields are already
              filled where data has been entered before.
            
6 - Admin Section

            - This page would be locked to users who aren't admin if user
              authentication was bening used.
            - It is similar to the layout of the recipe entry page.
              
              In the side bar, the total amount of recipes are displayed
              along with total amount of vegetarian recipes.
              The most popular recipe is also displayed, with options to
              view or edit it.
              
              The main area display three clickable charts and a list of all
              the recipes in alphabetical order. These are an accordion,
              you can see the description by clicking on it.
              
              There are also two button, to edit or delete the recipe.
              A modal pops up to confirm you want to delete the recipe.
              

<br>

## UX

The user experience design for this type of application had to be had to be very well executed. The journey the user was put on, wether to add a recipe, search for one or view one in detail had to be well thought out, and make sense to the user, causing little to no friction.

I started out by mapping a typical users journey, from landing on the site to adding, editing and deleting recipes. I thought about what attributes of the recipe the user would like to see in the samll recipe cards, before going to the detailed view, how they would search for a recipe and what details of the recipe needed to be shown.

Once I had this information, I created wireframes to get an idea of how the pages would be laid out, but also how each step in the journey would connect to each other. You can see a PDF of the wireframes in the wireframes folder.

Once I had an understanding of how the site would look I designed a database schema (PDF in wireframs folder). Over the course of the build, the database schmea changed slightly to fit the needs of the site.

When it came to the advanced search section I had to add certain keys to make it function properly. These are detailed in the app.py file comments.


Overall I think the app fulfills its purpose in a simple and straightforward manner.

<br>

## Technologies

#### Main Build
 - Balsamiq Mockups
 - HTML 5
 - CSS 3
 - Materialize
 - Javascript / jQuery
 - Python & Flask
 - Mongo DB (Mlab)
 
I aslo used a JS library called MatchHeight.js to make the recipe cards be the same height.

#### Data Visualisation
  - Crossfilter.js
  - D3.js
  - DC.js
  - queue.js

<br>


## Testing


### Frontend Testing

After I had set the flask app up, I aded a simple view for the index page with hello world, to test the app was working properly.

I then set about building the template files for all the pages. I used Materialize to help with layout and styles. Once I had built the website with dummy content I tested it on various browsers and devices to make sure it was compatible. I checked the validation on the forms by manually filling them in, and checked every link to make sure they were pointing to the correct place.

<br>

### Testing the Database

I set up a mongoDB database in Mlab and tested the connection using the the command line terminal. I was able to use it within my app. I created a **test.html** file that I could use to render to and test variables etc quickly, once I knew it worked I could place it in the view I needed to.

Setting up the advanced search view took a bit of time, I needed to go back and fourth between my template and the app.py file taing each search criteria at a time making sure it give me the results I needed. I found I had to add additional keys to the database that could be put into a dictionary and queried.

I feel there is probably an easier way to get the information I needed, but after some research I couldn't find an easier way.


<br>

### Adding and Editing a Recipe

I now needed to test the editing and adding functionality of the app with the database. For this I thought it better user experience if the recipe name couldn't be repeated. To do this a queried the titles form the database, used json dumps to create a json list. This was sent to the frontend where I used jquery to vaidate the form and disable the edit/add button it the title was already in use. I used console.log to make sure I was getting the recipe titles in the correct format, and manualy tested the form field. 

Once I added or edited a recipe, I checked the database in M Lab to make sure everything was correct.


<br>

### Deleting a Recipe

After adding the delete view and front end button, I added some dummy recipes and after testing the deleting, I realised as the edit and delete buttons were quite close, a user might accidently delete a recipe. To stop this from hppening, I added a confirm delete modal, that pops up to ask the user if they are shure they want to delete the recipe.

<br>

### Oven Mitt Scoring ('likes') Test

On the frontend, I had a button linked to a view, that took the recipe_id and added 1 to oven_mitt_score. This was a simple test, as when I clicked the button I the view added one to the score and then redirected me to the same page. This worked without a problem 

<br>

### Data Visualisation Tests

Once I had built the functions to show the data in the charts, I was able to go to the frontend and ched that they displayed properly. I clicked on the various categories to check that they filtered the data properly.

I added and deleted recipes to check that the chats were updating properly. Everything worked as it should.

<br>

### Deployment
There are a number of steps that needed to be taken to deploy the web app.

The first step was to make sure all the files were in the correct folder structure. I created a requirements.txt file using the terminal. As this app is deployed to Heroku I needed to include a Procfile.

So that I could add the app.py file to Git Hub,  took out the database login credentials out of app.py and put them into another file called **db_config.py**, this file was then added to .gitignore and only uploaded to Heroku. I also changed debug mode to false before deploying to Heroku. You can see a sample db config file in the files above called **sample_db_config.py**

When all the files were uploaded to Heroku, I had to start a dyno. The last step was to add two config variables, one for PORT and one For IP.

I then went to the url of the app: [visit the project website here](https://ficoea-cookbook.herokuapp.com/) to test it. After testing all the functionality and links I was happy the site was working as it should.


<br>

### Credits
The photos are free stock images from: [pexels.com](https://pexels.com) and the recipes are taken from [The BBC Website](https://bbc.co.uk/food/)