# Import dependencies
import scrape_mars
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo

# Create Flask app
app = Flask(__name__)

# Create connection to Mongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route for homepage
@app.route("/")
def home_page():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Create route for scrape
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_facts = scrape_mars.scrape()
    mars.update({}, mars_facts, upsert=True)
    return render_template("index.html", mars=mars)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)