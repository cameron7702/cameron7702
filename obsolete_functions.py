#name(String), bio (String), program (String), admissions_avg (integer), tuition_cost(integer), city_pop (integer), university_pop (integer), vibe_hours (integer, average time spent partying per week from a survey)
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
