import vr_func
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



# {  "custom_classes": 0,  "images": [{  "classifiers": [{  "classes": [{  "class": "street",  "score": 0.846,  "type_hierarchy": "/road/street"},{  "class": "road",  "score": 0.85},{  "class": "yellow color",  "score": 0.872},{  "class": "green color",  "score": 0.702}  ],  "classifier_id": "default",  "name": "default"}  ],  "image": "images/parisstreets/paris-streets-1.jpg"}  ],  "images_processed": 1}


"""def test_classify_image():
    vr_obj = vr_func.vr_open()
    ret_value = vr_func.classify_image(vr_obj,
                                          'pytest_data/0.jpg',
                                          'default',
                                          0.1)

    assert ret_value is not None, "value returned by vr_classify_image should not be None."
    assert type(ret_value) == set, "value returned by vr_classify_image should be a set."
    assert len(ret_value) > 0, "when run on 'testing/parisstreets/paris-streets-1.jpg' should not return an empty set."
"""

def test_parse_classes():
    data = read_json_file('pytest_data/classifier_output_1.json')

    assert vr_func.parse_classes(data) == {'street','road','yellow color','green color'}, \
        "when run on file 'pytest_data/classifier_output_1.json', should return {'street','road','yellow color','green color'}"


def test_measure_accuracy():
    image_list = [
        { 'path':'1.jpg', 'actual':{'dog'}, 'predicted':{'dog'} },
        { 'path':'2.jpg', 'actual':{'dog'}, 'predicted':{'cat'} },
        { 'path':'3.jpg', 'actual':{'cat'}, 'predicted':{'cat'} },
        { 'path':'4.jpg', 'actual':{'cat'}, 'predicted':{'dog'} },
        { 'path':'5.jpg', 'actual':{'dog'}, 'predicted':{'dog'} }
    ]
    assert vr_func.measure_accuracy(image_list) == 0.6, "when run on course example, should return 0.6"
