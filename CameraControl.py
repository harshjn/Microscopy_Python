# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:38:35 2024

@author: Leica-Admin
"""

from pypylon import pylon
import cv2
import numpy as np
import os

#os.chdir
VideoFileName = 'live_view_500.avi'
FrameRate = 100.0
# Connect to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Open the camera
camera.Open()

# Set ROI (Region of Interest)
roi_width, roi_height = 500, 500
camera.Width.SetValue(roi_width)
camera.Height.SetValue(roi_height)
camera.OffsetX.SetValue(00)
camera.OffsetY.SetValue(00)

# Set the frame rate to the desired value
camera.AcquisitionFrameRateEnable.SetValue(True)
camera.AcquisitionFrameRate.SetValue(FrameRate)

# Set initial exposure time
initial_exposure_time = 10000  # in microseconds (10ms)
camera.ExposureTime.SetValue(initial_exposure_time)

# Print current settings for verification
print(f"Width: {camera.Width.GetValue()}")
print(f"Height: {camera.Height.GetValue()}")
print(f"OffsetX: {camera.OffsetX.GetValue()}")
print(f"OffsetY: {camera.OffsetY.GetValue()}")
print(f"Frame Rate: {camera.AcquisitionFrameRate.GetValue()}")
print(f"Exposure Time: {camera.ExposureTime.GetValue()}")

# Start grabbing imagesq
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Set up image converter
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Create an OpenCV window
cv2.namedWindow('Basler Camera Live View', cv2.WINDOW_NORMAL)

# Create a VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(VideoFileName, fourcc, 20.0, (1920, 1080))

# Function to update exposure time from trackbar
def update_exposure(val):
    exposure_time = max(1, val)  # ensure exposure time is at least 1 microsecond
    camera.ExposureTime.SetValue(exposure_time)
    print(f"Updated Exposure Time: {camera.ExposureTime.GetValue()}")

# Create a trackbar for exposure time
cv2.createTrackbar('Exposure Time', 'Basler Camera Live View', initial_exposure_time, 100000, update_exposure)

try:
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        
        if grabResult.GrabSucceeded():
            # Convert image to OpenCV format
            image = converter.Convert(grabResult)
            img = image.GetArray()
            
            # Check if the image is valid
            if img is not None:
                # Display the image using OpenCV
                cv2.imshow('Basler Camera Live View', img)
                
                # Save the frame to the video file
                out.write(img)
                
                # Break the loop if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Warning: Received an empty frame.")

        else:
            print("Error: Failed to grab image.")

        grabResult.Release()

finally:
    # Stop grabbing and close the camera
    camera.StopGrabbing()
    camera.Close()

    # Release the VideoWriter object
    out.release()

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()
