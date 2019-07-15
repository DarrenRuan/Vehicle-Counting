import sys
sys.path.append('..')

import cv2
from blobs.blob2 import Blob


def csrt_create(bounding_box, frame, vehicle_type):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(bounding_box))
    blob = Blob(bounding_box, tracker, vehicle_type)
    return blob

def kcf_create(bounding_box, frame, vehicle_type):
    tracker = cv2.TrackerKCF_create()
    tracker.init(frame, tuple(bounding_box))
    blob = Blob(bounding_box, tracker, vehicle_type)
    return blob