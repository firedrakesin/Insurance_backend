from pymongo import MongoClient
import csv
csv_file_path = './sample--rates.csv'

client = MongoClient('mongodb+srv://Firedrakesin:Garubb66@cluster0.iodwiy3.mongodb.net/')
db = client['social']
collection = db['user']


def get_result(result):
    adult_value=result[0]
    child_value=result[1]
    discount_amt=result[2]

    adult_data=[]
    total_cost=0
    for adult_amt in adult_value:
        
        if len(adult_amt)>2:
            values= values={
            "adult":adult_amt[0],
            "age":adult_amt[1],
            "discount":adult_amt[2]
            }
            total_cost+=float(adult_amt[2])
            adult_data.append(values)
        else:
            values={
                "adult":adult_amt[0],
                "age":adult_amt[1]
            }
            total_cost+=float(adult_amt[0])
            adult_data.append(values)

    total_cost+=child_value
    return (adult_data,child_value,discount_amt,total_cost)


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


    for row in load_scheme_data:
        if row!=[]:
            if family_type==row[0] :
                ages= row[1].split("-")
                new_ages=[age for age in range(int(ages[0]),int(ages[1])+1) ]
                row[1]=new_ages
                all_families.append(row)

    claim_discount = False
    if len(all_age_range)>1:
        claim_discount = True
        all_age_range = sorted(all_age_range) 


    for row in all_families:
        is_in_age_range=False
        intial_row_value=0

        for i,age in enumerate(all_age_range):
            
            if int(age) in row[1]:

                intial_row_value+=1
                
                if claim_discount and i == 0:
                    row.append("discount")
                row.append(age)
            
                if intial_row_value>1:
                    row.pop(-2)
                    if "discount" in row:
                        row.pop(-2)
                immute = tuple(row)
                found_scheme.append(immute)
            
            
   
    premium_value=["500000","700000","1000000","1500000","2000000","2500000","3000000","4000000","5000000","6000000","7500000"]

    all_result=[]
    final_result = []

    discounted_amt="No discount is applicable"
    for value in found_scheme:
        for i in range(len(premium_value)):
            
            if  sum_insured == premium_value[i] and city_tier == "tier-1":
                if "discount" in value:
                    cal=float(value[i+3])//2
                    discounted_amt=float(value[i+3])-float(value[i+3])//2
                    final_value=(value[i+3],str(value[-1]),discounted_amt)
                    all_result.append(final_value)
                else:
                    all_result.append((value[i+3],str(value[-1])))

    final_result.append(all_result)
    final_result.append(child_rate)
    final_result.append(discounted_amt)

    return final_result

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
                

