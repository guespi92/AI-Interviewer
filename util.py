import os
print(os.getcwd())

apiKey=""

def import_config():
    global apiKey
    with open("./API_key.txt","r") as f:
        apiKey = f.readline()
