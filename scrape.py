import sys

import requests
from bs4 import BeautifulSoup
import csv
import time
import math

courses = []
url_nums = []

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def scraper(start_time, upper_bound, school_def):
    checkVal = 50
    if(upper_bound < 50):
        checkVal = 25
    elif(upper_bound < 1000):
        checkVal = upper_bound/5
    elif(upper_bound < 10000):
        checkVal = upper_bound/10
    elif(upper_bound < 100000):
        checkVal = upper_bound/25
    elif(checkVal > 100000):
        checkVal = upper_bound/50

    checkVal = math.trunc(checkVal)

    if(checkVal%2 == 0):
        checkVal = checkVal
    else:
        checkVal = checkVal+1

    for i in range (0, upper_bound):
        try:
            if(i%checkVal == 0 and i != 0):
                print("Checking course number: ", i)
                print("Time Elapsed: ", truncate((time.time()-start_time)/60, 2), " minutes")
                percentage = i/upper_bound
                if(percentage==0):
                    percentage=1
                time_elapsed = (time.time()-start_time)/60
                print("Estimated time to completion: ", truncate(time_elapsed/percentage, 2), " minutes")
            URL = "https://" + school_def + ".instructure.com/courses/" + str(i)
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find("h1", class_="screenreader-only")

            if(title):
                bits = title.contents[0].split('<')
                pieces = bits[0].split('>')

                courses.append({'Course Name': pieces[0], 'URL Number': i, 'Full URL': URL})
                print("\nFound course: ", pieces[0], " Course Number: ", i, "\n")
        except:
            continue

def main():
    school_def = input("Please enter the first part of a Canvas URL, which replaces the typical www (For example, from fontbonne.instructure.com enter fontbonne): ")

    if not school_def:
        print("No value entered, quitting program")
        sys.exit()

    upper_bound = input("Please enter an integer as an upperbound (Recommend 9999): ")

    if not upper_bound:
        print("No value entered, quitting program")
        sys.exit()
    else:
        upper_bound = int(upper_bound)

    start_time = time.time()

    print("Started")

    scraper(start_time, upper_bound, school_def)

    fileName = "Course_Names_and_URL_Numbers_" + school_def + ".csv"

    with open(fileName, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, ('Course Name', 'URL Number', 'Full URL'))
        csvwriter.writeheader()

        csvwriter.writerows(courses)

    print('--- %s minutes ---' % truncate((time.time() - start_time)/60, 2))

if __name__ == "__main__":
    main()


