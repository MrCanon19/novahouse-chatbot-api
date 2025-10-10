import csv
import json

with open('intents.csv', 'r') as infile, open('intents_fixed.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        # Fix training_phrases
        try:
            training_phrases = row[2].replace("'", '"')
            json.loads(training_phrases)
            row[2] = training_phrases
        except json.JSONDecodeError:
            pass

        # Fix response_templates
        try:
            response_templates = row[3].replace("'", '"')
            json.loads(response_templates)
            row[3] = response_templates
        except json.JSONDecodeError:
            pass

        writer.writerow(row)

