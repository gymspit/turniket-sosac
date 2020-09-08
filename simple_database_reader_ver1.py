from pypxlib import Table

# Replace Lafovi znaky
def lafprint(text):
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

    print(text_string)

# Print last n passes
def f_print_last_n_passes(table_passes, num_from_end):
    for i in range(num_from_end):
        line = i - num_from_end
        print(table_passes[line])

# Get row from table_person with chip_id
def f_print_person_with_chip_id(table_person, chip_id):
    chip_id = str(chip_id)
    for row in table_person:
        if row["Cip"] == chip_id:
            lafprint(row)

# Main
def main():
    table_passes = Table("PRUCHODY.db")
    table_person = Table("OSOBY.db")


    num_passes = int(input("How many last passes do you want to see? "))
    #num_passes = 1
    f_print_last_n_passes(table_passes, num_passes)

    print("\n")

    chip_id = "0000015730731300"
    f_print_person_with_chip_id(table_person, chip_id)

if __name__ == "__main__":
    main()

    # Wait for user to read output
    input("\nPress enter to continue...")
