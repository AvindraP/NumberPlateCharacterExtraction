import os
import numpy as np
from skimage import io, filters, morphology, measure, transform
import pickle
import cv2
import pandas as pd
import myEmail
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from io import BytesIO  # Import BytesIO from the io module

# Define the scopes required for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authorize_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def load_svm_model_from_drive(creds, svm_model_id):
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=svm_model_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    svm_model = pickle.load(fh)
    return svm_model

def load_svm_model():
    creds = authorize_google_drive()
    svm_model_id = '15sgJHY50oFKPzhzYXJ_ceri6_Jh8FOwN'
    svm_model = load_svm_model_from_drive(creds, svm_model_id)
    return svm_model

# Load the SVM model
svm_model = load_svm_model()

# Define the scopes required for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate and authorize Google Drive access
def authorize_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Load the SVM model from Google Drive
def load_svm_model_from_drive(creds, svm_model_id):
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=svm_model_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    svm_model = pickle.load(fh)
    return svm_model

def load_svm_model():
    creds = authorize_google_drive()
    svm_model_id = '15sgJHY50oFKPzhzYXJ_ceri6_Jh8FOwN'
    svm_model = load_svm_model_from_drive(creds, svm_model_id)
    return svm_model

svm_model = load_svm_model()

label_mapping = {'1': 6,'Y': 4,'F': 3,'B': 1,'8': 0,'7': 5,'5': 2}

def find_bounding_box_and_crop(image, max_aspect_ratio=5):
    inverted_image = 1 - image
    label_image = measure.label(inverted_image)
    regions = measure.regionprops(label_image)
    max_area = 0
    max_bbox = None
    for region in regions:
        if region.area > max_area and region.major_axis_length / region.minor_axis_length < max_aspect_ratio:
            max_area = region.area
            max_bbox = region.bbox
    min_row, min_col, max_row, max_col = max_bbox
    cropped_image = image[min_row:max_row, min_col:max_col]
    return cropped_image

def delete_outer_black_areas(image):
    inner_black_mask = morphology.binary_erosion(image)
    outer_black_mask = image & ~inner_black_mask
    cleaned_image = image.copy()
    cleaned_image[outer_black_mask] = 1
    return cleaned_image

def angle_image(image, angle_degrees):
    transformation_matrix = transform.AffineTransform(rotation=np.deg2rad(angle_degrees))
    angled_image = transform.warp(image, transformation_matrix)
    return angled_image

def flood_fill(image, row, col):
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < image.shape[0] and 0 <= c < image.shape[1] and image[r, c] == 0:
            image[r, c] = 1
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))

def replace_consecutive_zeros(image, threshold=30):
    cleaned_image = image.copy()
    for row in range(cleaned_image.shape[0]):
        count = 0
        for col in range(cleaned_image.shape[1]):
            if cleaned_image[row, col] == 0:
                count += 1
                if count >= threshold:
                    cleaned_image[row, col - count + 1:col + 1] = 1
                    for r in range(row, -1, -1):
                        if cleaned_image[r, col] == 0:
                            flood_fill(cleaned_image, r, col)
                        else:
                            break
                    for r in range(row + 1, cleaned_image.shape[0]):
                        if cleaned_image[r, col] == 0:
                            flood_fill(cleaned_image, r, col)
                        else:
                            break
            else:
                count = 0
    return cleaned_image

def save_character_matrix(character_image, filename):
    resized_character_image = transform.resize(character_image, (50, 50), anti_aliasing=False)
    np.savetxt(filename, resized_character_image.astype(int), fmt='%d')

def detect_numberplate(image_path):
    
    image = io.imread(image_path, as_gray=True)
    cropped_image = find_bounding_box_and_crop(image)
    cleaned_image = delete_outer_black_areas(cropped_image)
    angled_image = angle_image(cleaned_image, angle_degrees=2)
    binary_image = angled_image > filters.threshold_otsu(angled_image)
    cleaned_binary_image = replace_consecutive_zeros(binary_image)
    label_image = measure.label(cleaned_binary_image == 0)
    num_characters = np.max(label_image)
    
    predicted_number = ""

    regions = measure.regionprops(label_image)
    sorted_regions = sorted(regions, key=lambda region: region.bbox[1])
    for i, region in enumerate(sorted_regions):
        if region.area < 200:
            cleaned_binary_image[label_image == region.label] = 1
        else:
            character_matrix = cleaned_binary_image.copy()
            character_matrix[label_image != region.label] = 1
            min_row, min_col, max_row, max_col = region.bbox
            character_matrix = character_matrix[min_row:max_row, min_col:max_col]
            save_character_matrix(character_matrix, f'character_{i + 1}.txt')
            new_matrix = np.loadtxt(f'character_{i + 1}.txt').flatten()
            predicted_character_index = svm_model.predict([new_matrix])[0]
            predicted_character = list(label_mapping.keys())[list(label_mapping.values()).index(predicted_character_index)]
            predicted_number += predicted_character
    
    print("Predicted Numberplate:", predicted_number)

    myEmail.searchVehicleNumber(predicted_number)
    myEmail.saveViolator(predicted_number)
    return predicted_number

    # ======= ED =======