import cv2,time
from ultralytics import YOLO

ptime=0

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    ctime = time.time() 
    fps = 1//(ctime-ptime)
    ptime = ctime

    if success:
        # Run YOLOv8 inference on the frame
        #results = model(frame,conf=0.25)
        results = model.predict(frame,conf=0.25)
        #print(model.fuse())
        #print(model.info)     
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        #print()
        #print(str(results[0]))
        # Display the annotated frame
        cv2.UMat(cv2.putText(annotated_frame,f'fps:{int(fps)}',(10,55),cv2.FONT_HERSHEY_TRIPLEX,1,(0,160,28))) 
        cv2.imshow("YOLOv8", annotated_frame)
        
        
        #debug
        
        #print(str(results))
        #names = model.names
        #print(names())        
        #boxes = results[0].boxes   
        #print(str(boxes))    
        #for result in results:
        # boxes = result.boxes  # Boxes object for bbox outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        # probs = result.probs  # Class probabilities for classification outputs
        # print('resultados')
        # print(result)
        
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()