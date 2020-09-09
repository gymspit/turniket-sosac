from pypxlib import Table
import requests
import time
import json

API_URL = "https://api.gymsp.it/passes"

# Replace Lafovi znaky
def f_decode_laf(text):
    text_string = str(text)

    text_string = text_string.replace("ý", "ě")
    text_string = text_string.replace('²','ý')
    text_string = text_string.replace("°", "ř")
    text_string = text_string.replace("×", "ž")
    text_string = text_string.replace("Ú", "é")
    text_string = text_string.replace("ß", "á")
    text_string = text_string.replace("Þ", "č")
    text_string = text_string.replace("Ý", "í")
    text_string = text_string.replace("Ü", "š")
    text_string = text_string.replace("╚", "Č")
    text_string = text_string.replace("¨", "ů")
    text_string = text_string.replace("è", "Š")
    text_string = text_string.replace("Ï", "Ř")
    text_string = text_string.replace("┴", "Á")
    text_string = text_string.replace("═", "Í")
    text_string = text_string.replace("Ä", "Ž")
    text_string = text_string.replace("╠", "Ě")
    text_string = text_string.replace("¦", "Ý")
    text_string = text_string.replace("╔", "É")

    return(text_string)

# Get row from table_person with chip_id
def f_get_person_with_chip_id(table_person, chip_id):
    chip_id = str(chip_id)
    for row in table_person:
        if row["Cip"] == chip_id:
            return(row)

# Main
def main(last_logged_pass):
    table_passes = Table("PRUCHODY.db")
    table_person = Table("OSOBY.db")

    found = False
    position_from_end = 1

    while(not found):
        position = len(table_passes) - position_from_end
        current_pass = table_passes[position]

        print("Current ID", current_pass.ID)
        print("Last ID", last_logged_pass)

        if current_pass.ID <= last_logged_pass:
            found = True
            print("Last record found")
        else:        
            person = f_get_person_with_chip_id(table_person, current_pass.CIP)

            payload = ("{\n  \"datetime\": \"%s\",\n  \"studentName\": \"%s\",\n  \"studentSurname\": \"%s\",\n  \"recordId\": \"%s\",\n  \"chipId\": \"%s\"\n}"  \
                % (current_pass.Cas, f_decode_laf(person.Jmeno), f_decode_laf(person.Prijmeni), current_pass.ID, current_pass.CIP)).encode("utf-8")

            headers = {'content-type': 'application/json'}

            response = requests.request("POST", url=API_URL, data=payload, headers=headers)

            position_from_end += 1
            print("Inserted record")

    print("Going to sleep")
    time.sleep(10)
    main(table_passes[len(table_passes) - 1].ID)

if __name__ == "__main__":
    querystring = {"last":"1"}
    response = requests.request("GET", url=API_URL, data="", params=querystring)

    last_record = json.loads(response.text)

    main(int(last_record["recordId"]))

    # Wait for user to read output
    input("\nPress enter to continue...")
