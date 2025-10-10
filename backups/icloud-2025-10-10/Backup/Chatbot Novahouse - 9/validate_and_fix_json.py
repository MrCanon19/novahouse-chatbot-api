import csv
import json

def is_valid_json(data):
    try:
        json.loads(data)
    except json.JSONDecodeError:
        return False
    return True

with open('intents_re-v2.csv', 'r') as infile, open('intents_re-v3.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        # Validate and fix training_phrases
        if not is_valid_json(row[2]):
            row[2] = json.dumps(row[2].strip('[]').replace('\'','').split(', '))

        # Validate and fix response_templates
        if not is_valid_json(row[3]):
            row[3] = json.dumps(row[3].strip('[]').replace('\'','').split(', '))

        writer.writerow(row)

