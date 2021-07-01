import csv
import random

def csvLoader(num):
    with open('./dataLoaderr/dictionary.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        mySet = set([row[0] for row in rows]) # filter the repeated element
        myData = []
        for element in mySet:
            myData.append(element)
        random.shuffle(myData)
        outputData = []
        for index, element in enumerate(myData):
            if(index >= num):
                break
            outputData.append({"id":index, "word":element})
        print(index, "data fetched.")
        return outputData
def load_words(num):
    with open('./dataLoader/words_alpha.txt') as word_file:
        mySet = set(word_file.read().split())
        myData = []
        for element in mySet:
            myData.append(element)
        random.shuffle(myData)
        outputData = []
        for index, element in enumerate(myData):
            if(index >= num):
                break
            outputData.append({"id":index, "word":element})
        print(index, "data fetched.")
    # print(outputData)
    return outputData

if __name__ == '__main__':
    # data = csvLoader(100000)
    # print(data)
    # load_words(10)
    # Total 370102 items
    data = load_words(10)
    