# Astrotime
Recreation of the astrotime boardgame for table top simulator published by Ravensburger (https://www.gesellschaftsspiele.de/ravensburger/astrotime/)


# Generation Files

In the card generation folder you find an executable python script and the cards.json file with the record for all cards in the game.

All cards have a unique identifier which acts as translation key and locator.

## cards.json Structure

|Powers|German|English|
|-|-|-|
|Red|Ansehen und Bewunderung|Reputation and Admiration|
|Yellow|Macht und Einfluss|Power and Influence |
|Green|Einkommen und Wohlstand|Income and Wealth|
|Blue|Sympathie und Freundschaft|Sympathy and Friendship|
|Grey|Harmonie und Familienglueck|Harmony and Family Happiness |
|Purple|Erfahrung und Wissen|Experience and Knowledge |

|Attributes|German|English|
|-|-|-|
|attr_0|Tatkraft|Vigor|
|attr_1|Ehrgeiz|Ambition|
|attr_2|Mut|Courage|
|attr_3|Durchsetzungsvermögen|Assertiveness|
|attr_4|Offenheit|Openness|
|attr_5|Ausdauer|Endurance|
|attr_6|Sachlickeit|Objectivity|
|attr_7|Urteilskraft|Judgement|
|attr_8|Sorgfalt|Diligence|
|attr_9|Zuverlaessigkeit|Reliability|
|attr_10|Kreativitaet|Creativity|
|attr_11|Redegabe|Eloquence|
|attr_12|Kontaktfreude|Sociability|
|attr_13|Diplomatie|Diplomacy|
|attr_14|Charme|Charme|
|attr_15|Gefühl|Empathy|
|attr_16|Phantasie|Fantasy|
|attr_17|Gemeinschaftssinn|Sense of community|
|attr_18|Idealismus|Idealism|
|attr_19|Toleranz|Tolerance|

## How to add a new card?

1) Add the new card metadata

Add an object to the `cards.json` file using the following template and set the attributes your card represents to `true`.
```json
    {
        "id": "<unique ID>",
        "red": false,
        "yellow": false,
        "green": false,
        "blue": false,
        "grey": false,
        "purple": false,
        "attr_0": false,
        "attr_1": false,
        "attr_2": false,
        "attr_3": false,
        "attr_4": false,
        "attr_5": false,
        "attr_6": false,
        "attr_7": false,
        "attr_8": false,
        "attr_9": false,
        "attr_10": false,
        "attr_11": false,
        "attr_12": false,
        "attr_13": false,
        "attr_14": false,
        "attr_15": false,
        "attr_16": false,
        "attr_17": false,
        "attr_18": false,
        "attr_19": false
    },
```
2) Add the text and translation

In the `locales` folder navigate inside the LC_MESSAGES folders for the language of your text and open the `base.po` file. 

Add two new lines for your card to the file like shown in the example below:
```m
msgid "card_<id>_title"
msgstr "Titel"
msgid "card_<id>_desc"
msgstr "Scenario Description for the card."
```

3) Compile and Generate new images

Follow the instructions in the [I18n Chapter](#i18n-and-localization) to generate the `.mo` file for all files you added texts for

Run the `generator.py` script using the following command. Python 3.8 is required to be installed.
```
python ./generator.py
```

# I18n and Localization
Gettext is used to provide the translation of all texts for the cards.
After modifying the .po files you need to convert them into their .mo representation.
.po to .mo file conversion is done using this online service https://po2mo.net/.

