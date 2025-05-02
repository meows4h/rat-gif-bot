import datetime
import csv
import discord
import math

csv_file = "data.csv"

def get_rat(number):

    data = []
    number = f'{number}'

    # reading all the csv file info
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            data.append(row)

    # print(f'NUMBER: {number}, THE DATA: {data}')

    for idx, row in enumerate(data):
        if row[0] == number: # checking for the matching date / number
            return f'{row[1]}'
        
    return ''
