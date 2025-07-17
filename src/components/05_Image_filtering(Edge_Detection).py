import cv2
import sys
import numpy

PREVIEW  = 0  # Preview Mode
BLUR     = 1  # Blurring Filter
FEATURES = 2  # Corner Feature Detector
CANNY    = 3  # Canny Edge Detector

feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)
# Find up to 500 sharp corners, which are at least 15 pixels apart, using a 9x9 pixel neighborhood, and only return corners with quality ≥ 20% of the best one.

# So when you set qualityLevel = 0.1, OpenCV looks at all the pixels' corner scores, takes the maximum score, and filters out any that are below 10% of that max(explained more clearly below in the goodfeaturestoteack section).

# The corner score is how OpenCV ranks and decides which points are worth keeping.


# What is cv2.goodFeaturesToTrack()?
# This is OpenCV’s implementation of the Shi-Tomasi Corner Detection algorithm.

# 📌 It does:
# Finds the best N corner points in a grayscale image

# Used as a feature extractor before tracking or matching (e.g., Lucas-Kanade optical flow, SLAM, etc.)


s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

image_filter = PREVIEW
alive = True

win_name = "Camera Filters"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

source = cv2.VideoCapture(s)

while alive:
    has_frame, frame = source.read()
    if not has_frame:
        break

    frame = cv2.flip(frame, 1)

    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 80, 150)
    elif image_filter == BLUR:
        result = cv2.blur(frame, (13, 13))
        # It applies an 'average blurring' filter to an image. 
        # Blurring is a convolution operation where each pixel’s value is replaced by a weighted average of its neighboring pixels.
        # Types: 
        # Greater the kernel higher the blurring
        # 🟦 Average Blur (cv2.blur)
        # 📌 Description: Simple mean of pixel values in the kernel

        # ✅ Best Used For:
        # Basic smoothing
        # Removing uniform noise
        # Privacy blur
        # 🟨 Gaussian Blur (cv2.GaussianBlur)
        # 📌 Description: Weighted average (center pixels have more influence)
        # ✅ Best Used For:
        # Preprocessing for edge detection
        # Noise reduction
        # Creating soft blur effects
        # 🟩 Median Blur (cv2.medianBlur)
        # 📌 Description: Takes median of surrounding pixels (instead of mean)
        # ✅ Best Used For:
        # Removing salt-and-pepper noise
        # Preserving edges better than average blur
        # 🟥 Bilateral Filter (cv2.bilateralFilter)
        # 📌 Description: Blurs only similar pixels, preserving edges
        # ✅ Best Used For:
        # Beautifying portraits
        # Edge-preserving smoothing
        # Cartoonization
        # ⚪ Box Filter (cv2.boxFilter)
        # 📌 Description: Like average blur, but with more control over padding and normalization
        # ✅ Best Used For:
        # Efficient approximation of average blur
        # When custom padding behavior is needed
        # ⚫ Motion Blur (custom kernel)
        # 📌 Description: Simulates directional motion blur using a custom kernel
        # ✅ Best Used For:
        # Creating motion effects
        # Simulating fast-moving subjects
        
    elif image_filter == FEATURES:
        result = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        # Returns a numpy array.So if 120 corners are detected, shape = (120, 1, 2)
# The ** is called the "dictionary unpacking operator".
# 🔍 In short:
# It takes a dictionary and unpacks it into keyword arguments (key=value) when passed to a function.
        # Corners are places in the image where intensity changes sharply in multiple directions. The corner score tells us how strong this behavior is at each pixel
        # ✅ 1. Harris Corner Detection
        # Harris uses a structure tensor matrix to compute the score.

        # 💡 Formula:
        # python
        # Copy
        # Edit
        # R = det(M) - k * (trace(M))^2
        # Where:

        # M = matrix of image gradients (captures local changes in intensity)

        # det(M) = determinant of M (measures intensity variation)

        # trace(M) = sum of diagonal of M

        # k = sensitivity constant (usually ~0.04–0.06)

        # 💥 Interpretation:
        # If R is very large and positive → Strong corner

        # If R is small or negative → Edge or flat region

        # ✅ 2. Shi-Tomasi Corner Detection (goodFeaturesToTrack)
        # Shi-Tomasi improves on Harris by using the minimum eigenvalue of the matrix M.

        # 💡 Formula:
        # python
        # Copy
        # Edit
        # score = min(eigenvalue1, eigenvalue2)
        # Where:

        # The eigenvalues of M represent gradient changes in 2 directions

        # If both eigenvalues are large, it's a corner

        # If only one is large → it's an edge

        # If both are small → flat region

        # This score is used directly as the "corner score" in cv2.goodFeaturesToTrack().
        if corners is not None:
            for x, y in numpy.float32(corners).reshape(-1, 2):
            # Reshapes into : [ [x1, y1],  
            #                   [x2, y2], ... ]
                cv2.circle(result, (x, y), 10, (0, 255, 0), 1)
            # x,y is the center , 10 is the radius, then green color and then the thickness of the circle.
    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR
    elif key == ord("F") or key == ord("f"):
        image_filter = FEATURES
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

source.release()
cv2.destroyWindow(win_name)