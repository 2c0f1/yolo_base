from ultralytics import YOLO
import cv2,time

model = YOLO("yolov8n.pt") 
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
 success, frame = cap.read()
 results = model.predict(frame,conf=0.25)