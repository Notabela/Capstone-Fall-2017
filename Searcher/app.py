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

    request = requests.get("https://www.google.com/search?q="
                           + scrambledword)
    content = request.content

    soup = BeautifulSoup(content, "html.parser")

    #print(soup)
    find_element1 = soup.find("span", {"style": "font-weight:bold"})
    find_element2 = soup.find("a", {"class": "spell"})
    find_element3 = soup.find("i", {})

    # element1 is definition box
    element1 = ()
    # element2 is spell check
    element2 = ()
    # element3 is "Did you mean: "
    element3 = ()

    if find_element1 is not None:
        element1 = find_element1.text.strip().replace('·', '')
    if find_element2 is not None:
        element2 = find_element2.text.strip()
    if find_element3 is not None:
        element3 = find_element3.text.strip()

    # If all of these elements are empty, then most likely no results.
    if element1 == realword:
        google_results[realword] = [[1]]
    else:
        google_results[realword] = [[0]]

    if element2 == realword:
        google_results[realword].append([1])
    else:
        google_results[realword].append([0])

    if element3 == realword:
        google_results[realword].append([1])
    else:
        google_results[realword].append([0])


def bing_search(realword, scrambledword):
    request = requests.get("https://www.bing.com/search?q=" + scrambledword)
    content = request.content

    soup = BeautifulSoup(content, "html.parser")

    # TODO: Find span for what we are looking for.
    find_element1 = soup.find("div", {"role": "heading", "aria-level": "2"})
    find_element2 = soup.find("div", {"id": "sp_requery"})
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
    if find_element2 is not None:
        element2_first = find_element2.text.strip().replace('Including results for ', '')
        element2 = element2_first.replace('.', '')
    if find_element3 is not None:
        element3 = find_element3.text.strip()

    # If all of these elements are empty, then most likely no results.
    if element1 == realword:
        bing_results[realword] = [[1]]
    else:
        bing_results[realword] = [[0]]

    if element2 == realword:
        bing_results[realword].append([1])
    else:
        bing_results[realword].append([0])

    if element3 == realword:
        bing_results[realword].append([1])
    else:
        bing_results[realword].append([0])


def build_results(number_of_words):
    while number_of_words > 0:
        real_word, scrambled_word = find_words(file, size)
        if scrambled_word is not None:
            google_search(real_word, scrambled_word)
            bing_search(real_word, scrambled_word)
            number_of_words -= 1


def write_to_file(google_dict, bing_dict):
    with open('Data/Google.csv', 'w', newline='') as csv_file1:
        writer1 = csv.writer(csv_file1)
        writer1.writerow(["Words", "Definition Box", "Spell Check",
                          "Did You Mean: "])
        for key, value in google_dict.items():
            writer1.writerow([key, str(value[0]).strip('[]'),
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


build_results(100)
write_to_file(google_results, bing_results)





