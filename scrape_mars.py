#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}

    #NASA Mars News URL to be scraped for latest news and paragraph title
    URL = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(URL)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')  

    #Retrieve the latest news title from Nasa Mars News
    news_title = soup.find('div', class_='content_title').text

    #Retrieve the latest news paragraph from Nasa Mars News
    news_para = soup.find('div', class_='rollover_description_inner').text

    print(f'News Title:{news_title}')
    print(f'News Paragraph:{news_para}') 

    # add latest news and paragraph to dictionary
    listings['news_title'] = news_title
    listings['news_para'] = news_para

    # JPL url to scrape featured images
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # visit JPL url
    browser.visit(jpl_url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    jpl_soup = bs(html, 'html.parser')

    # Retrieve all elements that contain url information
    result = jpl_soup.find('footer')

    #run the loop to find the image url
    a = result.find('a')
    image_url = result.a['data-fancybox-href']
    baseUrl = 'https://www.jpl.nasa.gov'
    featured_image_url = baseUrl + image_url
    print(featured_image_url)

    # add featured image url to dictionary
    listings['featured_image_url'] = featured_image_url

    #mars weather URL
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    # visit weather url
    browser.visit(weather_url)

    # HTML object
    weather_html = browser.html
    # Parse HTML with Beautiful Soup
    weather_soup = bs(weather_html, 'html.parser')

    #get mars weather latest tweet from website
    mars_weather = weather_soup.find('p', class_='TweetTextSize').text
    print(mars_weather)

    # add mars weather latest tweet to dictionary
    listings['mars_weather'] = mars_weather

    #Mars facts URL
    facts_url = 'http://space-facts.com/mars/'

    #use pandas to scrape the table
    tables = pd.read_html(facts_url)

    #use pandas to convert data into a table
    df = tables[0]
    df.columns = ['0', '1']
    df.rename(columns={'0': 'Description', '1': 'Values'})

    #Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html()

    # add latest news and paragraph to dictionary
    listings['html_table'] = html_table

    # use the USGS Astrogeology site
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # setting up splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(usgs_url)

    # HTML object
    usgs_html = browser.html
    # Parse HTML with Beautiful Soup
    usgs_soup = bs(usgs_html, 'html.parser')

    # create an empty list to hold the hrefs from usgs URL
    href = []
    # find the hrefs
    links = browser.find_by_css('div[class="description"] a')
    # Loop through those links, click the link, find the sample anchor, return the href
    for i in links:
        k = i['href']
        href.append(k)

    # import urljoin from urllib.parse
    from urllib.parse import urljoin
    # create an empty list for image url and title 
    hemisphere_url_title = []
    # run the loop to find the image url and title from usgs webpage
    for h in href:
        hemisphere = {}
        browser.visit(h)
        html = browser.html
        soup = bs(html, 'html.parser')
        quotes = soup.find_all('img', class_='wide-image')
        a = soup.find_all('h2', class_='title')
        for quote in quotes:
            #print(quote['src'])
            #print(urljoin(h, quote['src']))
            hemisphere['img_url'] = urljoin(h, quote['src'])
            
        for i in a:
            #print(i.text)
            hemisphere['title'] = i.text

        hemisphere_url_title.append(hemisphere)

        # add hemisphere image URL and title to dictionary
        listings['hemisphere'] = hemisphere_url_title

        return listings









