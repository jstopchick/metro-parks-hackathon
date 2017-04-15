# Christina Chelf
# Lab 6B

#   1.  Using what you’ve learned in ex1-3 and in reading the documents, your goal is to  create a script that:
#       a.  Asks a user what they would like to search on Twitter
#       b.  Asks a user where they would like a map of these tweets.
#       c.  Creates a map centered on the location given that starts at zoom level 8.
#       d.  The map has markers placed at the location of each tweet, the pop up text is the content of each 
#            tweet and the poster, like so:
#           i.  “[Username] said [Tweet Content]”
#   2.  Some hints:
#       a.  Your script can store the generated .html in the local path.
#       b.  Don’t forget about error handling – You’ll want to make sure all of your inputs are correct and that a ‘user’ gives an actual place name.
#       c.  Remember the basics of this lab – use for loops to iterate across data, etc.

import arcpy 
from arcpy import env 
from TwitterSearch import *
from geopy import geocoders
import fileinput
import string
import os
import datetime
import folium
import webbrowser
import os

displaylocation = None
twittersearch = None

# Geocode location using geopy, returns lat and long
def geo(location):
    g = geocoders.Nominatim()
    loc = g.geocode(location)
    return loc.latitude, loc.longitude

# Ask user what to search for

while twittersearch is None:
    input_word=raw_input('What should we search for on Twitter: ')
    try:
        twittersearch=str(input_word)
    except ValueError:
        print 'Invalid input. Try again'
    else:
        break
while displaylocation is None:
    input_word=raw_input('Where should we look on a map: ')
    try:
        displaylocation=str(input_word)
    except ValueError:
        print 'Invalid input. Try again'
    else:
        break


#creates a map centered on the location specified using default configuration
map3 = folium.Map(location=geo(displaylocation), tiles='Stamen Terrain', zoom_start=8)
print "Gathering tweets and putting them on the map!"

#Search Twitter 
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([twittersearch]) # let's define all words we would like to have a look for
    tso.set_include_entities(False) # and don't give us all those entity information

    #object creation with secret token
    #These are Christina Chelfs Personal keys, please delete if you use for anything else. 
    ts = TwitterSearch(
        consumer_key = 'tCZCl52HevrPprawvygKkWWVF',
        consumer_secret = 'K1UAUoCcZvCeGEY62ciy36itMIIIcfmbNuY8xvZc7IkLiXbSyv',
        access_token = '235018027-CQLQi4Sz6wePWfEuo77AFyOUBh8lFKD0JH4U4ZpW',
        access_token_secret = 'E7ZQb80ItUF9hXFdHq5CAw8JShwWdzQtpEg8lrPcoMAfE'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        if tweet['place'] is not None: 
            (lat, lng) = geo(tweet['place']['full_name'])
            x= lng
            y= lat
            twitteruser = tweet['user']['screen_name']
            tweettext= tweet['text']
            folium.Marker([y, x], popup= twitteruser +" tweeted: "+ tweettext).add_to(map3)
        
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
        
#saves to whatever directory you're in
map3.save('map3.html')

#This will take the location of maps1.html in our local directory and return the absolute path to it
webbrowser.open('file://'+ os.path.realpath('map3.html'))

print "done"