# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import VisualRecognitionV3
import vr_func
import argparse

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="id of the classifier to delete")
    args = parser.parse_args()

    # obtains a connector to Watson V.R.
    vr_connector = vr_func.vr_open()

    # displays a list of custom classifiers
    vr_func.delete_classifier(vr_connector, args.id)
