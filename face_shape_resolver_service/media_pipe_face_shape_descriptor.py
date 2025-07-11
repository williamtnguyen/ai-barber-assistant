#!/usr/bin/env python3

import mediapipe as mp
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os


def describe_face_shape_localhost_mcp_tool(image_key: str):
    """
    For localhost demo purposes, the flow is simplified by:
    1. hackily downloading client face image in browser
    2. sending image key to web server and eventually MCP
    3. prefixing image key with absolute path to Downloads folder
    4. validate that image path exists
    4. describing the face
    """
    downloads_path = str(Path.home() / "Downloads")
    full_path = os.path.join(downloads_path, image_key)

    if os.path.exists(full_path):
        print(f"Found image at: {full_path}")
        return describe_face_shape(full_path)
    else:
        print(f"No image found at: {full_path}")
        return None


def describe_face_shape(image_path: str):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils

    # Read image
    image = cv2.imread(image_path)
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    # Initialize Face Mesh
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:
        
        # Process the image
        results = face_mesh.process(image_rgb)
        
        # Check if face detected
        if not results.multi_face_landmarks:
            print("No face detected!")
            return
        
        # Get the first face's landmarks
        face_landmarks = results.multi_face_landmarks[0]
        
        # Create a copy for visualization
        annotated_image = image_rgb.copy()
        
        # Draw the landmarks / face mesh
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,0,0), thickness=1)
        )

        # Extract key measurements
        landmarks = np.array([(lm.x * width, lm.y * height) for lm in face_landmarks.landmark])
        
        # Key facial points (using MediaPipe Face Mesh indices)
        # These points help determine face shape
        FACE_POINTS = {
            'chin': 152,
            'forehead': 10,
            'left_cheek': 234,
            'right_cheek': 454,
            'left_temple': 447,
            'right_temple': 227
        }

        # Calculate face measurements
        face_width = np.linalg.norm(landmarks[FACE_POINTS['left_cheek']] - landmarks[FACE_POINTS['right_cheek']])
        face_height = np.linalg.norm(landmarks[FACE_POINTS['chin']] - landmarks[FACE_POINTS['forehead']])
        jaw_width = np.linalg.norm(landmarks[FACE_POINTS['left_temple']] - landmarks[FACE_POINTS['right_temple']])
        
        # Calculate ratios
        height_width_ratio = face_height / face_width
        jaw_face_ratio = jaw_width / face_width

        # Determine face shape
        face_shape = determine_face_shape(height_width_ratio, jaw_face_ratio)

        # Visualize key points
        for point_name, point_idx in FACE_POINTS.items():
            cv2.circle(annotated_image, 
                      (int(landmarks[point_idx][0]), int(landmarks[point_idx][1])), 
                      5, (0, 255, 0), -1)

        return {
            'face_shape': face_shape,
            'measurements': {
                'height_width_ratio': height_width_ratio,
                'jaw_face_ratio': jaw_face_ratio,
                'face_width': face_width,
                'face_height': face_height
            },
            'annotated_image': annotated_image
        }        


def determine_face_shape(height_width_ratio, jaw_face_ratio):
    """
    Determine face shape based on ratios
    This is a simplified version - you might want to add more sophisticated logic
    """
    if height_width_ratio > 1.75:
        return "Oblong"
    elif height_width_ratio < 1.25:
        return "Round"
    elif jaw_face_ratio > 0.9:
        return "Square"
    elif jaw_face_ratio < 0.8:
        return "Heart"
    else:
        return "Oval"


def display_results(result):
    """Display the original image with annotations and measurements"""
    plt.figure(figsize=(12, 8))
    plt.imshow(result['annotated_image'])
    plt.title(f"Detected Face Shape: {result['face_shape']}")
    plt.axis('off')
    
    # Print measurements
    print("\nFace Measurements:")
    print(f"Detected Face Shape: {result['face_shape']}")
    print(f"Height/Width Ratio: {result['measurements']['height_width_ratio']:.2f}")
    print(f"Jaw/Face Ratio: {result['measurements']['jaw_face_ratio']:.2f}")
    print(f"Face Width: {result['measurements']['face_width']:.2f} pixels")
    print(f"Face Height: {result['measurements']['face_height']:.2f} pixels")
    
    plt.show()


def main():
    print("hello i'm about to try describing input face!!")
    for image_path in [
        # "test1.jpg",
        # "test2.jpg",
        "test3.jpg",
    ]:        
        result = describe_face_shape(image_path)
        if isinstance(result, str):
            print(result)  # Print error message if face not detected
        else:
            display_results(result)


if __name__ == "__main__":
    main()
