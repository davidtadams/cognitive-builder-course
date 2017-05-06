# -*- coding: utf-8 -*-
"""
"""
import json
from watson_developer_cloud import VisualRecognitionV3
import argparse
import vr_func

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classifier", help="the name of the classifier to create")
    parser.add_argument("traindir", help="path to the training directory to find zip archives")
    args = parser.parse_args()

    # default value if no classifier is specified
    if args.classifier is None:
        _clf_name = "cbc"
    else:
        _clf_name = args.classifier

    # find all zip archives in training dir
    zip_archives = vr_func.find_training_zipfiles(args.traindir)

    print("creating classifier '{}' based on zip files {}".format(_clf_name,
                                                                  zip_archives))

    # obtains a connector to Watson V.R.
    vr_connector = vr_func.vr_open()

    # calls function to create classifier using V.R.
    vr_func.create_multiclass_classifier(vr_connector, _clf_name, zip_archives)
