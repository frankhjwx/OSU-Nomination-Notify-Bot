import json

def getUsers():
    f = open('users.json', 'r')
    users = f.read()
    data = json.loads(users)
    f.close()
    return data

def saveUsers(list):
    with open('users.json', "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(list))