import csv

DATA_HEADER_QUESTION = ["id","submission_time","view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]



def export_data(data, filename):
    with open(filename, 'w', encoding='utf-8', newline="") as file:
        fieldnames=DATA_HEADER
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for line in data:
            writer.writerow(line)


def import_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data



