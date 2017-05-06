import json_code
import pytest


def test_simple_tdd_function():
    assert json_code.simple_tdd_function(1,2) == 3, "sum of 1 and 2 should be 3"
    assert json_code.simple_tdd_function(-1,1) == 0, "sum of -1 and 1 should be 0"
    assert json_code.simple_tdd_function(-3,2) == -1, "sum of -3 and 2 should be -1"
    with pytest.raises(TypeError,
                       message="when adding an int and a char, raises a TypeError"):
        json_code.simple_tdd_function(1, 'a')


def test_read_json_file():
    ret_value = json_code.read_json_file("data/paper.json")

    # the return value should be a dict
    assert type(ret_value) == dict, \
           "read_json_file() should return a dict"

    # test on an example file, check for a given key
    assert "Authors" in ret_value, \
           "run on file 'data/paper.json', the returned dict should have a key 'Authors'"

    # when file does not exist, should raise exception
    with pytest.raises(FileNotFoundError,
                       message="Expecting FileNotFoundError when run on 'data/notfound.json'"):
        json_code.read_json_file("data/notfound.json")

    # when file is not json, should raise exception
    with pytest.raises(ValueError,
                       message="when run on a file that is NOT json ('data/notjson.txt'), should raise ValueError"):
        json_code.read_json_file("data/notjson.txt")


def test_course_weeks_count():
    json_content = json_code.read_json_file('data/course_1_full.json')
    assert json_code.course_weeks_count(json_content) == 5, \
           "when run on 'data/course_1_full.json' should return 5"

    json_content = json_code.read_json_file('data/course_3_fail.json')
    assert json_code.course_weeks_count(json_content) == 0, \
           "when json has no 'weeks' key, should return 0"


def test_course_content_count():
    json_content = json_code.read_json_file('data/course_1_full.json')
    ret_value = json_code.course_content_count(json_content)
    assert ret_value == { 'precourse' : 3, 'week 1' : 2, 'week 2' : 2 }, \
           "when run on 'data/course_1_full.json' should return { 'precourse' : 3, 'week 1' : 2, 'week 2' : 2 }"

    json_content = json_code.read_json_file('data/course_2_trunc.json')
    ret_value = json_code.course_content_count(json_content)
    assert ret_value == { 'week 1' : 3 }, \
           "when run on 'data/course_2_trunc.json' should return { 'week 1' : 3 }"

    json_content = json_code.read_json_file('data/course_3_fail.json')
    ret_value = json_code.course_content_count(json_content)
    assert ret_value == { }, \
           "when run on 'data/course_3_fail.json' should return an empty dict {}"


def test_tones_parse_anger():
    json_content = json_code.read_json_file("data/tones_1.json")
    assert json_code.tones_parse_anger(json_content) == 0.102932, \
           "when run on file 'data/tones_1.json' should find 0.102932"

    json_content = json_code.read_json_file("data/tones_2.json")
    assert json_code.tones_parse_anger(json_content) == 0.057571, \
           "when run on file 'data/tones_2.json' should find 0.057571.\
           do you know 'Anger' is not necessarily the first in its list?"

    json_content = json_code.read_json_file("data/tones_3.json")
    assert json_code.tones_parse_anger(json_content) == 0.040993, \
           "when run on file 'data/tones_3.json' should find 0.040993.\
           be aware that emotions are not necessarily the first in order in the 'tone_categories' list"

    json_content = json_code.read_json_file("data/tones_4_fail.json")
    assert json_code.tones_parse_anger(json_content) == 0.0, \
           "when run on file 'data/tones_4_fail.json' should find 0.0.\
           note: in this file there is no anger."

    json_content = json_code.read_json_file("data/tones_5_fail.json")
    assert json_code.tones_parse_anger(json_content) == 0.0, \
           "when run on file 'data/tones_5_fail.json' should find 0.0.\
           note: in this file there are no emotional tones."
