# Import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define scrape function
def mars_scrape(): 

    # Import ChromeDriver: 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Open and let load
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # Grab HTML 
    html = browser.html 
    news_soup = soup(html, 'html.parser')

    # Grabbing the pieces using the classes
    mars_news_result = news_soup.find_all('div', class_='list_text')[0]
    news_title = mars_news_result.find('div', class_="content_title").text
    news_p = mars_news_result.find('div', class_="article_teaser_body").text

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html 
    image_soup = soup(html, 'html.parser')

    # Grabbing the pieces using the classes
    image_soup_result = image_result = image_soup.find_all('div', class_='floating_text_area')[0]
    image_url_href = image_soup_result.find('a', class_='showimg fancybox-thumbs').get('href')

    image_url = url + image_url_href
    image_url

    mars_table = pd.read_html('https://space-facts.com/mars/')[0]

    # Changing column names 
    mars_table.columns = ['Description', 'Metrics']
    mars_table_html = mars_table.to_html(index=False)

    # Open and let load
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)

    # Grab HTML 
    html = browser.html 
    hemi_soup = soup(html, 'html.parser')

    # Grabbing the href using the classes
    hemi_img_list = hemi_soup.find_all('a', class_='itemLink product-item')

    # Prepare for the next step 
    hrefs = []

    for img_url in hemi_img_list: 
        print(img_url)
        hrefs.append(img_url.get('href'))

    hrefs = hrefs[:-1]
    hrefs = list(set(hrefs)) 

    # Make empty list for final urls and titles
    hemi_img_urls = []

    for img_url in hrefs:
        sec_link = url + img_url
        
        # Visit and let load
        browser.visit(sec_link)
        time.sleep(1)
        
        # Grab HTML 
        html = browser.html
        sec_link_soup = soup(html, 'html.parser')
        
        # Find the title
        img_title = sec_link_soup.find('h2', class_='title').text 
        img_title = img_title.replace(' Enhanced','')
        
        # Append sample url to final urls
        final_url = sec_link_soup.find('a', text = 'Sample').get('href')
        final_url = url + final_url # combine with base url
        
        d = {"title": img_title, "img_url": final_url}
        hemi_img_urls.append(d)
        
    # Close it
    browser.quit()

    # Combining into one dictionary for Mongo

    mars_dict = {'news_title': news_title, 
                    'news_p': news_p, 
                    'image_url': image_url, 
                    'mars_table_html': mars_table_html,
                    'hemi_img_urls': hemi_img_urls}
    print(mars_dict)
    return mars_dict 