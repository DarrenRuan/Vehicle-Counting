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

from Vehicle_Counting import VehicleCounter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mcdf', type=int, default=2, help='maximum consecutive detection failures \
                        i.e number of detection failures before it\'s concluded that \
                        an object is no longer in the frame')
    parser.add_argument('--mctf', type=int, default=3, help='maximum consecutive tracking failures \
                        i.e number of tracking failures before the tracker concludes \
                        the tracked object has left the frame')
    parser.add_argument('--di', type=int, default=10, help='detection interval i.e number of frames \
                        before detection is carried out again (in order to find new vehicles \
                        and update the trackers of old ones)')
    parser.add_argument('--detector', default='yolo', help='select a model/algorithm to use for vehicle detection \
                        (options: yolo, haarc, bgsub, ssd, tfoda | default: yolo)')
    parser.add_argument('--tracker', default='kcf', help='select a model/algorithm to use for vehicle tracking \
                        (options: csrt, kcf, camshift | default: kcf)')
    parser.add_argument('--clposition', help='position of counting line (options: top, bottom, \
                        left, right | default: bottom)')


    args = parser.parse_args()
    for i in range(32):
        video_dir = 'I:\\01 Computer Vision\\04_June_2018\\Hamburg_Hall1_050101062018\\ffmpeg-20190706-feade2b-win64-static\\bin\\'+'Hamburg_Hall1_050101062018_' + "{:03}".format(i) + ".mp4"
        # capture traffic scene video
        cap = cv2.VideoCapture(video_dir)
        if not cap.isOpened():
            sys.exit('Error capturing video.')
        ret, frame = cap.read()
        f_height, f_width, _ = frame.shape

        detector = args.detector
        tracker = args.tracker
        mcdf = args.mcdf
        print('args.mcdf', args.mcdf)
        mctf = args.mctf
        di = args.di

        droi = [(0, 0), (f_width, 0), (f_width, f_height), (0, f_height)]

        vehicle_counter = VehicleCounter(frame, detector, tracker, droi, False, mcdf, mctf, di, args.clposition)

        record_flag = True

        if record_flag:
            csv_file_name = 'counting.csv'
            with open(csv_file_name, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Name", "Number Of Vehicles"])

        # main loop
        print('VCS running...')
        while cap.get(cv2.CAP_PROP_POS_FRAMES) + 1 < cap.get(cv2.CAP_PROP_FRAME_COUNT):
            if ret:
                log = vehicle_counter.count(frame)
                output_frame = vehicle_counter.visualize()

            ret, frame = cap.read()
        print(video_dir, log)

    # end capture, close window, close log file and video object if any
    cap.release()
    print('End of video.')
