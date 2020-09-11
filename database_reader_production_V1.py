from pypxlib import Table
import requests, time


# Replace Lafovi znaky
def f_decode_laf(text):
    text_string = str(text)

    laf_znaky = ["ý", "²", "°", "×", "Ú", "ß", "Þ", "Ý", "Ü", "╚", "¨", "è", "Ï", "┴", "═", "Ä", "╠", "¦", "╔"]
    translated_znaky = ["ě", "ý", "ř", "ž", "é", "á", "č", "í", "š", "Č", "ů", "Š", "Ř", "Á", "Í", "Ž", "Ě", "Ý", "É"]

    for original, translated in zip(laf_znaky, translated_znaky):
        text_string = text_string.replace(original, translated)

    return(text_string)

# Get row from table_person with chip_id
def f_get_person_with_chip_id(table_person, chip_id):
    chip_id = str(chip_id)
    for row in table_person:
        if row["Cip"] == chip_id:
            return(row)

# Post new data to API and repeat
def f_post_new_records_into_api(api_url, decode_with="", last_sent_id=0, log=False):
    last_sent_id = int(last_sent_id)

    parse_table = Table("PRUCHODY.db")
    decoding_table = Table("OSOBY.db")

    found = False
    position_from_end = 1

    while(not found):
        position = len(parse_table) - position_from_end
        current_pass = parse_table[position]

        if log: print("Current ID", current_pass.ID)
        if log: print("Last ID", last_sent_id)

        if current_pass.ID <= last_sent_id:
            found = True
            if log: print("Last record found")
        else:
            person = f_get_person_with_chip_id(decoding_table, current_pass[decode_with])

            payload = ("{\"datetime\": \"%s\", \"studentName\": \"%s\", \"studentSurname\": \"%s\", \"recordId\": \"%s\", \"chipId\": \"%s\"}"  \
                % (current_pass.Cas, f_decode_laf(person.Jmeno), f_decode_laf(person.Prijmeni), current_pass.ID, current_pass.CIP)).encode("utf-8")

            headers = {'content-type': 'application/json'}

            response = requests.request("POST", url=API_URL, data=payload, headers=headers)
            print(response)

            position_from_end += 1
            if log: print("Inserted record")

    if log: print("Going to sleep", end='\n\n')

if __name__ == "__main__":
    API_URL = "https://api.gymsp.it/passes"

    def f_get_last_record():
        querystring = {"last":"1"}
        response = requests.request("GET", url=API_URL, data="", params=querystring)
        return (eval(response.text))

    #table_passes = Table("PRUCHODY.db")
    #table_person = Table("OSOBY.db")
    try:
        while (True):
            try:
                last_record = f_get_last_record()
                f_post_new_records_into_api(api_url=API_URL, decode_with="CIP", last_sent_id=last_record["recordId"], log=True)
            except:
                print("Error reading database or posting to API")
                print("Prosíme kontaktujte vývojáře")
            time.sleep(20)
    except:
        print("\n\n\n\n\n")
        print("Prosíme kontaktujte vývojáře")

    # Wait for user to read output
    input("\nPress enter to continue...")
