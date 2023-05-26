#5.25.23

#Versions
#Python 3.9.5
#Pandas 1.3.2

#Sources
#https://python-reference.readthedocs.io/en/latest/intro.html
#https://docs.python.org/3.11/index.html
#https://pandas.pydata.org/docs/getting_started/index.html 

#Imports
import pandas as pd

#Initialize variables

#Read in an Excel file of deficencies to analyze
#This input file is the output of Nucletotide_Breakpoints.py
#The file should contain a list of deficencies pairs of FBab in column B and breakpoints columns C and D
flies = pd.read_excel("i.xlsx")

#Number of deficencies
rows = len(flies.index)

#Dictionary of deficiencies and breakpoints
#{"FBab": [start_nucleotide, end_nucleotide]}
dfs = {}

#Initialize the dictionary ignoring empty cells
for i in range(rows):
    if str(flies.iat[i, 1]) != "nan" and str(flies.iat[i, 1]) != "":
        dfs.update({str(flies.iat[i, 1]): [(flies.iat[i, 2]),(flies.iat[i, 3])]})

#Nucleotides covered by deficiencies
nucleotides = 0

#Sort deficiencies by first breakpoint
srt = sorted(list(dfs.values()), key=lambda x:x[0])

#Main for loop to calculate coverase
#Loop through deficiencies
for i in range(len(srt)):

    #Count Everything covered by the first deficiency
    if i == 0:
        nucleotides += srt[i][1]-srt[i][0]

    else:
        
        #Check if the current deficiency starts past the end of the last deficiency (there is no overlap)
        if srt[i][0] >= srt[i-1][1]:

            #If so, add all nucleotides to the sum
            nucleotides += srt[i][1]-srt[i][0]

        #If there is overlap
        else:

            #If the end of the current deficiency is less that the end of the last deficiecy (complete overlap)
            if srt[i][1] < srt[i-1][1]:
           
                #Add nothing
                pass

            #If the overlap is partial
            else:
                 
                 #Add the non-overlapping portion
                 nucleotides += srt[i][1]-srt[i-1][1]

#Print the total number of nucleotides
print("nucleotides: " + str(nucleotides))
