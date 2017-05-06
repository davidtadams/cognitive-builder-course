# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import ToneAnalyzerV3


# BEGIN of python-dotenv section
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# END of python-dotenv section


tone_analyzer = ToneAnalyzerV3(
   username=os.environ.get("TONE_USERNAME"),
   password=os.environ.get("TONE_PASSWORD"),
   version='2016-05-19')


def read_json_file(file_path):
    """Reads and parse a json file.

    Parameters
    ----------
    file_path : {str} the path to the json file.

    Returns
    -------
    dict : a dictionary containing the json structure read from the file.
    """
    with open(file_path) as json_file:
        json_content = json_file.read()
        json_data = json.loads(json_content)

    return(json_data)


def parse_toneanalyzer_response(json_data):
    """Parses the JSON response from ToneAnalyzer to return
    a dictionary of emotions and their corresponding score.

    Parameters
    ----------
    json_data: {dict} a json response from ToneAnalyzer (see Notes)

    Returns
    -------
    dict : a {dict} whose keys are emotion ids and values are their corresponding score.

    Notes
    -----
    for an example of json see type pytest_data/tones_1.json
    """
    return_value = {}
    for category in json_data["document_tone"]["tone_categories"]:
        if category["category_id"] == "emotion_tone":
            for tone in category["tones"]:
                return_value[tone["tone_name"]] = tone["score"]
    return return_value


if __name__ == '__main__':
    while 1:
        # get some sentence from user input
        input_content = input('ToneAnalyzer> ')

        # use line below instead if you're in python 2
        # input_content = raw_input('ToneAnalyzer>').strip()

        # if you type one of these, you exit the script
        if (input_content.lower() in {'exit', 'quit', 'q', 'n'}):
            break


        # ask ToneAnalyzer to analyse the input
        json_response = tone_analyzer.tone(text=input_content)

        # dumping the raw JSON response
        print(json.dumps(json_response, indent=2))

        # printing the result from the parsing function
        print(parse_toneanalyzer_response(json_response))
