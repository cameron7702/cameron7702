import math, requests, json

people = []

# pip install requests
import requests

email_address = "praxiscandie@gmail.com"
password = "praxiscandie2021"

user_uni_sheet = "6647/"
user_info_sheet = "6648/"
uni_info_sheet = "6649/"

r = requests.get("https://api.apispreadsheets.com/data/" + uni_info_sheet)

if r.status_code == 200:
    print("SUCCESS")
    universities = r.json()["data"]
else:
    print("OOF")

r2 = requests.get("https://api.apispreadsheets.com/data/" + user_info_sheet)

if(r.status_code == 200):
    print("#2 SUCCESS")
    users = r2.json()["data"]
else:
    print(r.status_code)
    print("FUCK THIS SHIT FUCK FUCK FUCK")

#returns a list of sorted universities
def get_match_list(person_id):

    matching_list = []
    temp = users[int(person_id) - 1]
    print(temp)
    program_interests = [temp["Program 1"], temp["Program 2"], temp["Program 3"], temp["Program 4"], temp["Program 5"]]

    person_dict = {"program_interests" : program_interests, "sat" : int(temp["Sat"]), "gpa" : float(temp["Admissions_avg"]), "budget" : int(temp["Tuition Cost"])}
    person_dict["city_size"] = temp["City size"]
    person_dict["uni_pop"] = temp["Uni size"]
    person_dict["vibe_level"] = float(temp["Vibe level"])

    for uni_id, uni in enumerate(universities):
        
        uni_score = 0.0
        person_avg = 0.0
        
        #convert SAT scores into percentiles (2020 statistics)
        if person_dict["sat"] >= 1550:
            person_avg = 99
        if person_dict["sat"] < 1550 and person_dict["sat"] >= 1500:
            person_avg = 98
        if person_dict["sat"] < 1500 and person_dict["sat"] >= 1450:
            person_avg = 97
        if person_dict["sat"] < 1450 and person_dict["sat"] >= 1400:
            person_avg = 95
        if person_dict["sat"] < 1400 and person_dict["sat"] >= 1350:
            person_avg = 93
        if person_dict["sat"] < 1350 and person_dict["sat"] >= 1300:
            person_avg = 88
        if person_dict["sat"] < 1300 and person_dict["sat"] >= 1250:
            person_avg = 84
        if person_dict["sat"] < 1250 and person_dict["sat"] >= 1200:
            person_avg = 78
        if person_dict["sat"] < 1200 and person_dict["sat"] >= 1150:
            person_avg = 70
        if person_dict["sat"] < 1150 and person_dict["sat"] >= 1000:
            person_avg = 65
        else:
            person_avg = 55

        #in order to get a personal average application percentage, average the SAT percentile and GPA score percentage 
        person_avg = (person_avg + person_dict["gpa"])/2

        # academic avg --> max 25% 
        # exponential multiplier takes into account that if your average is higher than the uni's requirements
        # you will be more likely to apply than if your average was lower
        avg_dif = abs(person_avg - float(uni["avg"]))
        exponential_multiplier = 0.7 * (person_avg > float(uni["avg"])) + 1.1 * (person_avg < float(uni["avg"])) 
        uni_score += 25 - (avg_dif > 5) * abs(avg_dif - 5) ** exponential_multiplier

        # program interests --> max 30%
        # calculate the match based on how the applicant ranks their program choices
        for cnt, program in enumerate(person_dict["program_interests"]):
            if program == uni["program"]:
                uni_score += 30 - cnt ** math.log(30, 4)

            
        # budget --> max 20%
        budget_dif = abs(int(person_dict["budget"]) - int(uni["tuition"]))
        uni_score += 20
        if int(person_dict["budget"]) < int(uni["tuition"]):
            uni_score -= (budget_dif > 3000) * (abs((3000 - budget_dif) / 2000) ** 1.1)


        # population density --> max 5%
        # small_city: 0-100000, medium_city: 100001-250000, big_city: 250000+
        if int(uni["city_pop"]) <= 100000:
            city_size = "Small"
        if int(uni["city_pop"]) > 100000 and int(uni["city_pop"]) <= 250000:
            city_size = "Medium"
        else:
            city_size = "Large"
        
        if city_size in person_dict["city_size"]:
            uni_score += 5
        else:
            uni_score += 0


        # uni size --> max 5%
        # small_uni: 0-5000, medium_uni: 5000-15000, big_uni: 15000+
        if int(uni["uni_pop"]) <= 5000:
            uni_size = "Small"
        if int(uni["uni_pop"]) > 5000 and int(uni["uni_pop"]) <= 15000:
            uni_size = "Medium"
        else:
            uni_size = "Large"
        
        if uni_size in person_dict["uni_pop"]:
            uni_score += 5
        else:
            uni_score += 0

        # vibe check --> max 15%
        # same approach as academic avg
        vibe_dif = abs(float(person_dict["vibe_level"]) - float(uni["vibe_hours"]))
        uni_score += 15 - (vibe_dif > 3) * (vibe_dif - 3) * 1.41
        

        matching_list.append([int(uni_score), uni_id])
  
    sorted(matching_list, reverse = True)

    r3 = requests.get("https://api.apispreadsheets.com/data/" + user_uni_sheet)
    user_data = r3.json()
    user_data["data"][1]["ID"] = 500
    print(user_data)

    r4 = requests.post("https://api.apispreadsheets.com/data/6647/", headers={}, json={"data": {"ID":"1"}, "query": "select*from6647whereID='5'"})
    print(r4)

print(get_match_list(1))