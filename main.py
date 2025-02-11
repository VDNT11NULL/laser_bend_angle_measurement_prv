import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_bends_and_angles(image_path, debug=True, final_res=False):
    """
    Detect bends and calculate angles relative to horizontal.
    """
    # Step 1: Load and preprocess the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if debug:
        display_step("1. Original Image", gray)

    # Step 2: Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    if debug:
        display_step("2. Blurred Image", blurred)

    # Step 3: Perform edge detection
    edges = cv2.Canny(blurred, 30, 150)
    if debug:
        display_step("3. Edge Detection", edges)

    # Step 4: Dilate edges
    kernel = np.ones((2, 2), np.uint8)
    # kernel = np.ones((1, 1), np.uint8)
    # kernel = np.ones((5, 5), np.uint8)

    # kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    if debug:
        display_step("4. Dilated Edges", dilated)

    # Step 5: Detect parallel lines and identify bends
    height, width = dilated.shape
    lines = cv2.HoughLinesP(
        dilated, rho=1, theta=np.pi/180, threshold=50, minLineLength=50, maxLineGap=20
    )
    
    bend_points = []
    if lines is not None:
        # Organize line segments and analyze gaps
        segments = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x1 > x2:  
              # Ensure lines are sorted right-to-left
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            segments.append((x1, y1, x2, y2))

        # Sort segments by x-coordinate (right-to-left)
        segments.sort(key=lambda seg: seg[0], reverse=True)

        # Detect bends based on gaps and rectangle shrinking
        for i in range(len(segments) - 1):
            x1, y1, x2, y2 = segments[i]
            x1_next, y1_next, x2_next, y2_next = segments[i + 1]

            if abs(x1 - x1_next) < 10 and abs(y1 - y1_next) < 10:
                bend_points.append((x1, y1))
    
    # Step 6: Calculate angles between bends
    angles = []
    for i in range(len(bend_points) - 1):
        x1, y1 = bend_points[i]
        x2, y2 = bend_points[i + 1]
        dx, dy = x2 - x1, y2 - y1
        angle = np.arctan2(dy, dx) * 180 / np.pi
        angle = angle if angle >= 0 else angle + 180  
        angles.append((bend_points[i], angle))

    if debug or final_res:
        result_img = image.copy()
        for i, (x, y) in enumerate(bend_points):
            cv2.circle(result_img, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(
                result_img, f"Bend {chr(65 + i)}", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1
            )
        for (x, y), angle in angles:
            cv2.putText(
                result_img, f"{angle:.1f}°", (x, y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )
        display_step("Detected Bends and Angles", result_img, is_gray=False)

    return bend_points, angles


def display_step(title, image, is_gray=True):
    """Helper function to display images with titles."""
    plt.figure(figsize=(12, 6))
    if is_gray:
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()


image_paths = [
    # "/home/vdnt/Documents/Chanakya_Fellowship/Initial_images/processed_JPG/1b_crop.png",
    # "/home/vdnt/Documents/Chanakya_Fellowship/Initial_images/processed_JPG/1b_crop_new.png",
    # "/home/vdnt/Documents/Chanakya_Fellowship/Initial_images/processed_JPG/7feb_00.png",
    # "/home/vdnt/Documents/Chanakya_Fellowship/Initial_images/processed_JPG/whatsapp_.png",
    # "/home/vdnt/Documents/Chanakya_Fellowship/Initial_images/processed_JPG/image11.png"
  #update file paths
]
for image_path in image_paths:
    bend_points, angles = detect_bends_and_angles(image_path, debug=False, final_res=True)
    for i, ((x, y), angle) in enumerate(angles):
        print(f"Bend {chr(65 + i)} at ({x}, {y}): {angle:.1f}°")
