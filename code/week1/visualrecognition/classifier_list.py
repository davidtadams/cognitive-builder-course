# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import VisualRecognitionV3
import vr_func

if (__name__ == "__main__"):
    # obtains a connector to Watson V.R.
    vr_connector = vr_func.vr_open()

    # displays and returns a list of custom classifiers
    classifier_list = vr_func.list_classifiers(vr_connector)
