# 👶 Neonatal Jaundice Vision Diagnosis System

[![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](http://localhost:8501)
[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8--cls-00FFFF?style=for-the-badge&logo=Ultralytics&logoColor=black)](https://ultralytics.com)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-EB5424?style=for-the-badge&logo=XGBoost&logoColor=white)](https://xgboost.readthedocs.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=Python&logoColor=white)](https://python.org)

An AI and Computer Vision screening system for non-invasive detection of **neonatal hyperbilirubinemia (jaundice)** in newborns, combining deep learning vision classifiers (**YOLOv8**) with clinical skin colorimetry (**XGBoost / Random Forest**).

Based on the clinical research paper:  
> **"Real-Time Jaundice Detection in Neonates Based on Machine Learning Models"**  
> *Abdulrazzak, A.Y., Mohammed, S.L., Al-Naji, A., and Chahl, J.* — **BioMedInformatics 2024, 4(1), 623–637**. [DOI: 10.3390/biomedinformatics4010034](https://doi.org/10.3390/biomedinformatics4010034)

---

## 🌟 Key Features

1. **Dual-Model Diagnostic Engine**:
   - **YOLOv8 Classification (`yolov8n-cls`)**: State-of-the-art vision classifier trained on 760 infant images achieving **98.68% validation accuracy**.
   - **Clinical Skin Colorimetry (XGBoost / RF)**: Replicates the paper's skin ROI extraction pipeline, achieving **96.73% test accuracy** (and **99.63%** benchmark on extracted features).
   - **Hybrid Ensemble Mode**: Combines both models for multi-modal verification.
2. **Automated Skin ROI Segmentation**:
   - Transforms RGB to **CIE-LAB** space.
   - Performs **Otsu automatic thresholding** on $A$ and $B$ chrominance channels.
   - Applies morphological erosion to eliminate non-skin background artifacts (bedding, incubator walls, diapers).
3. **Biophysical Color Analysis**:
   - Extracts mean intensities for Red ($R$), Green ($G$), Blue ($B$), Luminance ($Y$), Chrominance-Blue ($Cb$), and Chrominance-Red ($Cr$).
   - Leverages bilirubin's high blue absorption ($450 - 460\,\text{nm}$) to identify hyperbilirubinemia risk.
4. **Interactive Streamlit Web Dashboard**:
   - Drag-and-drop image upload or quick sample selector.
   - Real-time segmented skin ROI visualization and **$Cb$ channel jet heatmap**.
   - Immediate diagnosis (**JAUNDICE DETECTED** vs **NORMAL**) with confidence percentages.
   - American Academy of Pediatrics (AAP) risk evaluation guidance.

---

## 📊 Benchmark Results

| Model | Architecture | Accuracy | Precision | Recall (Sens.) | F1 Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **YOLOv8-cls** | Convolutional Neural Network | **98.68%** | 98.50% | 98.70% | 98.60% |
| **XGBoost** | Gradient Boosted Decision Trees | **96.73%** | 95.00% | 93.00% | 94.00% |
| **Random Forest** | Bagged Decision Trees (n=100) | **96.08%** | 95.00% | 92.50% | 93.70% |

---

## 🚀 Quick Start

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/TanmayKalra09/neonatal-jaundice-detection.git
cd neonatal-jaundice-detection

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

*(Note for macOS users running XGBoost: run `brew install libomp`)*

### 2. Launch Streamlit Dashboard
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 📁 Repository Structure

```
neonatal-jaundice-detection/
├── app.py                     # Interactive Streamlit dashboard
├── feature_extractor.py       # LAB Otsu skin ROI segmentation & color extraction
├── train_yolo.py              # YOLOv8-cls training pipeline
├── train_ml.py                # XGBoost and Random Forest training script
├── prepare_data.py            # Dataset extraction and train/val/test splitter
├── generate_pdf.py            # Automated technical & clinical PDF report generator
├── requirements.txt           # Project dependencies
├── models/
│   ├── yolov8_jaundice_best.pt   # Pretrained YOLOv8 weights (3 MB)
│   └── tabular_models.joblib     # Pretrained XGBoost, RF & Scaler
├── sample_images/             # Preloaded sample test images for evaluation
│   ├── jaundice/
│   └── normal/
└── docs/
    └── Neonatal_Jaundice_Detection_System_Report.pdf  # Comprehensive technical PDF
```

---

## 🔬 Clinical Methodology

```
Uploaded Image
      │
      ▼
RGB ──► CIE-LAB Transformation ──► Otsu Thresholding ──► Morphological Erosion
                                                                │
                                                                ▼
                                                       Segmented Skin ROI
                                                                │
                        ┌───────────────────────────────────────┴───────────────────────────────────────┐
                        ▼                                                                               ▼
           [YOLOv8 Vision Classifier]                                                      [Skin Colorimetric Engine]
                        │                                                                (R, G, B, Y, Cb, Cr Vector)
                        │                                                                               │
                        │                                                                               ▼
                        │                                                                   [XGBoost / Random Forest]
                        │                                                                               │
                        └───────────────────────────────┬───────────────────────────────────────────────┘
                                                        ▼
                                       Final Diagnostic Verdict + Confidence
                                        (⚠️ JAUNDICE DETECTED / ✅ NORMAL)
```

---

## 📜 Disclaimer
This software is intended for research and educational purposes as an AI-assisted non-invasive screening tool. Diagnostic results should always be clinically verified with a pediatric physician using transcutaneous bilirubinometry (TcB) or total serum bilirubin (TSB) laboratory blood tests per American Academy of Pediatrics (AAP) protocols.

---

## 👤 Author
**Tanmay Kalra**  
- GitHub: [@TanmayKalra09](https://github.com/TanmayKalra09)
