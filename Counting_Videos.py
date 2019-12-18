import sys
from argparse import ArgumentParser
import os

import cv2
import csv
from trackers.tracker import create_blob, add_new_blobs, remove_duplicates
import numpy as np
from collections import OrderedDict
from detectors.detector import get_bounding_boxes
import uuid
import os
import contextlib
from datetime import datetime
import argparse
from utils.detection_roi import get_roi_frame, draw_roi
from counter import get_counting_line, is_passed_counting_line

if __name__ == '__main__':
    current_wd = os.getcwd()
    if os.path.exists("./videos"):
        videos_list = os.listdir("./videos/")
        for video in videos_list:
            if ".mp4" in video:
                command_current = "python Vehicle_Counting.py "
                command_current += current_wd + "/videos/" + video
                command_current += " --clposition bottom --detector yolo --record --headless"
                print("Current Command:", command_current)
                sys.stdout.flush()

                os.system(command_current)
                print(video+" is done")
                sys.stdout.flush()
