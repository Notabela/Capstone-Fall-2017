from random import randrange, randint
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


def scramble(string):
    # remove two chars from the string at random indexes
    index = randrange(len(string))
    string = string[:index] + string[index + 1:]

    # Obtain a random index in string, reverse the substring from index
    rand_index = randrange(len(string))
    if rand_index + 2 > len(string)-1:
        rand_index -= 2

    # reverse the selected substring
    string = string[:rand_index] + string[rand_index:rand_index + 2][::-1] + string[rand_index + 2:]

    return string


def search_with(browser, word1, word2):
    search = browser.find_element_by_name('q')
    search.send_keys(word1)
    search.send_keys(Keys.RETURN)  # hit return after you enter search text
    time.sleep(0.5)
    browser.find_element_by_name('q').send_keys(' [Real Word: {}]'.format(word2))
    time.sleep(1)  # sleep for 2 seconds so you can see the results


def find_words(file, file_size):
    # Seek to a place in the file which is a random distance away
    # Mod by file size so that it wraps around to the beginning
    file.seek((file.tell() + randint(0, file_size - 1)) % file_size)

    # dont use the first readline since it may fall in the middle of a line
    file.readline()

    # this will return the next (complete) line from the file
    word = file.readline().strip()
    realword = word
    scrambledword = ''

    if len(word) > 5 and "'" not in word:
        scrambledword = scramble(word)

    return realword, scrambledword


if __name__ == '__main__':
    browser1 = webdriver.Chrome()
    browser2 = webdriver.Chrome()

    browser1.get('http://www.google.com')
    browser2.get('http://www.bing.com')

    filename = "dictionary.txt"
    file = open(filename, 'r')
    size = os.stat(filename)[6]

    while True:
        real_word, scrambled_word = find_words(file, size)
        if len(scrambled_word) > 0:
            search_with(browser1, scrambled_word, real_word)
            search_with(browser2, scrambled_word, real_word)

            browser1.find_element_by_name('q').clear()
            browser2.find_element_by_name('q').clear()
