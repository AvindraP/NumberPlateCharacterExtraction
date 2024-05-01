import cv2
import pandas as pd
from ultralytics import YOLO
import os
import numpy as np
import preProcessor

model = YOLO('best.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  
        point = [x, y]
        print(point)
  
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Get the current working directory
current_directory = os.getcwd()

video_path = os.path.join(current_directory, 'Camera video footage', 'run.mp4')

# Create the video capture object using the relative path
cap = cv2.VideoCapture(video_path)

# Check if the video capture object was successfully created
if not cap.isOpened():
    print("Error: Could not open video file at path:", video_path)
else:
    print("Video file opened successfully:", video_path)

with open("coco1.txt", "r") as file:
    class_list = file.read().split("\n") 

if len(class_list) != 9:
    print("Error: class_list does not have 9 elements. Please check your coco1.txt file.")
    exit()

count = 0
numberplate_count = 0
YOUR_HORIZONTAL_LINE_Y_COORDINATE = 600
OUTPUT_RESOLUTION = (222, 80)

def calculate_rotation_angle(region):
    # Convert the region to grayscale
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    # Threshold the grayscale image to get a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(contours[0])
    
    # Calculate the angle of rotation needed to make the number plate region straight
    angle = np.arctan(h / w) * (15 / np.pi)
    
    return angle

def straighten_image(image):
    # Get the dimensions of the image
    h, w = image.shape[:2]
    
    # Define the coordinates of the corners of the number plate region
    x1, y1 = 0, 0
    x2, y2 = w, 0
    x3, y3 = w, h
    x4, y4 = 0, h

    # Define the source points for the perspective transformation
    src_points = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    # Define the destination points for the perspective transformation
    dst_points = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

    # Compute the perspective transformation matrix
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transformation to straighten the image
    straightened_image = cv2.warpPerspective(image, perspective_matrix, (w, h))

    return straightened_image

def convert_to_binary(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive threshold
    binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary_image

# Create the directory if it doesn't exist
output_dir = "violator"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

x_numberplate = None  # Initialize x_numberplate

while True:    
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1280, 720))

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        
        # Check if d is within the range of class_list
        if 0 <= d < len(class_list):
            c = class_list[d]

            if (y1 + y2) / 2 >= YOUR_HORIZONTAL_LINE_Y_COORDINATE:

                if c == "numberplate":
                    # Extract the region containing the number plate
                    region = frame[y1:y2, x1:x2]
                    
                    # Get the coordinates of the numberplate bounding box
                    x_numberplate = x1
                    y_numberplate = y1

                    # Straighten the region to make it straight
                    straightened_region = straighten_image(region)

                    binary_image = convert_to_binary(straightened_region)

                    # Resize the binary region to the desired output resolution
                    binary_image_resized = cv2.resize(binary_image, OUTPUT_RESOLUTION, interpolation=cv2.INTER_NEAREST)

                    # Save the resized and straightened region
                    numberplate_count += 1
                    cv2.imwrite(os.path.join(output_dir, f'numberplate{numberplate_count}.jpg'), binary_image_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                    image_path = os.path.join(output_dir, f'numberplate{numberplate_count}.jpg')
                    preProcessor.detect_numberplate(image_path)
                
                if c == "bikewithouthelmet" and x_numberplate is not None:
                    # Extract the region containing the "bikewithouthelmet" bounding box
                    bbox_region = frame[y1:y2, x1:x2]

                    if (x1 <= x_numberplate <= x2) and (y1 <= y_numberplate <= y2):

                        cv2.imwrite(os.path.join(output_dir, f'bikewithouthelmet_numberplate{numberplate_count}.jpg'), binary_image_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()