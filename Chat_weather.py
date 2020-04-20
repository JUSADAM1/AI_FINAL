# import required modules
import requests, json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import  ListTrainer
import wikipedia
import random
# Needed to parse the HTML page
from bs4 import BeautifulSoup
chatbot = ChatBot('Chatquisha')

# To train A.I
trainer = ChatterBotCorpusTrainer(chatbot)
trainers = ListTrainer(chatbot)
# This is to establish what corpus to use.
# This corpus has everything. Mainly being used for conversation
trainer.train(
    "chatterbot.corpus.english"
)
# Conversation on football
conversation_football = [
    "What is your favorite football team?",
    "Do you play fantasy football?",
    "Who do you like on the raiders?",
    "Oakland Raiders is the best football team",
    "Oakland Raiders is my favorite football team."
]
conversation_Gaming = ['The type of games I like to play are RTS, Shooter, RPGs, Open world, MMOs.',
                       'Yes, I love playing games.']

trainers.train(conversation_football)
trainers.train(conversation_Gaming)
# Introduction
def intro():
    print("Hello I am Chatquisha!!")
    print("Type something clever or say goodbye.")

# This is being used as
def get_user_input():
    # The while loop is used for trigger words.
    # like if I say something about weather it will got to the weather function
    # once the weather function has ran it course it will go back to the main conversations such as the corpus.
    while True:
        user_input = input("> ")
        # Weather trigger word
        if user_input.find("weather") != -1:
        # Weather Function Call
            weather()
        elif user_input.find("Justyn") != -1:
            print("OH!! he is a cool guy!")
        elif user_input.find("made") != -1:
            print("I was made from a whole bunch of minds put together!!")
        # Wiki search function
        elif user_input.find("search") != -1:
            wiki()
        elif user_input.find("movie") != -1:
            movie_suggestion()
        #Trigger word for leaving ending the program
        elif user_input.find("goodbye") != -1:
            print("Its been dope talking to ya!!")
            return
        # This is used for when lets say search, Justyn, made, weather it goes back to the main chat
        else:
            general_chat(user_input)

def general_chat(user_input):
    # Get chatbot response
    response = chatbot.get_response(user_input)
    # Prints the AI assistants response
    print(response)

# This is the weather function that uses
def weather():

    # Enter your API key here
    api_key = "f3720d104d5e2a30112e54473c152c44"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"


    # Give city name
    city_name = input("Enter city name : ")

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        print(" Temperature (in kelvin unit) = " +
            str(current_temperature) +
            "\n description = " +
            str(weather_description))
    # if the city cannot be found
    else:
        print(" City Not Found ")

def wiki_p1():
    data=input('What would you like to search? ')
    return data
def wiki():
    speech_data = wiki_p1()

    words = speech_data.split(' ')

    print(words)

    if words[0] == 'search':
        search_word = ''
        for i in range(len(words)):
            if i > 0:
                search_word = search_word + words[i]

        print("Here is what I think about ", search_word)
        print(wikipedia.summary(search_word))

def movie_suggestion():
    # This is the URL I decide to webscrape from movies
    url = 'https://www.imdb.com/chart/top/?sort=rk,asc&mode=simple&page=1'
    # Getting a response from the webpage
    response = requests.get(url)
    html = response.text
    # Got to parse everything
    soup = BeautifulSoup(html, 'html.parser')
    # Here I have to get the movie title.
    # the td.titleColumn it the html code I am calling to grab information from the webpage
    movietags = soup.select('td.titleColumn')
    inner_movietags = soup.select('td.titleColumn a')
    # Will extract all the unnecessary text from website code
    rating_tags = soup.select('td.posterColumn span[name=ir]')

    # Calling the first one
    def get_year(movie_tag):
        # Here I split the movie thingy to only get movie title and
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1]
        return year

    years = [get_year(tag) for tag in movietags]
    # Gets actors list
    actors_list = [tag['title'] for tag in inner_movietags]
    # Gets title of movie
    titles = [tag.text for tag in inner_movietags]
    # Gets the rating
    ratings = [float(tag['data-value']) for tag in rating_tags]
    # number of movie titles
    n_movies = len(titles)
    while (True):
        idx = random.randrange(0, n_movies)
        # Prints everything
        print(f'{titles[idx]} {years[idx]}, ratings: {ratings[idx]:.1f}, actors/starring: {actors_list[idx]}')
        # Gives the user a choice to pick another movie suggestion.
        user_input = input('do you want another movie (y/[n])?')
        if user_input != 'y':
            break
        else:
            general_chat(user_input)


if __name__ == '__main__':
    intro()
    get_user_input()