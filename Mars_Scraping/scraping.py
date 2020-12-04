# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriver
import pandas as pd
import datetime as dt
import time

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# ### Visit the NASA Mars News Site
def mars_news(browser):
    #Scrape Mars News
    #Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Convert the browser html to a soup object and then quit brower
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
     # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

 
# ### JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

     # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# ### Mars Weather
def mars_weather(browser):

    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)

    # Parse the data
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    try: 

        # Scrape the Daily Weather Report table
        weather_table = weather_soup.find('table', class_='mb_table')

    except AttributeError:
        return None

    return weather_table.prettify()    


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
def hemisphere_image_urls(brower):
    try:
        # 1. Use browser to visit the URL 
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')

        base_url = 'https://astrogeology.usgs.gov'

        hemi_section = hemisphere_soup.find_all('div', class_='item')
        for hemi in hemi_section:
            hemisphere = {}
            hemi_title = hemi.find('h3').get_text()
            thumbnail = hemi.find('a', class_='itemLink product-item').get('href')
            browser.visit(base_url + thumbnail)
            html2 = browser.html
            hemi_soup2 = soup(html2, 'html.parser')
            hemi_img = hemi_soup2.find('img', class_='wide-image').get('src')
            hemisphere['title'] = hemi_title
            hemisphere['image_url'] = hemi_img
            hemisphere_image_urls.append(hemisphere)
            browser.back()

        # 4. Print the list that holds the dictionary of each image url and title.
        return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())

