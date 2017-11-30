import csv
import pandas

def read_from_csv(filename):
    # first Column line Key words
    # Second Column line definition box
    # Third Column line spell check
    # Fourth Column line Did you mean?\
    # Fifth Column line Resemblence
    colnames = ['words', 'definition_box', 'spell_check', 'did_you_mean']
    data = pandas.read_csv(filename, names=colnames)
    first_column = data.words.tolist()
    second_column = data.definition_box.tolist()
    third_column = data.spell_check.tolist()
    fourth_column = data.did_you_mean.tolist()
    #fifth_column = data.resemblence.tolist()

    return first_column, second_column, third_column, fourth_column

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


#TODO get more statistics and make graphs

words, definition_box, spell_check, did_you_mean = read_from_csv("data/bing.csv")
definition_box_percentage, spell_check_percentage, did_you_mean_percentage = get_percentage(definition_box, spell_check, did_you_mean)
print "Bing's Percentages"
print definition_box_percentage
print spell_check_percentage
print did_you_mean_percentage
print("\n")
words, definition_box, spell_check, did_you_mean = read_from_csv("data/google.csv")
definition_box_percentage, spell_check_percentage, did_you_mean_percentage = get_percentage(definition_box, spell_check, did_you_mean)
print "Google's Percentages"
print definition_box_percentage
print spell_check_percentage
print did_you_mean_percentage
