
import csv
import json
from pandas import *

ROWS = 12
COLUMNS = 'A:AC'


def load():

    result_json = []
    result_i18n = []

    df = read_excel('Cards_DE.xlsx', usecols=COLUMNS,
                    nrows=ROWS)

    for _, row in df.iterrows():
        generate_cards_json(row, result_json)
        generate_i18n_files(row, result_i18n)

    with open('imported_json.json', 'w') as f:
        json.dump(result_json, f)

    with open('imported_i18n.po', 'w') as f:
        f.write('\n'.join(result_i18n))


def generate_cards_json(row, result_json: list):
    card = {}
    card['id'] = row['Nummer']
    card['red'] = row['Rot'] == 1
    card['yellow'] = row['Gelb'] == 1
    card['green'] = row['Gruen'] == 1
    card['blue'] = row['Blau'] == 1
    card['grey'] = row['Grau'] == 1
    card['purple'] = row['Violett'] == 1
    card['attr_0'] = row['Tatkraft'] == 1
    card['attr_1'] = row['Ehrgeiz'] == 1
    card['attr_2'] = row['Durchsetzg'] == 1
    card['attr_3'] = row['Offenheit'] == 1
    card['attr_4'] = row['Kreativitaet'] == 1
    card['attr_5'] = row['Ausdauer'] == 1
    card['attr_6'] = row['Sachlichk'] == 1
    card['attr_7'] = row['Urteilskr'] == 1
    card['attr_8'] = row['Sorgfalt'] == 1
    card['attr_9'] = row['Zuverlkeit'] == 1
    card['attr_10'] = row['Kreativitaet'] == 1
    card['attr_11'] = row['Redegabe'] == 1
    card['attr_12'] = row['Kontaktfr'] == 1
    card['attr_13'] = row['Diplomatie'] == 1
    card['attr_14'] = row['Charme'] == 1
    card['attr_15'] = row['Gefuehl'] == 1
    card['attr_16'] = row['Phantasie'] == 1
    card['attr_17'] = row['Gemsinn'] == 1
    card['attr_18'] = row['Idealismus'] == 1
    card['attr_19'] = row['Toleranz'] == 1
    result_json.append(card)


def generate_i18n_files(row, result_i18n: list):
    id = row['Nummer']
    result_i18n.append('msgid "card_' + str(id) + '_title"')
    result_i18n.append('msgstr "' + row['Titel'] + '"')
    result_i18n.append('msgid "card_' + str(id) + '_desc"')
    result_i18n.append('msgstr "' + row['Text'] + '"')
    result_i18n.append('')


load()
