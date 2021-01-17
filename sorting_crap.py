import math, requests

test_unis = []
people = []

# pip install requests

import requests

email_address = "praxiscandie@gmail.com"
password = "praxiscandie2021"

r = requests.get("https://api.apispreadsheets.com/data/6639/")

if r.status_code == 200:
    print("SUCCESS")
    students_data = r.json()
    print(students_data)
else:
    print("FUCKING SHIT")


#person_id (String), program_interests (array of [Engineering, Computer Science, Arts, Business, Science]), academic_avg (integer), budget (integer), city_size (array of ["Small", "Medium", "Large"]), uni_size (array of ["Small", "Medium", "Large"]), vibe_level (integer, hours of expected partying per week)
def create_person(person_id, program_interests, academic_avg, budget, city_size, uni_size, vibe_level):
    person_dict = {
        "id" : person_id,
        "program_interests" : program_interests,
        "avg" : academic_avg,
        "budget" : budget,
        "city_size" : city_size,
        "uni_size" : uni_size,     
        "vibe_level" : vibe_level,
    }
    return person_dict

#name(String), bio (String), program (String), admissions_avg (integer), tuition_cost(integer), city_pop (integer), uni_pop (integer), vibe_hours (integer)
def create_university(university_id, name, bio, program, admissions_avg, tuition_cost, city_pop, uni_pop, vibe_hours):
    uni_dict = {
        "id" : university_id,
        "name" : name,
        "bio" : bio,
        "program" : program,
        "avg" : admissions_avg,
        "cost" : tuition_cost,
        "city_pop" : city_pop,
        "uni_pop" : uni_pop,
        "vibe_hours" : vibe_hours
    }
    return uni_dict

people.append(create_person(69, ["Engineering", "CompSci", "Arts", "Science", "Business"], 92, 12000, ["Small", "Medium"], ["Medium", "Large"], 7))

'''
def create_person(person_id, program_interests, academic_avg, budget, city_size, uni_size, vibe_level):
    person_dict = {
        "id" : person_id,
        "program_interests" : program_interests,
        "avg" : academic_avg,
        "budget" : budget,
        "city_size" : city_size,
        "uni_size" : uni_size,     
        "vibe_level" : vibe_level,
    }
    return person_dict
    
def create_university(university_id, name, bio, program, admissions_avg, tuition_cost, pop_density, uni_pop, uni_rank, vibe_hours):
    uni_dict = {
        "id" : university_id,
        "name" : name,
        "bio" : bio,
        "program" : program,
        "avg" : admissions_avg,
        "cost" : tuition_cost,
        "pop_dens" : pop_density,
        "uni_pop" : uni_pop,
        "vibe_hours" : vibe_hours
    }
    return uni_dict
'''

#returns a list of sorted universities
def get_match_list(person_id):

    matching_list = []
    person_dict = {}
    for person in people:
        if person_id == person["id"]:
            person_dict = person
            
    for uni in test_unis:
        uni_score = 0.0
        
        # academic avg --> max 25%
        # exponential multiplier takes into account that if your average is higher than the uni's requirements
        # you will be more likely to apply than if your average was lower 

        print(uni)
        avg_dif = abs(person_dict["avg"] - uni["avg"])
        exponential_multiplier = 0.7 * (person_dict["avg"] > uni["avg"]) + 1.1 * (person_dict["avg"] < uni["avg"]) 
        uni_score += 25 - (avg_dif > 5) * abs(avg_dif - 5) ** exponential_multiplier
        print("1", uni_score)


        # program interests --> max 30%
        for cnt, program in enumerate(person_dict["program_interests"]):
            if program == uni["program"]:
                uni_score += 30 - cnt ** math.log(30, 4)
        print("2", uni_score)

            
        # budget --> max 20%
        budget_dif = abs(person_dict["budget"] - uni["cost"])
        uni_score += 20
        if person_dict["budget"] < uni["cost"]:
            uni_score -= (budget_dif > 3000) * (abs((3000 - budget_dif) / 2000) ** 1.1)
        print("3", uni_score)

        # population density --> max 5%
        # small_city: 0-100000, medium_city: 100001-250000, big_city: 250000+
        #city_size = None
        if uni["city_pop"] <= 100000:
            city_size = "Small"
        if uni["city_pop"] > 100000 and uni["city_pop"] <= 250000:
            city_size = "Medium"
        else:
            city_size = "Large"
        
        if city_size in person_dict["city_size"]:
            uni_score += 5
        else:
            uni_score += 0
        print("4", uni_score)


        # uni size --> max 5%
        # small_uni: 0-5000, medium_uni: 5000-15000, big_uni: 15000+
        #uni_size = None
        if uni["uni_pop"] <= 5000:
            uni_size = "Small"
        if uni["uni_pop"] > 5000 and uni["uni_pop"] <= 15000:
            uni_size = "Medium"
        else:
            uni_size = "Large"
        
        if uni_size in person_dict["uni_size"]:
            uni_score += 5
        else:
            uni_score += 0
        print("5", uni_score)


        #vibe check --> max 15%
        # same approach as academic avg
        vibe_dif = abs(person_dict["vibe_level"] - uni["vibe_hours"])
        uni_score += 15 - (vibe_dif > 3) * (vibe_dif - 3) * 1.41

        #add to matching_list, how
        matching_list.append([int(uni_score), uni["id"]])
        print("6", uni_score)
        print('\n')

    return sorted(matching_list, reverse = True)

#print(get_match_list(69))