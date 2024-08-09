# Author: Sofia Segal
# Version: 8.9.24
#Flask script -- all the Python logic/OpenAI API implementation is in this script. Routes at the end to script.js

from flask import Flask, render_template, jsonify, request, url_for
from nltk.corpus import words
import nltk
from openai import OpenAI



app = Flask(__name__) 


client = OpenAI() #my API key is an env variable on my terminal

#accessing words from NLTK
english_words = set(words.words()) #using set instead to optimize lookup time

def getWords(bee):
    """Argument: bee, a string of 7 characters representing the 7 letters of today's spelling bee.
       Returns a string of the possible pangrams of those 7 letters
    """
    alphabet = set('abcdefghijklmnopqrstuvwxyz') #set of the english alph
    beeLetters = set(bee)
    remAlph = str(alphabet - beeLetters) #find remaining letters of the english alphabet

    allWords = [] #empty list to eventually store final pangrams in

    for word in english_words: #loop through NLKT provided eng dictionary
        countBeeLetters = 0#count of instances of the bee letters within instance of word
        skipThisWord = False #skip current word if any other letter in remAlph is in it
        for i in range(len(remAlph)):
            if str(remAlph)[i] in word: #if any other letter in word
                skipThisWord = True #skip!
                break
        if skipThisWord == True: #skip the word, move on to next word in english_words
            continue

        for i in range(7):#check if bee letters are in word
            if bee[i] in word:
                countBeeLetters +=1
        if countBeeLetters == 7: #once you reach a count of seven bee letters, you have a pangram, so add current word to the final list
            allWords += [word]
    return ', '.join(allWords) #turns final list into a String, seaprating each word with commas, makes it easier for OpenAI's chat completions to parse through


def isCompoundWord(pangram):
    """
    Checks to see if the pangram is a compound word
    Argument: String, pangram
    Returns: bool, isCompound 
    """

    for i in range(len(pangram)):#loops through letters in the pangram 
        if (pangram[:i] in english_words) and (pangram[i:] in english_words):#iterates through the pangram, comparing different sections to locate two separate words if they exist
            return "Yes, today's pangram is a compound word!"
    return "No, today's pangram is not a compound word."
    


def letterCount(pangram):
    """
    Argument: pangram, a str representing the pangram of today's bee
    Returns a hashmap of the count of each letter in the pangram
    """
    letter = pangram[0] 
    letterCount = {}
    for letter in pangram:
        if letter in letterCount:
            letterCount[letter] += 1
        else:
            letterCount[letter] = 1
    return str(letterCount)


def firstLetter(pangram):
    """
    Argument: Pangram, a str representing today's bee's pangram
    Returns the first letter of the first pangram in the list of pangrams generated by getWords(bee)
    """
    firstPangram = pangram[0]
    return "The first letter of the pangram is: " + firstPangram[0]



#OpenAI implementation:
#a carefully worded prompt is very important!

def offerWord(pangramString):
    """Utilizes OpenAI's API to determine the popularity of the pangram
       Argument: pangramString, making a String out of the list of strings pangrams generated from getWords
       Returns message, the string that gpt-3,5-turbo generates
    """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo", #using gpt-3.5-turpo, not 4o
    messages=[
        {"role": "system", "content": "You are an english expert."}, #prompt engineering 101!
        {"role": "user", "content": "Out of these words, which is the most popular? " + pangramString + "Just respond with the more popular word. Your response should only be one word, and have no special characters in it. it should be all lowercase. "} #pangramString ensured to be a string of pangrams separated by commas
    ]
    )
    message = completion.choices[0].message.content #accesses just the message content, not the role of the chat completion (OpenAI API's documentation)
    return message



#def justThePangram(chatCompletion):
    """Argument: chatCompletion, the string generated by offerWord
       Returns int index, the index at which to splice the generated chat message to determine the optimal pangram
    """
    #index = 0
    #for i in range(len(chatCompletion)):
        #if chatCompletion[i] == " ": #I noticed the chat completed with "BlahBlah" is the most popular word. So, I loop through until I hit a space and then splice the string form there
            #index = i
            #return index



def givePangram(bee): 
    """
    Master function to give the optimal (most popular) pangram for today's bee. Uses many helper functions. 
    """
    pangrams = getWords(bee)
    chatGPTAnswer = offerWord(pangrams)
    return chatGPTAnswer






#Beginning Flask routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_hint', methods=['POST'])
def get_hint():#will be executed when a POST req is made
    data = request.json #retrieves the data sent in the body of the POST. 'request': global object in Flask that represents the current request, and request.json accesses the JSON data in the request body
    bee = data.get('bee', '')  #extracts val associated w the key 'bee' from the 'data' dictionary, AKA the json. the '' empty string next to it ensures that if the key 'bee' does not exist it will return an empty string
    final = givePangram(bee) #using master function givePangram to extract the most optimal pangram
    hint = firstLetter(final)  # Generate the hint based on the pangram
    return jsonify({"hint": hint}) #returns a JSON response to client. the 'jsonify' fxn converts the Python dictionary {"hint": hint} to a JSON string. Client: script.js 

@app.route('/get_compound', methods=['POST'])
def get_compound():
    data = request.json
    bee = data.get('bee', '')  # Get the bee string from user input
    final = givePangram(bee)
    hint = isCompoundWord(final)
    return jsonify({"hint": hint})

@app.route('/get_letterCount', methods=['POST'])
def get_letterCount():
    data = request.json
    bee = data.get('bee', '')  # Get the bee string from user input
    final = givePangram(bee)
    hint = letterCount(final)  # Generate the hint based on the pangrams
    return jsonify({"hint": hint})


if __name__ == '__main__':
    app.run(debug=True)
