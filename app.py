from flask import Flask, request,jsonify
import json,csv
from csvupload import *

from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Connect to the MongoDB database
client = MongoClient('mongodb+srv://Firedrakesin:Garubb66@cluster0.iodwiy3.mongodb.net/')
db = client['social']
collection = db['user']


@app.route('/insert')
def insert():
    result=insert_data()
    return jsonify({"output":result})



@app.route('/get', methods=['POST']) 
def get_input():
    request_data = request.get_json()
    age = request_data.get('age', [])
    city_tier = request_data.get('cityTier', '')
    num_adults = request_data.get('numAdults', 0)
    num_children = request_data.get('numChildren', 0)
    sum_insured = request_data.get('sumInsured', 0)
    tenure = request_data.get('tenure', '')

    result = get_predefined_scheme(age, city_tier, num_adults, num_children, sum_insured, tenure)
    
    adult_value=result[0]
    child_value=result[1]
    discount_amt=result[2]

    adult_data=[]
    total_cost=0
    for adult_amt in adult_value:
        total_cost+=float(adult_amt[0])
        if len(adult_amt)>2:
            values= values={
            "adult":adult_amt[0],
            "age":adult_amt[1],
            "discount":adult_amt[2]
            }
            adult_data.append(values)
        else:
            values={
                "adult":adult_amt[0],
                "age":adult_amt[1]
            }
        
            adult_data.append(values)
    

    return jsonify({"adult": adult_data,"child":child_value,"discount_amt":discount_amt,"total_cost":total_cost})



def get_predefined_scheme(all_age_range, city_tier, num_adults, num_children, sum_insured, tenure):  

    base_child_rate = 7073

    if num_children == 0:
        family_type = str(num_adults)+'a'
    else:
        family_type = str(num_adults)+'a'+","+ str(num_children)+'c'
    
    child_rate=(base_child_rate*num_children)//2

    all_families=[]
    found_scheme=[]

    
    load_data = list(collection.find({}))

    load_scheme_data=[]

    for data in load_data:
        member_csv = data["member_csv"]
        age_range = data["age_range"]
        tier = data["tier"]
        var_500000 =  data["500000"]
        var_700000 =  data["700000"]
        var_1000000 = data["1000000"]
        var_1500000 = data["1500000"]
        var_2000000 = data["2000000"]
        var_2500000 = data["2500000"]
        var_3000000 = data["3000000"]
        var_4000000 = data["4000000"]
        var_5000000 = data["5000000"]
        var_6000000 = data["6000000"]
        var_7500000 = data["7500000"]
        load_scheme_data.append([member_csv,age_range,tier,var_500000,var_700000,var_1000000,var_1500000,var_2000000,var_2500000,var_3000000,var_4000000,
                                 var_5000000,var_6000000,var_7500000])

    #expanding age range
    for row in load_scheme_data:
        if row!=[]:
            if family_type==row[0] :
                ages= row[1].split("-")
                new_ages=[age for age in range(int(ages[0]),int(ages[1])+1) ]
                #reintializing the age column with expanded age range
                row[1]=new_ages
                all_families.append(row)

    claim_discount = False
    if len(all_age_range)>1:
        claim_discount = True
        all_age_range = sorted(all_age_range) 

    #checking if the age is in the range
    for i,row in enumerate(all_families):
        is_in_age_range=False
        #all_age_range is the entered age by the user
        record_age="NA"
        for age in all_age_range:
            if int(age) in row[1]:
                is_in_age_range=True
                record_age=age
                break

        if is_in_age_range:
            if claim_discount and i == 0:
                row.append("discount")
            row.append(record_age)
            found_scheme.append(row)
    
   
    premium_value=["500000","700000","1000000","1500000","2000000","2500000","3000000","4000000","5000000","6000000","7500000"]

    all_result=[]
    final_result = []
    print(found_scheme)
    discounted_amt="No discount is applicable"
    for value in found_scheme:
        for i in range(len(premium_value)):
            
            if  sum_insured == premium_value[i] and city_tier == "tier-1":
                if "discount" in value:
                    cal=float(value[i+3])//2
                    discounted_amt=float(value[i+3])-float(value[i+3])//2
                    #storing dicount value and age of the adult
                    final_value=(str(cal),str(value[-1]),discounted_amt)
                    all_result.append(final_value)
                else:
                    #storing value and age of the adult
                    all_result.append((value[i+3],str(value[-1])))

    final_result.append(all_result)
    final_result.append(child_rate)
    final_result.append(discounted_amt)

    return final_result




# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=5005)