import json
from watson_developer_cloud import VisualRecognitionV3

# BEGIN of python-dotenv section
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# END of python-dotenv section



##########################
### VISUAL RECOGNITION ###
##########################

def vr_open():
    """Opens a connection to Visual Recognition
    using credentials from .env file.

    Parameters
    ----------
    None

    Returns
    -------
    VisualRecognitionV3 : the connector from Watson API.
    """
    visual_recognition = VisualRecognitionV3(
        '2016-05-20',
        api_key=os.environ.get("VR_API_KEY")
        )
    return(visual_recognition)


def list_classifiers(vr_object):
    """Connects to Watson Visual Recognition
    and retrieves the list of custom classifiers.

    Parameters
    ----------
    vr_object : {VisualRecognitionV3} the connector to Visual Recognition (Watson API).

    Returns
    -------
    list : the list of classifiers ids.
    """
    json_data = vr_object.list_classifiers(verbose=True)

    if json_data is None:
        print("Error: connection not responding")
        return(None)

    if "classifiers" not in json_data.keys():
        print("Error: no listing available")
        return(None)

    id_list = []

    if len(json_data.get("classifiers",[])) == 0:
        print("There are no custom classifiers in your Visual Recognition component.")
        return(id_list)

    for clf in json_data.get("classifiers",[]):
        print("*** classifier id '{}'".format(clf['classifier_id']))
        id_list.append(clf['classifier_id'])
        print("classes: [ {} ]".format(", ".join([c['class'] for c in clf['classes']])))
        print("status: {}".format(clf['status']))

    return(id_list)


def delete_classifier(vr_object, classifier_id):
    """Connects to Watson Visual Recognition
    and deletes a given classifier.

    Parameters
    ----------
    vr_object : {VisualRecognitionV3} the connector to Visual Recognition (Watson API).
    classifiers_id : {str} the id of the classifier to delete.

    Returns
    -------
    dict : the JSON response from Watson
    """
    json_data = vr_object.delete_classifier(classifier_id=classifier_id)
    return(json_data)


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


########################
### APPLY CLASSIFIER ###
########################

def classify_image(vr_object, image_path, classifiers_id, threshold):
    """Classifies an image using Visual Recognition
    and outputs the set of detected classes.

    Parameters
    ----------
    image_path : {str} the path of the image to classify.
    vr_object : {VisualRecognitionV3} the connector to Visual Recognition (Watson API).
    classifiers_id : {str} the id of a classifier to apply (you can use 'default').

    Returns
    -------
    set : the set of classes ({str}) found in that image.
    """
    with open(image_path, 'rb') as image_file:
        response = vr_object.classify(  images_file=image_file,
                                        threshold=threshold,
                                        classifier_ids=[ classifiers_id ] )

    return(response)


def parse_classes(json_data):
    """Parses the JSON response given by Visual Recognition
    and outputs the set of detected classes in that response.

    Parameters
    ----------
    json_data : {dict} json response from VisualRecognition

    Returns
    -------
    set : the set of classes ({str}) found in that JSON response.

    Notes
    -----
    For an example of the JSON structure, see file 'pytest_data/classifier_output_1.json'
    """
    pass



################
### TRAINING ###
################


def find_training_zipfiles(root_dir):
    """Walks through a directory to find zip archives
    used as classes to train Visual Recognition.

    Parameters
    ----------
    root_dir: {str} the path to the directory to find zip archives.

    Returns
    -------
    list: a list of all the found zip archives, formatted as dict (see Notes).

    Notes
    -----
    Elements in the returned list are formatted as {dict}, with the following keys:
    - 'path': an {str} that indicates the path of the zip archive.
    - 'class': a {str} that provides the class of that archive (from zip file name).
    """
    training_sets = []
    for root, dirs, files in os.walk(root_dir):
        for file_str in files:
            if file_str.endswith(".zip"):
                zip_class = file_str.rstrip(".zip")
                zip_path = os.path.join(root, file_str)
                training_sets.append( {
                                        'class': zip_class,
                                        'path': zip_path
                                      } )
    return(training_sets)


def create_multiclass_classifier(vr_object, classifier_id, zip_archives):
    """Create a classifier from zip archives.

    Parameters
    ----------
    vr_object : {VisualRecognitionV3} the connector to Visual Recognition (Watson API).
    classifiers_id : {str} the name of the classifier to create.
    zip_archives: {list} of zip archives formatted as dictionaries.

    Returns
    -------
    None

    Notes
    -----
    Elements in zip_archives are formatted as {dict}, with the following keys:
    - 'path': an {str} that indicates the path of the zip archive.
    - 'class': a {str} that provides the class of that archive (from zip file name).
    """
    kwargs = {}
    for entry in zip_archives:
        kwarg_stringkey = "{}_positive_examples".format(entry['class'])
        kwargs_value = open(entry['path'], 'rb')
        kwargs[kwarg_stringkey] = kwargs_value

    ret_value = vr_object.create_classifier(classifier_id, **kwargs)
    print("Watson returned: {}".format(json.dumps(ret_value)))



###############
### TESTING ###
###############

def find_testing_images(root_dir):
    """Walks through a directory to find subdirs considered as classes,
    and images within these subdirs considered as testing examples
    for a Visual Recognition classifier.

    Parameters
    ----------
    root_dir: {str} the path to the directory to find subdirs/images.

    Returns
    -------
    list: a list of all the found images, formatted as dict (see Notes).

    Notes
    -----
    Elements in the returned list are formatted as {dict}, with the following keys:
    - 'path': an {str} that indicates the path of an image.
    - 'actual': a {set} that gives the actual class of that image (only one).
    """
    possible_extensions = [".jpg", ".jpeg"]
    image_list = []

    for dir_name, subdir_list, file_list in os.walk(root_dir, topdown=False):
        #print('Found subdir: {}'.format(dir_name))
        for file_name in file_list:
            for ext in possible_extensions:
                if file_name.lower().endswith(ext):
                    image_classes = { dir_name.split('/')[-1] }
                    image_path = os.path.join(dir_name, file_name)
                    image_list.append( {
                                         'path': image_path,
                                         'actual': image_classes
                                       } )
                    break

    return(image_list)


def measure_accuracy(image_entries):
    """Measure the accuracy on a given list of images.

    Parameters
    ----------
    image_entries: {list} of entries (dictionaries) giving for each image it's path,
                   it's actual class and predicted class (see Notes).

    Returns
    -------
    float: score for accuracy.

    Notes
    -----
    Elements in image_entries are formatted as {dict}, with the following keys:
    - 'path': an {str} that indicates the path of an image.
    - 'actual': a {set} that gives the actual class of that image (only one).
    - 'predicted': a {set} that gives the predicted class(es) of that image.
    """
    pass
