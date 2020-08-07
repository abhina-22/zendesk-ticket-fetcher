import json
import csv
import requests
import time

credentials = 'test@gmail.com', 'password'  # replace these with your zendesk email, password
session = requests.Session()
session.auth = credentials
zendesk = 'https://thetripguru.zendesk.com'

tickets = []

url = zendesk + '/api/v2/incremental/tickets/cursor.json?start_time=1564617600'  # specify filters as per your requirement
iteration_count = 0
end_of_stream = False
while not end_of_stream:
    response = session.get(url)
    if response.status_code == 429 or response.status_code == 422:
        print('Rate limited! Please wait.', iteration_count, response.content)
        time.sleep(int(response.headers.get('retry-after', 10)))
        continue
    if response.status_code != 200:
        print('Error with status code {}'.format(response.status_code), response.content)
        exit()
    print("done fetching, iteration - ", iteration_count)
    data = response.json()
    tickets.extend(data['tickets'])
    url = data['after_url']
    end_of_stream = data['end_of_stream']
    iteration_count = iteration_count + 1

ticket_data = {'tickets': tickets}
print("done with the api call")

with open('tickets.json', mode='wb') as f:
    json.dump(ticket_data, f)

print("done writing response to file")

with open('tickets.json', mode='rb') as f:
    topic = json.load(f)

data = topic['tickets']

f = csv.writer(open("tickets.csv", "wb+"))

f.writerow(["id", "created_at", "updated_at", "status", "custom_field_id_1", "custom_field_value_1",
            "custom_field_id_2", "custom_field_value_2", "custom_field_id_3", "custom_field_value_3", "custom_field_id_4",
            "custom_field_value_4",
            "custom_field_id_5", "custom_field_value_5", "custom_field_id_6", "custom_field_value_6", "custom_field_id_7",
            "custom_field_value_7",
            "custom_field_id_8", "custom_field_value_8", "custom_field_id_9", "custom_field_value_9"
            ])

for x in data:
    f.writerow([x["id"],
                x["created_at"],
                x["updated_at"],
                x["status"],
                x["custom_fields"][0]['id'],
                x["custom_fields"][0]['value'] and x["custom_fields"][0]['value'].encode('utf-8'),
                x["custom_fields"][1]['id'],
                x["custom_fields"][1]['value'] and x["custom_fields"][1]['value'].encode('utf-8'),
                x["custom_fields"][2]['id'],
                x["custom_fields"][2]['value'] and x["custom_fields"][2]['value'].encode('utf-8'),
                x["custom_fields"][3]['id'],
                x["custom_fields"][3]['value'] and x["custom_fields"][3]['value'].encode('utf-8'),
                x["custom_fields"][4]['id'],
                x["custom_fields"][4]['value'] and x["custom_fields"][4]['value'].encode('utf-8'),
                x["custom_fields"][5]['id'],
                x["custom_fields"][5]['value'] and x["custom_fields"][5]['value'].encode('utf-8'),
                x["custom_fields"][6]['id'],
                x["custom_fields"][6]['value'] and x["custom_fields"][6]['value'].encode('utf-8'),
                x["custom_fields"][7]['id'],
                x["custom_fields"][7]['value'] and x["custom_fields"][7]['value'].encode('utf-8'),
                x["custom_fields"][8]['id'],
                x["custom_fields"][8]['value'] and x["custom_fields"][8]['value'].encode('utf-8'),
                x["custom_fields"][9]['id'],
                x["custom_fields"][9]['value'] and x["custom_fields"][9]['value'].encode('utf-8')]
               )

print("done creating csv file")

