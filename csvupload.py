from flask import Flask, request,jsonify
import json,csv

from pymongo import MongoClient
from flask_cors import CORS

csv_file_path = './sample--rates.csv'

# Connect to the MongoDB database
client = MongoClient('mongodb+srv://Firedrakesin:Garubb66@cluster0.iodwiy3.mongodb.net/')
db = client['social']
collection = db['user']

def insert_data():
    with open(csv_file_path, mode='r') as file:
        load_scheme_data = csv.reader(file)  


        #expanding age range
        for data in load_scheme_data:
            if data!=[]:
                user_csv = {
                "member_csv": data[0],
                "age_range": data[1],
                "tier": data[2],
                "500000": data[3],
                "700000": data[4],
                "1000000": data[5],
                "1500000": data[6],
                "2000000": data[7],
                "2500000": data[8],
                "3000000": data[9],
                "4000000": data[10],
                "5000000": data[11],
                "6000000": data[12],
                "7500000": data[13]}

                collection.insert_one(user_csv)
        return "success"
                




            



