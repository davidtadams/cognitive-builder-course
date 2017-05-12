# coding: utf-8
import json
import watson_developer_cloud

# BEGIN of python-dotenv section
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# END of python-dotenv section


discovery = watson_developer_cloud.DiscoveryV1(
    '2016-12-01',
    username=os.environ.get("DISCOVERY_USERNAME"),
    password=os.environ.get("DISCOVERY_PASSWORD")
    )

environment_id = os.environ.get("DISCOVERY_ENVIRONMENT_ID")
collection_id = os.environ.get("DISCOVERY_COLLECTION_ID")

def display_discovery_query_response(json_data):
    for entry in json_data['results']:
        print("*** [{}] {}".format( entry['score'],
                                    entry['title'] ))
        for keyword in entry['enriched_text']['keywords']:
            if keyword['sentiment']['type'] == 'positive':
                print("+ [{}]".format(keyword['text']))
            if keyword['sentiment']['type'] == 'negative':
                print("- [{}]".format(keyword['text']))


if __name__ == '__main__':
    while 1:
        # get some natural language query from user input
        input_content = input('Discovery NLQ> ')

        # use line below instead if you're in python 2
        # input_content = raw_input('Discovery NLQ> ').strip()

        # if you type one of these, you exit the script
        if (input_content.lower() in {'exit', 'quit', 'q', 'n'}):
            break


        query_options = { 'natural_language_query':input_content,
                          'count':10 }
        query_results = discovery.query(environment_id,
                                        collection_id,
                                        query_options)

        # dumping the raw JSON response
        print(json.dumps(query_results, indent=2))

        # printing the result from the parsing function
        print(display_discovery_query_response(query_results))
