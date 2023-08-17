import json

studios = ['studio1', 'studio2', 'studio3']
days = ['day1', 'day2', 'day3']
timeslots = ['timeslot1', 'timeslot2', 'timeslot3']
classtypes = ['classtype1', 'classtype2', 'classtype3']
coaches = ['coach1', 'coach2', 'coach3']

sol_matrix = [
    [
        [
            [
                [0 for _ in range(len(coaches))]
                for _ in range(len(classtypes))]
            for _ in range(len(timeslots))]
        for _ in range(len(days))]
    for _ in range(len(studios))
]

sol_matrix[1][1][0][0][0] = 1
sol_matrix[1][1][1][0][0] = 1
sol_matrix[1][1][2][0][0] = 1

data = []

# Iterate through the matrix and update the JSON object
for studio_idx, studio in enumerate(studios):
    studio_exists = False
    
    # Check if the studio already exists in the data
    for existing_studio in data:
        if existing_studio["studio"] == studio:
            studio_exists = True
            studio_entry = existing_studio
            break
    
    if not studio_exists:
        # Create a new studio entry
        studio_entry = {
            "studio": studio,
            "schedule": []
        }
    
    for day_idx, day in enumerate(days):
        for timeslot_idx, timeslot in enumerate(timeslots):
            for classtype_idx, classtype in enumerate(classtypes):
                for coach_idx, coach in enumerate(coaches):
                    if sol_matrix[studio_idx][day_idx][timeslot_idx][classtype_idx][coach_idx] == 1:
                        entry = {
                            "timeslot": timeslot,
                            "coach": coach,
                            "classType": classtype
                        }
                        
                        # Check if the timeslot already exists in the schedule
                        existing_entry_index = None
                        for idx, schedule_entry in enumerate(studio_entry["schedule"]):
                            if schedule_entry["timeslot"] == timeslot:
                                existing_entry_index = idx
                                break
                        
                        if existing_entry_index is not None:
                            # Overwrite existing entry
                            studio_entry["schedule"][existing_entry_index] = entry
                        else:
                            # Append new entry
                            studio_entry["schedule"].append(entry)
    
    if not studio_exists:
        # Append the new studio entry to the data
        data.append(studio_entry)


# To do: Create function that validates if schedule is complete (Number of concurrent classes)

print(json.dumps(data, indent=4))