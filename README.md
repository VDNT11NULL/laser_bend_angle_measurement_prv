

# Detecting Bends and Measuring Angles in Metal Strips Using Image Processing Techniques

## Introduction

This project focuses on detecting bends in metal strips captured through laser detection in individual image frames and measuring the angles formed at these bends. The aim is to analyze metal strips for quality control by identifying the bend points and measuring the acute angles relative to a horizontal line. 

Key observations and hypotheses include:
1. **Regions Between Bends:** Bends are regions where the strip deviates significantly. As we move from right to left, bends mark the transition between regions.
2. **Rectangular Edges Frequency:** The detected rectangular edges become smaller as we move leftward into newer regions between bends.
3. **Fixed Continuous White Regions:** Bend points are identified by fixed, continuous white regions with zero or minimal gaps between the detected parallel edges of the strip.

This document explains the theoretical basis and working of each image processing technique used in the pipeline.

---

## Approach

### 1. **Loading and Preprocessing**
- The first step involves reading the image and converting it to grayscale for uniform intensity-based processing.  
  **Why grayscale?**  
  Grayscale simplifies image analysis by reducing color channels, focusing solely on intensity variations, which are crucial for detecting edges and bends.
![alt text](image-1.png)
### 2. **Blurring**
- **Technique:** Gaussian Blur (applied with a kernel size of 7x7).  
  **Purpose:** To smoothen the image, reducing noise and minor irregularities. This ensures that edge detection focuses on significant edges rather than noise.  
  **How it works:** Gaussian blur applies a weighted average of pixel intensities in a neighborhood, where closer pixels have higher weights (based on a Gaussian distribution).
![alt text](image-2.png)
---

### 3. **Edge Detection**
- **Technique:** Canny Edge Detection.
  **Purpose:** To detect edges by identifying intensity gradients in the image.  
  **Steps:**
  1. **Gradient Calculation:** The image gradient (change in pixel intensity) is computed in both horizontal (x) and vertical (y) directions.
  2. **Non-Maximum Suppression:** Thin out detected edges by suppressing non-maximum gradients, ensuring only the most prominent edges remain.
  3. **Double Thresholding:** Classify edges as strong, weak, or irrelevant based on gradient magnitude. Weak edges connected to strong edges are retained; the rest are discarded.
![alt text](image-3.png)
---

### 4. **Dilating Edges**
- **Technique:** Dilation with a 3x3 kernel.  
  **Purpose:** To thicken detected edges, ensuring connectivity between edge segments that represent bends.  
  **How it works:** Each pixel in the edge-detected image is replaced by the maximum pixel value within the kernel's neighborhood, effectively broadening the edges.
![alt text](image-4.png)
---

### 5. **Line Detection**
- **Technique:** Hough Line Transform.  
  **Purpose:** To detect straight lines by mapping points in Cartesian space to lines in Hough space.  
  **How it works:** 
  - Each point in the Cartesian plane can represent a line in Hough space (parameterized by distance `ρ` from the origin and angle `θ`).
  - Peaks in Hough space represent lines that pass through the most points in the original image.
![alt text](image-5.png)
---

![alt text](image.png)

### 6. **Bend Detection**
- **Observation-Based Insights for Bend Points:**
  - **Fixed White Regions:** At bend points, the detected edges form continuous, fixed white regions with little to no gaps. These regions signify strong alignment of parallel edges at bends.
  - **Rectangular Edge Shrinkage:** As we move leftward (across regions), the size of detected rectangular edges decreases progressively, correlating with structural differences across the strip.

**Algorithmic Approach:**
1. **Right-to-Left Scanning:** Line segments are extracted, ensuring that x-coordinates decrease (right to left), aligning with the direction of analysis.
2. **Clustering Line Segments:** Line segments are clustered based on proximity along the x-axis. This groups related edges within a single region or bend.
3. **Finding Bend Points:** The rightmost point of each cluster is considered a bend. 
   - At each bend, the intersection between the strip's horizontal base and the elevated line joining consecutive bends is calculated.

---

### 7. **Angle Calculation**
- **Technique:** Trigonometric Calculation of Angles.
  **Purpose:** To measure the acute angle formed by the horizontal line (x-axis) and the elevated line joining consecutive bend points.
  **How it works:**
  - For two bend points (B1 and B2), the angle θ is calculated using:
    \[
    \text{θ} = \arctan\left(\frac{y_2 - y_1}{x_2 - x_1}\right) \cdot \frac{180}{\pi}
    \]
  - Adjustments ensure θ remains in the range [0°, 90°] as acute angles are the focus.

---

### 8. **Visualizations**
- **Line Visualization:** Line segments are drawn over the detected edges to visualize the detected structure of the strip.  
- **Bend Points Marking:** Bend points are marked on the strip, labeled with the detected acute angles.  
- **Angle Histogram:** A histogram of detected angles is plotted, highlighting the frequency distribution of various angles in the strip.

---

## Observations and Findings

### 1. **Bend Characteristics**
- Bends are located at points where continuous white regions (detected parallel edges) are observed with minimal or zero gaps. These regions signify abrupt changes in the strip's direction.

### 2. **Region Characteristics**
- As we move leftward across bends:
  - Detected rectangular edges become smaller, reflecting structural narrowing in the strip.
  - This size reduction provides a supplementary cue for identifying regions between bends.

### 3. **Acute Angles**
- Acute angles between consecutive bends provide insights into the sharpness of bends. This measurement helps assess the quality and structural integrity of the metal strip.

---

## Techniques and Their Importance

| **Technique**           | **Purpose**                                                                                         |
|--------------------------|-----------------------------------------------------------------------------------------------------|
| **Gaussian Blur**        | Smoothens the image, reducing noise to improve edge detection accuracy.                             |
| **Canny Edge Detection** | Detects prominent edges by focusing on intensity gradients.                                         |
| **Dilated Edges**        | Ensures connectivity of fragmented edges, aiding in robust line and bend detection.                 |
| **Hough Line Transform** | Identifies straight lines in the image, crucial for analyzing the strip's structure and bends.      |
| **Clustering**           | Groups related edges, isolating distinct regions or bends.                                         |
| **Trigonometry**         | Measures angles formed by consecutive bends, quantifying sharpness.                                |

---



## Conclusion

This project combines image processing and geometric analysis to effectively detect bends in metal strips and measure their acute angles. The approach is grounded in key observations about the strip's structural behavior, such as continuous white regions and decreasing rectangular edge sizes across bends. Future improvements could include automating the pipeline for real-time analysis in industrial settings.

--- 
