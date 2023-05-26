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
import time as time

#Initialize variables

#Read in an Excel file of deficencies to analyze
#The file should contain a list of deficencies in column A formatted as FBab using https://flybase.org/convert/id
flies = pd.read_excel("Dfs.xlsx", header=None)

#Number of deficencies
rows = len(flies.index)

#Dict of deficencies
dfs = {}

#Initialize the list of deficencies ignoring empty cells
for i in range(rows):
    if str(flies.iat[i, 0]) != "nan" and str(flies.iat[i, 0]) != "":
        dfs.update({flies.iat[i, 0]: []})

#Main for loop to make call to the API and extract data
for df in dfs.keys():

    #Call to Flybase API
    request = requests.get("https://api.flybase.org/api/v1.0/chadoxml/"+str(df))
    
    #Import XML Data
    root = ET.fromstring(request.content)

    #Traversing the XML tree
    props = root.findall("./feature/featureprop")
    for prop in props:

        #Check if featureprop is a breakpoint (deleted_segment)
        isbreakpoint = False

        for type_id in prop:
            if type_id.tag=="type_id":
                 for cvterm in type_id:
                    if cvterm.tag=="cvterm":
                        for name in cvterm:
                            if name.tag == "name":
                                if name.text == "deleted_segment":
                                    isbreakpoint = True

        #If it is a deleted_segement, traverse XML Tree and obtain cytological breakpoints
        if isbreakpoint:
            for value in prop:
                if value.tag=="value":
                    dfs[df].append(value.text)

    #Delay per Flybase API request limit
    time.sleep(0.5)

#Format output as pair of FBgn and Gene Name
final = list(map(lambda x, y: [x]+y, dfs.keys(), dfs.values()))

#Create dateframe of output
output = pd.DataFrame(final)

#Export dataframe to Excel file
output.to_excel("Output.xlsx")
