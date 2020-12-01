import sys

import requests
from bs4 import BeautifulSoup
import csv
import time
import math

courses = []
url_nums = []

#truncates a float to a specified number of decimal places
def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

#Runs through a loop to iterate through course numbers from 0 up to the upper bound supplied by the user
def scraper(start_time, upper_bound, school_def):
    #Determines how often to give updates to the user, based on the upper bound
    checkVal = 50
    if(upper_bound < 50):
        checkVal = 2
    elif(upper_bound < 1000):
        checkVal = upper_bound/5
    elif(upper_bound < 10000):
        checkVal = upper_bound/10
    elif(upper_bound < 100000):
        checkVal = upper_bound/25
    elif(checkVal > 100000):
        checkVal = upper_bound/50

    checkVal = math.trunc(checkVal)

    #makes sure checkVal is an even number so there is no chance of having a prime number
    if(checkVal%2 == 0):
        checkVal = checkVal
    else:
        checkVal = checkVal+1

    for i in range (0, upper_bound):
        try:
            #Provides update to user if i%checkVal is 0
            if(i%checkVal == 0 and i != 0):
                print("Checking course number: ", i)
                print("Time Elapsed: ", truncate((time.time()-start_time)/60, 2), " minutes")
                percentage = i/upper_bound
                if(percentage==0):
                    percentage=1
                #Calculates the time elapsed
                time_elapsed = (time.time()-start_time)/60
                #Calculates and prints the estimated time until completion
                print("Estimated time to completion: ", truncate(time_elapsed/percentage, 2), " minutes")
            #Generates the URL to check
            URL = "https://" + school_def + ".instructure.com/courses/" + str(i)
            #Makes a web request to the URL
            page = requests.get(URL)

            #Declares a parser for HTML and looks for a h1 tag of class 'screenreader-only'
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find("h1", class_="screenreader-only")

            #If the h1 tag is found, splits the data by < and >, appends data to courses, and prints to the console
            if(title):
                bits = title.contents[0].split('<')
                pieces = bits[0].split('>')

                courses.append({'Course Name': pieces[0], 'URL Number': i, 'Full URL': URL})
                print("\nFound course: ", pieces[0], " Course Number: ", i, "\n")
        except:
            continue

def main():
    #Gets school definition from the user
    school_def = input("Please enter the first part of a Canvas URL, which replaces the typical www (For example, from fontbonne.instructure.com enter fontbonne): ")

    #Checks that something was actually entered
    if not school_def:
        print("No value entered, quitting program")
        sys.exit()

    #Gets an upper bound from the user
    upper_bound = input("Please enter an integer as an upperbound (Recommend 9999): ")

    #Makes sure something was entered and converts to int if so
    if not upper_bound:
        print("No value entered, quitting program")
        sys.exit()
    else:
        upper_bound = int(upper_bound)

    #Gets the current time for use later in the program
    start_time = time.time()

    #Lets the user know the process has started
    print("Started")

    #Calls the scraper class
    scraper(start_time, upper_bound, school_def)

    fileName = "Course_Names_and_URL_Numbers_" + school_def + ".csv"

    #Prints data from courses to a csv file
    with open(fileName, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, ('Course Name', 'URL Number', 'Full URL'))
        csvwriter.writeheader()

        csvwriter.writerows(courses)

    #Calculates total time taken to run the program
    print('--- %s minutes ---' % truncate((time.time() - start_time)/60, 2))

if __name__ == "__main__":
    main()


