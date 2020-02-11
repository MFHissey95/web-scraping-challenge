## Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

## Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
chrome_browser = Browser("chrome", **executable_path, headless=False)

## Open the NASA website
NASA_url = "https://mars.nasa.gov/news/"
chrome_browser.visit(NASA_url)

## Read the NASA website
html = chrome_browser.html
soup = BeautifulSoup(html, "html.parser")

## Scrape the NASA website. Assign the text to variables.
title_find = soup.find('div', class_='content_title').find('a').text
paragraph_find = soup.find('div', class_='article_teaser_body').text

## Display most recent news title and paragraph
print(title_find)
print(paragraph_find)

## Visit the url for JPL Featured Space Image 
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path)
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)

## Use splinter to navigate the site and find the image url. ##
image_button = browser.find_by_id("full_image")
image_button.click()

## Find "More Info" Button and Click It
browser.is_element_present_by_text("more info", wait_time=1)
more_info = browser.find_link_by_partial_text("more info")
more_info.click()

## Parse Results HTML with BeautifulSoup
html = browser.html
image_soup = BeautifulSoup(html, "html.parser")

## Find the image url to the full size `.jpg` image
featured_image_url = image_soup.select_one("figure.lede a img").get("src")
featured_image_url

## Save a complete url string for this image
featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"
print(featured_image_url)

## NEXT STEPS ## - - Mars Weather ##

## Mars Weather Twitter Account
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)

## Parse Results HTML with BeautifulSoup
html = browser.html
marsweather_soup = BeautifulSoup(html, "html.parser")

## Scrape the latest Mars weather tweet from the page
## Save the tweet for the weather report
mars_tweet = marsweather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })

# Search Within Tweet for <p> Tag Containing Text
mars_weather = mars_tweet.find("p", "tweet-text").get_text()
print(mars_weather)

## NEXT STEPS ## - - Mars Facts ##

# Visit the Mars Facts page - use Pandas to scrape the table 
mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_facts_df)

mars_facts_df.columns=["Description", "Value"]
mars_facts_df.set_index("Description", inplace=True)
mars_facts_df

## NEXT STEPS ## - - Mars Hemispheres ##

## Visit the USGS Astrogeology site & scrape

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)

mars_hemisphere_URL = []

## Get a List of every hemisphere ##
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    ## Loop each element
    browser.find_by_css("a.product-item h3")[item].click()
    
    ## Save both the image url string for the full resolution hemisphere image, and the Hemisphere title 
    ## containing the hemisphere name
    sample_element = browser.find_link_by_text("Sample").first
    
    ## Get hemisphere image url
    hemisphere["img_url"] = sample_element["href"]
    
    ## Get hemisphere title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    ## Append the dictionary with image url and hemisphere title to list
    mars_hemisphere_URL.append(hemisphere)
    
    
    browser.back()

## Print the array hemisphere_image_urls ##
mars_hemisphere_URL