#5.25.23

#Versions
#Python 3.9.5
#Pandas 1.3.2
#Et-xml-file 1.1.0
#Requests 2.26.0

#Sources
#https://python-reference.readthedocs.io/en/latest/intro.html
#https://docs.python.org/3.11/index.html
#https://docs.python-guide.org/scenarios/scrape/
#https://pandas.pydata.org/docs/getting_started/index.html 
#https://requests.readthedocs.io/en/latest/
#https://flybase.github.io/docs/api/

#Imports
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import time

#Initialize variables

#Read in an Excel file of deficencies to analyze
#The file should contain a list of deficencies formatted as FBab in column A (https://flybase.org/convert/id)
flies = pd.read_excel("Df.xlsx", header=None)

#Number of deficencies
rows = len(flies.index)

#Dictionary of deficiencies and breakpoints
dfs = {}

#Initialize the dictionary ignoring empty cells
for i in range(rows):
    if str(flies.iat[i, 0]) != "nan" and str(flies.iat[i, 0]) != "":
        dfs.update({str(flies.iat[i, 0]): [[],[]]})

#Main for loop to make call to the API and extract data
for df in dfs.keys():

    #Call to Flybase API
    request = requests.get("https://api.flybase.org/api/v1.0/chadoxml/"+str(df))

    #Import XML Data
    root = ET.fromstring(request.content)

    #Traversing the XML tree
    features = root.findall("./feature/feature_relationship/subject_id/feature")

    #check if left or right breakpoint (left ends in "bk1", right end in "bk2")
    for feature in features:
        breakpoint = ""
        for uniquename in feature:
            if uniquename.tag=="uniquename":
                breakpoint = uniquename.text[-1]

        #Add estimated breakpoints to dict with left breakpoint in first list and right in second
        for featureloc in feature:
            if featureloc.tag=="featureloc":
                for location in featureloc:
                    if location.tag =="fmin" or location.tag =="fmax":
                        dfs[df][int(breakpoint)-1].append(int(location.text))                        

    #Delay to abide by Flybase API 3 calls/second                         
    time.sleep(0.5)

#Data Analysis
#Iterate through deficiencies
for df in dfs.keys():
    #try to find a lower bound on df size
    try:
        leftmax = max(dfs[df][0])
        rightmin = min(dfs[df][1])
        dfs[df] = [leftmax,rightmin]
    except ValueError:
        pass

#Create dateframe of output
output = pd.DataFrame(list(map(lambda x, y: [x]+y, dfs.keys(),dfs.values())))

#Export dataframe to Excel file
output.to_excel("i.xlsx")

