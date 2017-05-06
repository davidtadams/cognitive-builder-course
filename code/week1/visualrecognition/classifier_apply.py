# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import VisualRecognitionV3
import argparse
import vr_func


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classifier", type=str, help="id of the classifier to apply (default is 'default')")
    parser.add_argument("-t", "--threshold", type=float, help="{float} threshold to use for classifier (defaut 0.5)")
    parser.add_argument("images", nargs="+", help="list of images to classify of images")
    args = parser.parse_args()

    # uncomment those below if you want to know what is given as an argument
    print("classifier ids given as arguments: {}".format(args.classifier))
    #print("images given as arguments: {}".format(args.images))

    # default value for classifier
    if args.classifier is None:
        _vr_classifier_id = 'default'
    else:
        _vr_classifier_id = args.classifier

    # default value for threshold
    if args.threshold is None:
        _threshold = 0.5
    else:
        _threshold = args.threshold


    # obtains a connector to Watson V.R.
    vr_connector = vr_func.vr_open()

    # for each image in the list given as argument of the script
    for image in args.images:
        # uses function to obtain set of classes
        ret_classes = vr_func.classify_image(vr_connector,
                                             image,
                                             _vr_classifier_id,
                                             _threshold)

        # you can comment that line below later
        print(json.dumps(ret_classes, indent=2))

        # and just print that...
        print("image '{}' classes: {}".format(image, vr_func.parse_classes(ret_classes)))
