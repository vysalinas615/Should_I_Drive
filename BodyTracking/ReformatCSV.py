from os import listdir
from os.path import isfile, join
import csv
import pandas as pd


def IndividualToSingle(startDir, outputFile):
    allCSVs = [f for f in listdir(startDir) if isfile(join(startDir, f))]
    allData = []

    for curCSV in allCSVs:
        singleData = []
        singleData.append(curCSV)
        print(startDir + curCSV)


        with open(startDir + curCSV) as file_obj:
            reader_obj = csv.reader(file_obj)

            # Iterate over each row in the csv
            # file using reader object
            for row in reader_obj:
                singleData.append(row)

        allData.append(singleData)

    dataframe = pd.DataFrame(allData)
    dataframe.to_csv(outputFile, index=False)


def addBlanks(inputFile, outputFile):
    data = []

    with open(inputFile) as file_obj:
        reader_obj = csv.reader(file_obj)

        # Iterate over each row in the csv
        # file using reader object
        for row in reader_obj:
            data.append(row)

    # for row in data:
    for rowIndex, row in enumerate(data):

        # for col in row:
        for colIndex, col in enumerate(row):

            if col == "":
                data[rowIndex][colIndex] = "['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']"


    # allData.append(singleData)
    #
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(outputFile, index=False)


def labelRows(inputFile, outputFile):
    data = []

    with open(inputFile) as file_obj:
        reader_obj = csv.reader(file_obj)

        # Iterate over each row in the csv
        # file using reader object
        for row in reader_obj:
            data.append(row)

    # for row in data:
    for rowIndex, row in enumerate(data):

        col = row[0]

        if col.endswith("e0.mp4"):
            data[rowIndex][
                0] = "0"
        elif col.endswith("e1.mp4") or col.endswith("e2.mp4") or col.endswith("e3.mp4") or col.endswith("e4.mp4") or col.endswith("e5.mp4") or col.endswith("e6.mp4"):
            data[rowIndex][
                0] = "1"
        else:
            data[rowIndex][
                0] = "BAD DATA, DELETE!"

    # allData.append(singleData)
    #
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(outputFile, index=False)
