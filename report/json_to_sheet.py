import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# https://docs.google.com/spreadsheets/d/1-0fv_nIuK0wz2Hn9KOu6FFzI2nvTAL9znSd9Annrugc/edit?usp=sharing
# python json_to_sheet.py <jsonファイル名> 
# <jsonファイル名> : ファイル名をマルウェアと同じ名前にする ex) mimikatz.json
# pip install gspread oauth2client

def next_available_row(sheet1):
    str_list = list(filter(None, sheet1.col_values(2)))
    return str(len(str_list)+1)

def next_available_column(sheet1):
    str_list = list(filter(None, sheet1.row_values(7)))
    return str(len(str_list)+2)

def read_json_file(file_path):
    json_open = open(file_path, 'r')
    json_load = json.load(json_open)
    return json_load

def read_spreadsheet(file):
    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(file).sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)
    next_row = next_available_row(sheet)
    next_column = next_available_column(sheet)
    print(next_row, next_column)
    sheet.update_cell(next_column, 1, "I just wrote to a spreadsheet using Python!")

def write_spreadsheet(file, jf):
    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(file).sheet1

    # Extract and print all of the values
    next_row = next_available_row(sheet)
    next_column = next_available_column(sheet)

    print(next_column)
    # sheet.update_cell(next_column, 1, sys.argv[1])

    is_first = True

    for l in jf:
        if is_first:
            lst =[sys.argv[1], "", "", "", "", l["eventrecid"], l["totalscore"]["totalscore"],l["totalscore"]["results"]["detect_iex"],l["totalscore"]["results"]["detect_sign"],l["totalscore"]["results"]["unreadable_string"],l["totalscore"]["results"]["detect_strings_blacklist"],l["totalscore"]["results"]["extract_url"],l["totalscore"]["results"]["logistic_reg"]]
            is_first = False
        else:
            lst =["", "", "", "", "", l["eventrecid"], l["totalscore"]["totalscore"],l["totalscore"]["results"]["detect_iex"],l["totalscore"]["results"]["detect_sign"],l["totalscore"]["results"]["unreadable_string"],l["totalscore"]["results"]["detect_strings_blacklist"],l["totalscore"]["results"]["extract_url"],l["totalscore"]["results"]["logistic_reg"]]
        sheet.append_row(lst)
        # next_column = str(int(next_column) + 1)
    return

def main():
    if len(sys.argv) < 2:
        print("usage : python json_to_sheet.py <jsonファイル名>")
        exit()
    print(sys.argv[1])
    # jsonファイル読込み
    jf = read_json_file(sys.argv[1])
    # spreadsheet書き込み
    write_spreadsheet("z9_results", jf)

if __name__ == "__main__":
    main()

