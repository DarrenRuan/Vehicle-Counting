# Video-based Vehicle Counting System
Original Project https://github.com/nicholaskajoh/Vehicle-Counting

Note: The difference between these two projects:
1. Current project could count different types of vehicles (YOLO).
2. You could specify the position of your counter line: `./counter.py`
3. How to get the positions of Region of Interest?
By MATLAB:
Original Image:
![](original_image.jpg)
roipoly:
![](image_ROI.jpg)
4. TODO: And more trackers: cv2.TrackerBoosting_create(), cv2.TrackerMIL_create(), cv2.TrackerTLD_create(), cv2.TrackerMedianFlow_create(), cv2.TrackerGOTURN_create(), cv2.TrackerMOSSE_create()
Tutorial: https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
5. TODO: Integrate tensorflow_object_counting_api(https://github.com/ahmetozlu/tensorflow_object_counting_api)
6. TODO: Make Tracker: CamShift work properly. There might be something wrong with this tracker.

![](Hamburg_Hall.jpg)

## Setup
- Clone this repo `git@github.com:DarrenRuan/Vehicle-Counting.git`.
- Create and/or use a virtual environment.
- Run `pip install -r requirements.txt` to install dependencies.

## Run

### Configuration
```
usage: Vehicle_Counting.py [-h] [--iscam] [--droi DROI] [--showdroi]
                           [--mcdf MCDF] [--mctf MCTF] [--di DI]
                           [--detector DETECTOR] [--tracker TRACKER]
                           [--record] [--headless] [--clposition CLPOSITION]
                           video

positional arguments:
  video                 relative/absolute path to video or camera input of
                        traffic scene

optional arguments:
  -h, --help            show this help message and exit
  --iscam               specify if video capture is from a camera
  --droi DROI           specify a detection region of interest (ROI) i.e a set
                        of vertices that represent the area (polygon) where
                        you want detections to be made (format:
                        1,2|3,4|5,6|7,8|9,10 default: 0,0|frame_width,0|frame_
                        width,frame_height|0,frame_height [i.e the whole video
                        frame])
  --showdroi            display/overlay the detection roi on the video
  --mcdf MCDF           maximum consecutive detection failures i.e number of
                        detection failures before it's concluded that an
                        object is no longer in the frame
  --mctf MCTF           maximum consecutive tracking failures i.e number of
                        tracking failures before the tracker concludes the
                        tracked object has left the frame
  --di DI               detection interval i.e number of frames before
                        detection is carried out again (in order to find new
                        vehicles and update the trackers of old ones)
  --detector DETECTOR   select a model/algorithm to use for vehicle detection
                        (options: yolo, haarc, bgsub, ssd, tfoda | default:
                        yolo)
  --tracker TRACKER     select a model/algorithm to use for vehicle tracking
                        (options: csrt, kcf, camshift | default: kcf)
  --record              record video and vehicle count logs
  --headless            run VCS without UI display
  --clposition CLPOSITION
                        position of counting line (options: top, bottom, left,
                        right | default: bottom)
```

### Notes
- To use the `yolo` detector, download the [YOLO v3 weights](https://pjreddie.com/media/files/yolov3.weights) and place it in the [detectors/yolo folder](/detectors/yolo).
- To use the `ssd` detector, download this [pre-trained model](https://drive.google.com/file/d/0BzKzrI_SkD1_WVVTSmQxU0dVRzA/view) and place it in the [detectors/ssd folder](/detectors/ssd).
- To use the `tfoda` detector (i.e Tensorflow Object Detection API), copy [detectors/tfoda/.env.example](/detectors/tfoda/.env.example) to detectors/tfoda/.env and edit as appropriate. You can try out this detector [with these pre-trained models](https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API#use-existing-config-file-for-your-model).

### Examples
Use defaults:

```
python Vehicle_Counting.py "./videos/sample_traffic_scene.mp4"
```

Custom configuration:

```
python Vehicle_Counting.py "./videos/sample_traffic_scene.mp4" --droi "750,400|1150,400|1850,700|1850,1050|500,1050" --showdroi --detector "haarc" --tracker "csrt" --di 5 --mctf 15
```

YOLOv3 + KCF + Bottom Counter Line + Record
```
python Vehicle_Counting.py "./videos/sample_traffic_scene.mp4" --clposition bottom --detector yolo --record
```

With camera input:

```
python Vehicle_Counting.py 1 --iscam
```

__NB:__ You can press the `s` key when the program is running to capture a screenshot. The images are saved in the [screenshots folder](/screenshots).

## How it works
The vehicle counting system is made up of three main components: 
1. a detector <br>
Input: a frame from a certain video or an image <br>
Output: the locations of bounding boxes and the types of those bounding boxes <br>
2. a tracker <br>
Input: a new frame <br>
Output: a new bounding box for each object <br>
3. a counter <br>
Input: centroid and the position of the counting line <br>
Output: whether a bounding box passed the line or not <br>

The detector identifies vehicles in a given frame of video and returns a list of bounding boxes and a list of vehicles types around the vehicles to the tracker. The tracker uses the bounding boxes to track the vehicles in subsequent frames. The detector is also used to update trackers periodically to ensure that they are still tracking the vehicles correctly. The counter draws a counting lines across the road. When a vehicle crosses the line, the vehicle count is incremented.
