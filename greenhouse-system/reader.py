import json
import csv
import requests
input_file = ('sensor_log_with_id copy.csv')
url = input("Please enter the IP address of the Flask server [localhost] : ")
if not url:
   url = "http://localhost:5000/post_data"
else: 
    url = url + ":5000/post_data"
print(f"OK, reading from {input_file} and sending to {url}")
with open(input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        response = requests.post(url, json=row)
        # 200 is OK, other things are errors
        if response.status_code != 200 :
            print (response.text)