import toneanalyzer
import pytest
import json


def test_parse_toneanalyzer_response():
    json_content = toneanalyzer.read_json_file("pytest_data/tones_1.json")
    expected_dict = {
                        "Anger":0.102932,
                        "Disgust":0.175853,
                        "Fear":0.091308,
                        "Joy":0.134345,
                        "Sadness":0.446459
                    }
    assert toneanalyzer.parse_toneanalyzer_response(json_content) == expected_dict, \
           "when run on file 'data/tones_1.json' should return {}".format(expected_dict)
