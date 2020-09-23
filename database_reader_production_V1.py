from pypxlib import Table
import requests, time

# Replace Lafovi znaky
def f_decode_laf(text):
    text_string = str(text)

    laf_znaky = [
        "ý",
        "²",
        "°",
        "×",
        "Ú",
        "ß",
        "Þ",
        "Ý",
        "Ü",
        "╚",
        "¨",
        "è",
        "Ï",
        "┴",
        "═",
        "Ä",
        "╠",
        "¦",
        "╔",
    ]
    translated_znaky = [
        "ě",
        "ý",
        "ř",
        "ž",
        "é",
        "á",
        "č",
        "í",
        "š",
        "Č",
        "ů",
        "Š",
        "Ř",
        "Á",
        "Í",
        "Ž",
        "Ě",
        "Ý",
        "É",
    ]

    for original, translated in zip(laf_znaky, translated_znaky):
        text_string = text_string.replace(original, translated)

    return text_string


# Get row from table_person with chip_id
def f_get_person_with_chip_id(table_person, chip_id):
    chip_id = str(chip_id)
    for row in table_person:
        if row["Cip"] == chip_id:
            return row


# Post new data to API and repeat
def f_post_new_records_into_api(
    api_url, decode_with="", last_sent_id=0, log=False, timeout=20
):
    try:
        last_sent_id = int(last_sent_id)

        parse_table = Table("PRUCHODY.db")
        decoding_table = Table("OSOBY.db")

        found = False
        position_from_last_sent = 1

        last_record_id = len(parse_table) - 1
        last_pass = parse_table[last_record_id]

        if last_record_id == last_sent_id:
            if log:
                print("No new records found")
            return

        while not found:
            position = last_sent_id + position_from_last_sent
            current_pass = parse_table[position]

            if log:
                print("Current ID", current_pass.ID)
            if log:
                print("Last ID", last_sent_id)

            person = f_get_person_with_chip_id(
                decoding_table, current_pass[decode_with]
            )

            if person is None:
                person = {"Prijmeni": "None", "Jmeno": "None"}

            payload = (
                '{"datetime": "%s", "studentName": "%s", "studentSurname": "%s", "recordId": "%s", "direction": "%s", "turniketId": "%s", "chipId": "%s"}'
                % (
                    current_pass["Cas"],
                    f_decode_laf(person["Jmeno"]),
                    f_decode_laf(person["Prijmeni"]),
                    current_pass["ID"],
                    current_pass["Druh"],
                    current_pass["Terminal"],
                    current_pass["CIP"],
                )
            ).encode("utf-8")

            headers = {"content-type": "application/json"}

            response = requests.request(
                "POST", url=API_URL, data=payload, headers=headers, timeout=1
            )
            print(current_pass)
            print(response)

            position_from_last_sent += 1
            if log:
                print("Inserted record")

            if current_pass["ID"] == last_pass["ID"]:
                found = True
                if log:
                    print("Last record found")
            elif (current_pass["ID"] - last_sent_id) > 10000:
                found = True
                if log:
                    print("Maximum number of rows open. Closing them and restarting.")

        parse_table.close()
        decoding_table.close()

    except Exception as e:
        if log:
            print(
                f"Unexpected error {{{e}}}. Couldn't insert new data. Trying again in {timeout} seconds."
            )
        parse_table.close()
        decoding_table.close()

    if log:
        print("Going to sleep", end="\n\n")


# Get last record from API
def f_get_last_record():
    querystring = {"last": "1"}
    response = requests.request(
        "GET", url=API_URL, data="", params=querystring, timeout=1
    )
    return eval(response.text)


# Main function
def main(log=False, timeout=20):
    while True:
        try:
            last_record = f_get_last_record()
            if log:
                print(f"last_record sent is { last_record }")
            f_post_new_records_into_api(
                api_url=API_URL,
                decode_with="CIP",
                last_sent_id=last_record["recordId"],
                log=log,
                timeout=timeout,
            )

            if log:
                print(f"Going to sleep for { timeout } seconds.")
            time.sleep(timeout)
        except Exception as e:
            if log:
                print(
                    f"Unexpected error {{{e}}}. Failed in main function. Trying again in {timeout} seconds."
                )
            time.sleep(timeout)


if __name__ == "__main__":
    API_URL = "https://api.gymsp.it/passes"

    main(log=True, timeout=5)
