import pandas as pd
import numpy as np

#prompt the user for the csv file names
files = input("Enter the name of the csv files to be read, separated by a comma: ").split(",")
# if not a csv file, prompt the user again
for file in files:
    while file[-4:] != ".csv":
        file = input("Initial input wrong, Enter the name of the csv files to be read, separated by a comma: ").split(",")


#combine all csvs into one file and store it in a new csv
combined_csv = pd.concat([pd.read_csv(f) for f in files ])
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

file_loc = "combined_csv.csv"

df = pd.read_csv(file_loc, usecols= ["title"])

df = pd.read_csv(file_loc, usecols= ["title", "year_published"])
titles = df["title"].values

filter_type = input("Enter the type of filter you want to apply: \n|1| for Title - keyword filter. \n|2| for title + year filter.");

#if the choice is neither 1 or 2 prompt the user again
while filter_type != "1" and filter_type != "2":
    filter_type = input("Initial input wrong, Enter the type of filter you want to apply: \n|1| for Title - keyword filter. \n|2| for title + year filter.\n");

#if the user choses option 2 ask for the minimum year
if filter_type == "2":
    min_year = input("Enter the minimum year: ");
    #if the input is not a number, prompt the user again
    while not min_year.isdigit():
        min_year = input("Initial input wrong, Enter the minimum year: ");

#ask the user if they want automated keywords or to enter manually 
auto = input("Do you want to use automated keywords? (y/n): ")

if auto == "n" or auto == "N":
    # prompt the user for the keywords and store them in an array
    keywords = input("Enter the keywords you want to search for, separated by a comma: ").split(",")
else : 
    keywords = ["collaboration","Virtual Reality","collaboration task",
        "collaboration framework","Augmented Reality", "Asynchronous collaboration", 
        "Synchronous collaboration", "CVREs", "peer-to-peer topology", "GCW", "peer VR collaboration", 
        "collaboration framework", "Building Information Modeling (BIM)", "collaborative task simulation", 
        "peer-to-peer topology", "collaboration framework in VR", "Virtual reality", "augmented reality", 
        "latency-free collaboration", "real-time collaboration", "remote collaboration", "3D scene reconstruction", 
        "classification", "MR", "VLE", "IVR", "Human-centered computing", "Human computer interaction (HCI)", "Interaction paradigms", 
        "Collaborative and social computing", "Industrial collaboration","Collaborative virtual reality", "Maintenance method development",
        "embedded guidance", "Mental workload", "collaborative interaction", "redirected interaction", "social presence" , "shared perspective", 
        "Human-Robot Collaboration", "social"]

#create a lower case version of the keywords
keywords_lower = [keyword.lower() for keyword in keywords]

# if the user wants to apply both filters
if filter_type == "1":

    # check if any of the keywords exist in the title
    # if so, add the title to a new list
    new_titles = []
    for title in titles:
        for keyword in keywords:
            # if at least one keyword is there we add the title to the new list
            if keyword.lower() in title.lower() and title not in new_titles:
                new_titles.append(title)


if filter_type == "2":
    #check if the title contains any of the keywords and that the date is higher than 2009
    newList = []
    # go over both columns and check if the title contains any of the keywords and that the date is higher than 2009
    for title, date in df.itertuples(index=False):
        for keyword in keywords:
            if keyword.lower() in title.lower() and date >= min_year and title not in newList:
                newList.append(title)


# write the new list to a csv called result2.csv
df = pd.DataFrame(new_titles, columns=["title"]);
# inform the user that we  are generating the csv file
print("Generating csv file with filtered data...");
df.to_csv("filteredPapers.csv", index=False)

# inform the user that the csv file has been generated
print("csv file generated successfully");
