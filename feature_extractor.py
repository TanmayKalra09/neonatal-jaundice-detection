import cv2
import numpy as np

def extract_skin_roi_and_features(image_bgr_or_rgb, is_rgb=True):
    """
    Implements the skin detection and colorimetric feature extraction
    described in BioMedInformatics 2024 paper (Sections 2.3.1 & 2.3.2).
    
    1. Transforms to LAB color space.
    2. Applies Otsu thresholding and morphological operations to segment skin.
    3. Transforms to YCrCb and RGB color models.
    4. Computes mean values for red, green, blue, Y, cblue, and cred across skin pixels.
    """
    if is_rgb:
        img_rgb = image_bgr_or_rgb
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = image_bgr_or_rgb
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
    # Convert to LAB
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(img_lab)
    
    # Otsu thresholding on b-channel (blue-yellow spectrum) & a-channel (green-red)
    _, thresh_b = cv2.threshold(b_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, thresh_a = cv2.threshold(a_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    skin_mask = cv2.bitwise_and(thresh_b, thresh_a)
    
    # Morphological erosion and opening to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    
    # If mask is too small or empty, fall back to center crop / whole image
    if cv2.countNonZero(skin_mask) < 100:
        h, w = img_rgb.shape[:2]
        skin_mask = np.zeros((h, w), dtype=np.uint8)
        ch, cw = h // 4, w // 4
        skin_mask[ch:h-ch, cw:w-cw] = 255
        
    # Convert to YCrCb
    img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    Y = img_ycrcb[:, :, 0]
    Cr = img_ycrcb[:, :, 1]
    Cb = img_ycrcb[:, :, 2]
    
    R = img_rgb[:, :, 0]
    G = img_rgb[:, :, 1]
    B = img_rgb[:, :, 2]
    
    mask_indices = skin_mask > 0
    mean_r = float(np.mean(R[mask_indices]))
    mean_g = float(np.mean(G[mask_indices]))
    mean_b = float(np.mean(B[mask_indices]))
    mean_y = float(np.mean(Y[mask_indices]))
    mean_cb = float(np.mean(Cb[mask_indices]))
    mean_cr = float(np.mean(Cr[mask_indices]))
    
    # Segmented skin visualization
    segmented_skin = cv2.bitwise_and(img_rgb, img_rgb, mask=skin_mask)
    
    features = {
        'red': mean_r,
        'green': mean_g,
        'blue': mean_b,
        'Y': mean_y,
        'cblue': mean_cb,
        'cred': mean_cr
    }
    
    return features, skin_mask, segmented_skin
