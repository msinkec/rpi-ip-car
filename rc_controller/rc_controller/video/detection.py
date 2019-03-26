from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

import controls
import config

class BallDetector:

    def __init__(self):
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        #greenLower = (29, 86, 6)
        #greenUpper = (64, 255, 255)
        self.pts = deque(maxlen = 64)
         
        self.colorLower = (24, 48, 46)
        self.colorUpper = (81, 135, 122)

    def process_frame(self, frame):

        self.frame_dimens = frame.shape
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        #frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
     
        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 20:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                # Now we have all the data to send a command to the car
                self.react(center, radius)

        # update the points queue
        #self.pts.appendleft(center)
        
        # loop over the set of tracked points
        for i in range(1, len(self.pts)):
            # if either of the tracked points are None, ignore
            # them
            if self.pts[i - 1] is None or self.pts[i] is None:
                continue
     
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(512 / float(i + 1)) * 2.5)
            cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

        return frame
 
    def react(self, ball_location, radius):
        x_center = self.frame_dimens[0] / 2;
        x_delta = ball_location[0] - x_center

        commands = set()

        if radius < 400:
            commands.add('f')
            if x_delta < -200
                # Steer right and move forward
                commands.add('r')
                print('going right lel')
            if x_delta > 200:
                # Steer left and move forward
                commands.add('l')
                print('going left ZOMG')
        
        controls.execute(commands, config.controls_sock, config.car_addr, config.controls_port)
        
        
