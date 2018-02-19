## Synopsis

This project is first part of our Capstone project in which we prove, using induction, the Huffman Coding data compression algorithm. We also compare the Google and Bing search engines to see how often they catch misspelled words and correct them. We use certain criteria to judge the both of them to accurately find out which search engine is better in this regard. We use python to run code that collects data based off this criteria using the api Selenium to search words on both Google and Bing.

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.


In run.py we are opening two chrome browsers with Google and Bing open on each one, taking a random word from a dictionary, scrambling the word then searching it on both browsers to see the results. With this code we are just looking at the results in real time to see how each search engine does.
```python
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
```

In app.py we collect the data based on our criteria which were if a definition box appeared in the search, if a spell check appeared with the correct spelling, and if a did you mean suggestion appeared with the correct word. This is done in both functions google_search and bing_search(). The data is collected and inserted into a csv file for further processing.

```python
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
```

In statistics.py we take the data and calculate the percentages of of each criteria.

```python
# Get the list with 0s, and 1s and add them together. Then Divide to by the length of the
# list to get the percentage that is correct
def get_percentage(second, third, fourth):
    second_len = len(second)
    third_len = len(third)
    fourth_len = len(fourth)

    second_total = 0
    third_total = 0
    fourth_total = 0

    for i in range(1, second_len):
        second_total += float(second[i])
        third_total += float(third[i])
        fourth_total += float(fourth[i])

    second_result = second_total / second_len
    third_result = third_total / third_len
    fourth_result = fourth_total / fourth_len

    return second_result, third_result, fourth_result
```

## Installation
To get the same results we did, see instructions.txt in the Searcher folder to get the chrome drivers to work.
Then run the command

**pip install -r requirements.txt**

to install the api's required but our scripts.

- To run run.py run the command python run.py

- To run app.py run the command python app.py

- To run statistics.py run the command statistics.py

All data is placed with in the Data folder with in the Seacher folder.

## References and Resources

https://drive.google.com/open?id=13uXmD4sRa6-V3yXvP71MtuWEeBsLyqjF
All of our presentations and research material can be found through the above link. This material was previously found in our repository.

https://trello.com/b/OrsvFPzi/deception-detection
Where we will be organizing our tasks. You can check and see our progress here.

