import conversation_prompt
import pytest
import json


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


def test_parse_conversation_response():
    json_data = read_json_file('pytest_data/conversation_start.json')
    output = conversation_prompt.parse_conversation_response(json_data)
    assert type(output) is dict, "parse_conversation_response() should return a dict"
    assert "text" in output, "parse_conversation_response() should have a key 'text'"
    assert type(output['text']) is str, "key 'text' of output dict should contain a string"
    assert output['text'] == "Hi! How can I help you?", "when run on file 'pytest_data/conversation_start.json', text should be 'Hi! How can I help you?'"

    json_data = read_json_file('pytest_data/conversation_hello.json')
    output = conversation_prompt.parse_conversation_response(json_data)
    assert type(output) is dict, "parse_conversation_response() should return a dict"
    assert "text" in output, "parse_conversation_response() should have a key 'text'"
    assert type(output['text']) is str, "key 'text' of output dict should contain a string"
    assert output['text'] == "Hi ! Nice to meet you !\nMy name is Robot.", "when run on file 'pytest_data/conversation_hello.json', text should be 'Hi ! Nice to meet you !\\nMy name is Robot.'"
