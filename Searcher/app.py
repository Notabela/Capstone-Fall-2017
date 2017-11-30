import requests
from run import find_words
from bs4 import BeautifulSoup
from os import stat
import csv

filename = "dictionary.txt"
file = open(filename, 'r')
size = stat(filename)[6]

# Could probably only use total results
google_results = {}
bing_results = {}
total_results = {}


def google_search(realword, scrambledword):

    request = requests.get("https://www.google.com/search?q="   #search word on google
                           + scrambledword)
    content = request.content   #Save google search page result

    soup = BeautifulSoup(content, "html.parser")   #Parse 'content' using html parser

    #print(soup)
    find_element1 = soup.find("span", {"style": "font-weight:bold"})  
    #Look for span element with 
    #designated style if it exists on the page
    #definition box on google search has this
    #element and style
    find_element2 = soup.find("a", {"class": "spell"})
    #Look for a element with class 'spell' which exists if a spell check exists on the google search
    find_element3 = soup.find("i", {})
    #Look for element i which google uses for 'Did you mean: ' on search page.



    # element1 is definition box
    element1 = ()
    # element2 is spell check
    element2 = ()
    # element3 is "Did you mean: "
    element3 = ()

    if find_element1 is not None:
        element1 = find_element1.text.strip().replace('·', '')   
        #If google search returns definition box than strip text of whitespace and symbols and save in variable
    if find_element2 is not None:
        element2 = find_element2.text.strip()
        #If google search result returns spell check than strip whitespace and save text
    if find_element3 is not None:
        element3 = find_element3.text.strip()

    # If all of these elements are empty, then most likely no results.
    if element1 == realword:
        google_results[realword] = [[1]]
        #This means that definition box was found and now we store [1] with word to indicate def box found.
    else:
        google_results[realword] = [[0]]
        #This means that definition box was NOT found and now we store [0] with word

    if element2 == realword:
        google_results[realword].append([1])
        #This means that spell check was found and now we store [1] with word to indicate spell check found.
    else:
        google_results[realword].append([0])
        #This means that spell check was NOT found and now we store [0] with word

    if element3 == realword:
        google_results[realword].append([1])
        #This means that 'Did you mean:' was found and now we store [1] with word
    else:
        google_results[realword].append([0])
        #This means that 'Did you mean:' was NOT found and now we store [0] with word

    #NOTE: Each word will have 3 numbers associated with it. 
    #The first number reps if 'def box' was found
    #The second number represents if 'spell check' was found
    #Third box reps if 'did you mean' was found



def bing_search(realword, scrambledword):
    request = requests.get("https://www.bing.com/search?q=" + scrambledword)
    content = request.content

    soup = BeautifulSoup(content, "html.parser")

    # TODO: Find span for what we are looking for.
    find_element1 = soup.find("div", {"role": "heading", "aria-level": "2"})
    #Look for div element with designated role, 
    #If it exists than we know we have found a definition box 
    find_element2 = soup.find("div", {"id": "sp_requery"})
    #Look for div element with designated id, 
    #If it exists than we know we have found a definition box 
    find_element3 = soup.find("strong", {})


    # element1 is definition box
    element1 = ()
    # element2 is spell check
    element2 = ()
    # element3 is "Did you mean: "
    element3 = ()

    #TODO: Write logic for formatting soup statements
    if find_element1 is not None:
        element1 = find_element1.text.strip().replace('·', '')
        #If bing search returns definition box than strip text of whitespace and symbols and save in variable
    if find_element2 is not None:
        element2_first = find_element2.text.strip().replace('Including results for ', '')
        #If bing search returns spell check
        #strip text of whitespace and the remove the 'Including results for ' 
        element2 = element2_first.replace('.', '')
        #Remove the dot symbol from element2_first text
    if find_element3 is not None:
        element3 = find_element3.text.strip()
        #If bing search returns 'did you mean:' than strip whitespaces and save text

    # If all of these elements are empty, then most likely no results.
    if element1 == realword:
        bing_results[realword] = [[1]]
        #This means that definition box was found and now we store [1] with word to indicate def box found.
    else:
        bing_results[realword] = [[0]]
        #This means that definition box was NOT found and now we store [0] with word
    if element2 == realword:
        bing_results[realword].append([1])
        #This means that spell check was found and now we store [1] with word to indicate spell check found.
    else:
        bing_results[realword].append([0])
        #This means that spell check was NOT found and now we store [0] with word
    if element3 == realword:
        bing_results[realword].append([1])
        #This means that 'Did you mean:' was found and now we store [1] with word
    else:
        bing_results[realword].append([0])
        #This means that 'Did you mean:' was NOT found and now we store [0] with word

def build_results(number_of_words):
    progress = number_of_words
    while number_of_words > 0:
        real_word, scrambled_word = find_words(file, size)
        if scrambled_word is not None:
            google_search(real_word, scrambled_word)
            bing_search(real_word, scrambled_word)
            number_of_words -= 1

        print(int(100*(1 - number_of_words/progress)), 'Percent Complete')


def write_to_file(google_dict, bing_dict):
    with open('Data/Google.csv', 'w', newline='') as csv_file1:   #Open google csv file as csv_file1
        writer1 = csv.writer(csv_file1)                          
        writer1.writerow(["Words", "Definition Box", "Spell Check", #First row of csv file are column names
                          "Did You Mean: "])
        for key, value in google_dict.items():      #Fill in the 4 columns
            writer1.writerow([key, str(value[0]).strip('[]'),   #strip away the brackets from each number
                              str(value[1]).strip('[]'),
                              str(value[2]).strip('[]')])

    with open('Data/Bing.csv', 'w', newline='') as csv_file2:
        writer2 = csv.writer(csv_file2)
        writer2.writerow(["Words", "Definition Box", "Spell Check",
                          "Did You Mean: "])
        for key, value in bing_dict.items():
            writer2.writerow([key, str(value[0]).strip('[]'),
                              str(value[1]).strip('[]'),
                              str(value[2]).strip('[]')])


build_results(10000)
write_to_file(google_results, bing_results)





