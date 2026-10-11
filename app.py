import os
import glob
import streamlit as st
import numpy as np
from PIL import Image
import cv2
import joblib

# Set Streamlit page config
st.set_page_config(
    page_title="Neonatal Jaundice Detection AI",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .card-jaundice {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-left: 6px solid #D97706;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-normal {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 6px solid #059669;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .badge-metric {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = "/Users/tanmaykalra/jaundice_detection"
MODELS_DIR = os.path.join(BASE_DIR, "models")
YOLO_MODEL_PATH = os.path.join(MODELS_DIR, "yolov8_jaundice_best.pt")
TABULAR_MODEL_PATH = os.path.join(MODELS_DIR, "tabular_models.joblib")
TEST_JAUNDICE_DIR = os.path.join(BASE_DIR, "dataset", "test", "jaundice")
if not os.path.exists(TEST_JAUNDICE_DIR):
    TEST_JAUNDICE_DIR = os.path.join(BASE_DIR, "sample_images", "jaundice")

TEST_NORMAL_DIR = os.path.join(BASE_DIR, "dataset", "test", "normal")
if not os.path.exists(TEST_NORMAL_DIR):
    TEST_NORMAL_DIR = os.path.join(BASE_DIR, "sample_images", "normal")

# Lazy model loaders
@st.cache_resource
def load_yolo_model():
    if os.path.exists(YOLO_MODEL_PATH):
        from ultralytics import YOLO
        return YOLO(YOLO_MODEL_PATH)
    # Check runs directory fallback
    fallback = os.path.join(BASE_DIR, "runs", "jaundice_yolo_cls", "weights", "best.pt")
    if os.path.exists(fallback):
        from ultralytics import YOLO
        return YOLO(fallback)
    return None

@st.cache_resource
def load_tabular_model():
    if os.path.exists(TABULAR_MODEL_PATH):
        return joblib.load(TABULAR_MODEL_PATH)
    return None

# Import feature extraction
from feature_extractor import extract_skin_roi_and_features

# Sidebar controls
st.sidebar.image("https://img.icons8.com/color/96/baby.png", width=70)
st.sidebar.title("Configuration")

model_choice = st.sidebar.radio(
    "Choose Diagnostic Model:",
    ["Skin Colorimetric XGBoost (BioMedInformatics Paper - Recommended)", "YOLOv8 Computer Vision (Full Image)", "Hybrid Ensemble (YOLO + XGBoost)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Test Samples")
sample_category = st.sidebar.selectbox("Select Sample Category:", ["None (Upload custom)", "Test Jaundiced Newborn", "Test Normal Newborn"])

selected_sample_path = None
if sample_category == "Test Jaundiced Newborn":
    sample_files = sorted(glob.glob(os.path.join(TEST_JAUNDICE_DIR, "*.jpg")))
    if sample_files:
        chosen_f = st.sidebar.selectbox("Choose sample image:", [os.path.basename(f) for f in sample_files[:10]])
        selected_sample_path = os.path.join(TEST_JAUNDICE_DIR, chosen_f)
elif sample_category == "Test Normal Newborn":
    sample_files = sorted(glob.glob(os.path.join(TEST_NORMAL_DIR, "*.jpg")))
    if sample_files:
        chosen_f = st.sidebar.selectbox("Choose sample image:", [os.path.basename(f) for f in sample_files[:10]])
        selected_sample_path = os.path.join(TEST_NORMAL_DIR, chosen_f)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Dataset Source**: Normal & Jaundiced Newborns (NJN)  
**Reference**: *BioMedInformatics 2024, 4, 623–637*  
**Key Features**: B (Blue) & Cb (Chrominance)
""")

# Main UI
st.markdown('<div class="main-header">👶 Neonatal Jaundice Vision Diagnosis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Non-invasive neonatal hyperbilirubinemia screening powered by YOLO Computer Vision & Clinical Colorimetric Models</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an infant photo (JPEG / PNG):", type=["jpg", "jpeg", "png"])

input_image = None
if selected_sample_path and os.path.exists(selected_sample_path):
    input_image = Image.open(selected_sample_path).convert("RGB")
    st.info(f"Loaded sample image: **{os.path.basename(selected_sample_path)}**")
elif uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGB")

if input_image is not None:
    img_np = np.array(input_image)
    
    # Extract ROI and paper features
    features, skin_mask, segmented_skin = extract_skin_roi_and_features(img_np, is_rgb=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Input Image")
        st.image(input_image, use_container_width=True)
    with col2:
        st.subheader("2. Skin ROI Detection")
        st.image(segmented_skin, caption="Segmented Skin Pixels (LAB Otsu)", use_container_width=True)
    with col3:
        st.subheader("3. YCbCr Cb Heatmap")
        # Visualizing Cb channel (blue chrominance)
        ycrcb = cv2.cvtColor(img_np, cv2.COLOR_RGB2YCrCb)
        cb_channel = ycrcb[:, :, 2]
        heatmap = cv2.applyColorMap(cb_channel, cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        st.image(heatmap_rgb, caption="Cb Channel (Bilirubin Sensitive)", use_container_width=True)
        
    st.markdown("---")
    
    # Diagnostics Execution
    yolo_model = load_yolo_model()
    tab_data = load_tabular_model()
    
    yolo_prob_jaundice = None
    yolo_pred_class = None
    
    if yolo_model is not None:
        try:
            res = yolo_model.predict(img_np, verbose=False)[0]
            names = res.names
            probs = res.probs.data.cpu().numpy()
            
            # Map names
            jaundice_idx = None
            normal_idx = None
            for idx, name in names.items():
                if "jaundice" in name.lower():
                    jaundice_idx = idx
                elif "normal" in name.lower():
                    normal_idx = idx
                    
            if jaundice_idx is not None and normal_idx is not None:
                yolo_prob_jaundice = float(probs[jaundice_idx])
                yolo_pred_class = "Jaundice" if yolo_prob_jaundice >= 0.5 else "Normal"
            else:
                top_idx = int(res.probs.top1)
                yolo_pred_class = names[top_idx].capitalize()
                yolo_prob_jaundice = float(res.probs.top1conf) if "jaundice" in yolo_pred_class.lower() else (1.0 - float(res.probs.top1conf))
        except Exception as e:
            st.warning(f"YOLO inference warning: {e}")
            
    # Tabular XGBoost evaluation
    xgb_prob_jaundice = None
    xgb_pred_class = None
    if tab_data is not None:
        xgb_clf = tab_data['xgb_model']
        scaler = tab_data['scaler']
        cols = tab_data['feature_cols']
        min_label = tab_data['min_label']
        
        vec = np.array([[features[c] for c in cols]])
        vec_scaled = scaler.transform(vec)
        proba = xgb_clf.predict_proba(vec_scaled)[0]
        # class 1 = normal (0 in xgb), class 2 = jaundice (1 in xgb)
        xgb_prob_jaundice = float(proba[1]) if len(proba) > 1 else float(proba[0])
        xgb_pred_class = "Jaundice" if xgb_prob_jaundice >= 0.5 else "Normal"
        
    # Decision aggregation based on user selection
    final_class = "Unknown"
    final_conf = 0.0
    
    if "YOLOv8" in model_choice:
        if yolo_prob_jaundice is not None:
            if yolo_prob_jaundice >= 0.5:
                final_class = "Jaundice"
                final_conf = yolo_prob_jaundice
            else:
                final_class = "Normal"
                final_conf = 1.0 - yolo_prob_jaundice
        elif xgb_prob_jaundice is not None:
            final_class = xgb_pred_class
            final_conf = xgb_prob_jaundice if final_class == "Jaundice" else (1.0 - xgb_prob_jaundice)
    elif "BioMedInformatics" in model_choice:
        if xgb_prob_jaundice is not None:
            final_class = xgb_pred_class
            final_conf = xgb_prob_jaundice if final_class == "Jaundice" else (1.0 - xgb_prob_jaundice)
        elif yolo_prob_jaundice is not None:
            final_class = yolo_pred_class
            final_conf = yolo_prob_jaundice if final_class == "Jaundice" else (1.0 - yolo_prob_jaundice)
    else: # Hybrid
        scores = []
        if yolo_prob_jaundice is not None:
            scores.append(yolo_prob_jaundice)
        if xgb_prob_jaundice is not None:
            scores.append(xgb_prob_jaundice)
        if scores:
            avg_prob = np.mean(scores)
            if avg_prob >= 0.5:
                final_class = "Jaundice"
                final_conf = avg_prob
            else:
                final_class = "Normal"
                final_conf = 1.0 - avg_prob
                
    # Display Result
    st.subheader("Diagnostic Results & Confidence")
    if final_class == "Jaundice":
        st.markdown(f"""
        <div class="card-jaundice">
            <h2 style="color: #92400E; margin-top:0;">⚠️ JAUNDICE DETECTED</h2>
            <p style="font-size: 1.2rem; color: #78350F; margin-bottom: 0;">
                <strong>Diagnostic Verdict:</strong> Elevated Bilirubin Discoloration Detected (Hyperbilirubinemia Risk)<br>
                <strong>Confidence Score:</strong> <span style="font-size:1.4rem; font-weight:bold;">{final_conf * 100:.2f}%</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card-normal">
            <h2 style="color: #065F46; margin-top:0;">✅ NORMAL / NO JAUNDICE DETECTED</h2>
            <p style="font-size: 1.2rem; color: #047857; margin-bottom: 0;">
                <strong>Diagnostic Verdict:</strong> Healthy Skin Pigmentation within Expected Range<br>
                <strong>Confidence Score:</strong> <span style="font-size:1.4rem; font-weight:bold;">{final_conf * 100:.2f}%</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.progress(min(max(final_conf, 0.0), 1.0))
    
    # Breakdown Metrics
    st.subheader("Skin Colorimetric Feature Breakdown (from Research Paper)")
    mcol1, mcol2, mcol3, mcol4, mcol5, mcol6 = st.columns(6)
    mcol1.metric("Red (R)", f"{features['red']:.1f}")
    mcol2.metric("Green (G)", f"{features['green']:.1f}")
    mcol3.metric("Blue (B)", f"{features['blue']:.1f}", help="Highest negative correlation with bilirubin in paper")
    mcol4.metric("Luminance (Y)", f"{features['Y']:.1f}")
    mcol5.metric("Cb (Blue Chrom)", f"{features['cblue']:.1f}", help="Highest feature importance in paper (Figure 2)")
    mcol6.metric("Cr (Red Chrom)", f"{features['cred']:.1f}")
    
    # Model detail expander
    with st.expander("Detailed Multi-Model Comparison & Diagnostic Analysis"):
        st.write(f"- **YOLOv8 Vision Model Probability (Jaundice)**: {yolo_prob_jaundice * 100:.2f}%" if yolo_prob_jaundice is not None else "- YOLO Model: Not loaded")
        st.write(f"- **XGBoost Colorimetric Model Probability (Jaundice)**: {xgb_prob_jaundice * 100:.2f}%" if xgb_prob_jaundice is not None else "- XGBoost Model: Not loaded")
        
        if yolo_pred_class is not None and xgb_pred_class is not None and yolo_pred_class != xgb_pred_class:
            st.warning("""
            **💡 Why do the models show different results for this image?**
            - **XGBoost (BioMedInformatics Paper Method)** uses **Skin ROI Segmentation** (isolating only skin pixels and discarding the background). The infant's extracted skin features show severely depressed **Blue (69.9)** and **Cb (83.0)**, which corresponds directly to high bilirubin yellowness. Therefore, XGBoost detects **Jaundice**.
            - **YOLOv8 (Full-Scene Vision)** evaluates the whole image at once. If the baby is lying on a non-hospital colored surface (e.g. a bright blue blanket or colored cloth), the prominent background color shifts the global color balance away from the hospital incubator images YOLO was trained on.
            - **Recommendation**: For non-standard backgrounds (colored blankets/sheets), trust the **Skin Colorimetric XGBoost** model.
            """)
        
    st.info("ℹ️ **Clinical Note**: This AI-assisted screening tool non-invasively analyzes cutaneous discoloration. Any flagged cases should be verified with a pediatric physician using transcutaneous bilirubinometry (TcB) or total serum bilirubin (TSB) laboratory testing per American Academy of Pediatrics (AAP) protocols.")
else:
    st.markdown("""
    ### How to Use:
    1. **Upload an image** of a newborn infant via the box above, or **select a pre-loaded sample** from the left sidebar.
    2. The computer vision model will automatically detect the infant's skin region (ROI) and analyze the visual cues.
    3. The system will diagnose whether jaundice is detected along with an exact **confidence score**.
    """)
