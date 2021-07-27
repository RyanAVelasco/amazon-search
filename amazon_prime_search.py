from selenium import webdriver
from string import punctuation
import colored
from colored import stylize
import time
import re
import os

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
##open amazon prime page
##search in search bar
##click include with prime // ID: p_n_ways_to_watch-title, TAG: a, attr: href (FIRST ONE WILL BE INCLUDED WITH PRIME)
##check search results that contain title of movie
####if fails click NEXT
#######when NEXT unavailable end search
##check found search result for actors (if specified)
##check found search result for year (if specified)
##return search results in this order: moviename, year, actor(s), \n, url, screenshot of poster

search_query = []
# excluded = []

movie_name = input('Enter movie title: ').lower().strip()
if not movie_name == '' and len(movie_name) > 0:
    search_query.append(movie_name + ' ')
    
# print(search_query)
# quit()
# movie_year = input('Enter year: ').lower().strip()
# if not movie_year == '' and len(movie_year) > 0:
#     search_query.append(movie_year + ' ')

# movie_actors = input('Enter actors: ').lower().strip()
# if not movie_actors == '' and len(movie_actors) > 0:
#     search_query.append(movie_actors + ' ')



with webdriver.Firefox(options=fireFoxOptions) as driver:
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()
    driver.get('https://www.primevideo.com/')
    driver.implicitly_wait(5)
    driver.find_element_by_class_name('dv-copy-button').click()
    driver.find_element_by_id('ap_email').send_keys(username)
    driver.find_element_by_id('ap_password').send_keys(password)
    driver.find_element_by_id('signInSubmit').click()
    driver.find_element_by_id('pv-search-nav').click()
    time.sleep(1)
    driver.find_element_by_id('pv-search-nav').send_keys(search_query[0])
    driver.find_element_by_id('pv-search-nav').send_keys('\uE007')


    # time in seconds to wait before scrolling
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # begins search for search query
    search_results = driver.find_elements_by_class_name('tst-hover-container')
    for results in search_results:
        link = results.find_element_by_tag_name('a')
        aria = link.get_attribute('aria-label')

        temp = results.find_element_by_class_name('_2gl_vG')
        included_with_prime = temp.find_element_by_tag_name('img')
        included_with_prime = included_with_prime.get_attribute('alt')
        if included_with_prime == 'Included with Prime' : included_with_prime = '[PRIME]'
        else : included_with_prime = '[NOT PRIME]'
        

        # replaces all punctuations in aria with no space and converts it to lowercase
        for i in range(0, len(punctuation)):
            aria = aria.replace(punctuation[i], '').lower()

        if movie_name in aria:
            poster = results.find_element_by_tag_name('img')
            print(included_with_prime, poster.get_attribute('alt') + '\n' + stylize('[LINK]', colored.fg(118)), link.get_attribute('href'), '\n')
            poster.screenshot(aria.replace('  ', ' ') + '.png')

            file = open('test.txt', 'a')
            file.write(included_with_prime + ' ' + poster.get_attribute('alt') + '\n' + '[LINK]' + ' ' + link.get_attribute('href') + '\n\n')
            file.close()
            