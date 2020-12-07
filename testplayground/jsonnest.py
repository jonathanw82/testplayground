import json

with open('./source/data.json') as access_json:
    # tell python to json in to a pyton object 
    read_content = json.load(access_json)


question_access = read_content['results']

print(question_access[2])