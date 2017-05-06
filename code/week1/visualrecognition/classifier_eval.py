# -*- coding: utf-8 -*-
import json
import argparse
import vr_func


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classifier", type=str, help="id of the classifier to apply (default is 'default')")
    parser.add_argument("-t", "--threshold", type=float, help="{float} threshold to use for classifier (defaut 0.5)")
    parser.add_argument("testdir", type=str, help="path to the test directory")
    args = parser.parse_args()

    # uncomment those below if you want to know what is given as an argument
    #print("classifier ids given as arguments: {}".format(args.classifier))

    if args.classifier is None:
        _vr_classifier_id = 'default'
    else:
        _vr_classifier_id = args.classifier

    if args.threshold is None:
        _threshold = 0.5
    else:
        _threshold = args.threshold

    # obtains the list of images in testing directory
    # formatted as dictionaries with key 'id' and 'actual'
    testing_image_list = vr_func.find_testing_images(args.testdir)
    print("testing on {} images found in {}.".format(len(testing_image_list), args.testdir))

    # obtains a connector to Watson V.R.
    vr_connector = vr_func.vr_open()

    # for each image in the list found in testing dir
    for entry in testing_image_list:
        # uses function to obtain set of classes
        json_response = vr_func.classify_image(vr_connector,
                                             entry['path'],
                                             _vr_classifier_id,
                                             _threshold)

        ret_classes = vr_func.parse_classes(json_response)

        entry['predicted'] = ret_classes

        # print for fun...
        print("*** image '{}'\nactual: {}\npredicted: {}".format(entry['path'], entry['actual'], entry['predicted']))

    # compute accuracy and print it
    print("accuracy: {}".format(vr_func.measure_accuracy(testing_image_list)))
