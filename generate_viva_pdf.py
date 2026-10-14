import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Neonatal Jaundice Vision Diagnosis — Viva & Project Defense Guide")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "30 Essential Q&A")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 34, "Author: Tanmay Kalra | GitHub: github.com/TanmayKalra09/neonatal-jaundice-detection")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 46, letter[0] - 54, 46)
        self.restoreState()

def build_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1E3A8A")   # Navy
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_text = colors.HexColor("#1F2937")       # Charcoal
    category_color = colors.HexColor("#1E40AF")  # Blue Accent
    bg_box = colors.HexColor("#F8FAFC")
    border_box = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=10
    )

    cat_style = ParagraphStyle(
        'CategoryHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=category_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=primary_color,
        spaceBefore=4,
        spaceAfter=2
    )

    a_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_text,
        spaceAfter=6
    )

    story = []

    # Title header
    story.append(Paragraph("Neonatal Jaundice Detection — Viva &amp; Oral Defense Q&amp;A", title_style))
    story.append(Paragraph("<b>30 Essential Questions &amp; Clear Answers</b> on Technologies, Computer Vision, Models, and Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    qa_list = [
        # SECTION 1
        ("Section 1: Basic Project & Technology Overview", [
            ("Q1: What is the main objective of this project?",
             "The objective is to build a non-invasive, AI-driven computer vision system that screens newborn babies for neonatal jaundice (hyperbilirubinemia) by analyzing an infant's photo. It detects yellow skin discoloration, gives an immediate diagnosis (Jaundice vs. Normal), and provides a confidence percentage without causing discomfort to the baby."),

            ("Q2: Which programming language is used for coding this project?",
             "The entire project is coded in <b>Python 3.13</b>. Python was chosen for its rich ecosystem of medical computer vision libraries (OpenCV, PIL), machine learning frameworks (PyTorch, Ultralytics YOLO, XGBoost, Scikit-Learn), and rapid web UI deployment tools (Streamlit)."),

            ("Q3: What key libraries and technologies did you use?",
             "The core technologies are: <br/>"
             "• <b>Computer Vision:</b> OpenCV (cv2) and PIL (Pillow) for color space conversions and skin segmentation.<br/>"
             "• <b>Deep Learning:</b> PyTorch and Ultralytics YOLOv8 for convolutional image classification.<br/>"
             "• <b>Machine Learning:</b> XGBoost, Scikit-Learn, and Joblib for clinical colorimetric models.<br/>"
             "• <b>Web Dashboard:</b> Streamlit for interactive web browser deployment.<br/>"
             "• <b>Data Handling & Visualization:</b> Pandas, NumPy, and Matplotlib."),

            ("Q4: What is neonatal jaundice and why is automated screening important?",
             "Neonatal jaundice is caused by excessive bilirubin in an infant's blood due to an immature liver. While mild cases are common, severe cases can lead to irreversible brain damage (kernicterus) or fatality. Standard tests require invasive blood draws (TSB). Our non-invasive computer vision tool allows painless, rapid, low-cost screening that can be deployed anywhere via camera or mobile app."),

            ("Q5: What dataset is used to train and test the models?",
             "We used the clinical <b>Normal and Jaundiced Newborns (NJN) dataset</b> from Al-Elwiya Maternity Teaching Hospital (associated with the BioMedInformatics 2024 paper). It contains 760+ newborn photos across various skin tones, age groups (2 to 12 days), and clinical conditions, complete with ground-truth laboratory bilirubin confirmations.")
        ]),

        # SECTION 2
        ("Section 2: Dataset, Computer Vision & ROI Extraction", [
            ("Q6: How did you divide the dataset for training and testing?",
             "The dataset was partitioned into <b>80% training</b> (to teach the models patterns), <b>10% validation</b> (to tune hyperparameters during training), and <b>10% test set</b> (unseen images reserved solely to measure real-world diagnostic accuracy)."),

            ("Q7: What is ROI (Region of Interest) and why is it essential?",
             "ROI stands for Region of Interest. In clinical image processing, examining the entire raw photo causes errors because backgrounds contain blankets, diapers, incubator glass, or clothes. ROI extraction isolates only the baby's actual skin tissue so color analysis reflects biological conditions rather than surrounding objects."),

            ("Q8: What are the three steps in your skin ROI segmentation pipeline?",
             "The pipeline consists of: <br/>"
             "1. <b>Color Conversion:</b> Convert the RGB image to the CIE-LAB color space.<br/>"
             "2. <b>Otsu Thresholding:</b> Automatically compute mathematical thresholds on chromatic channels to create a binary skin mask.<br/>"
             "3. <b>Morphological Erosion:</b> Filter out stray pixels, noise, and foreign boundaries to isolate pure skin pixels."),

            ("Q9: What is Otsu's thresholding and how does it work here?",
             "Otsu's method is an automatic thresholding algorithm. It examines the histogram of pixel intensities and calculates the threshold that minimizes intra-class variance (or maximizes variance between classes). Here, it automatically splits skin pixels (labeled 1/white) from background pixels (labeled 0/black) without requiring manual threshold tuning."),

            ("Q10: Why are morphological filters (erosion and opening) applied?",
             "Raw threshold masks often contain noise such as diaper edges, hair, shadow boundaries, or medical stickers. Morphological erosion with an elliptical kernel shrinks boundaries and eliminates disconnected small artifacts, ensuring that only true, continuous skin pixels are passed to the feature extractor.")
        ]),

        # SECTION 3
        ("Section 3: Color Spaces & Biophysical Principles", [
            ("Q11: Why is the raw RGB color space not sufficient on its own?",
             "In RGB, color (chrominance) and brightness (luminance) are mixed across all three channels. A change in room lighting or camera flash alters all R, G, and B numbers simultaneously. Medical computer vision requires color spaces where luminance is separated from pure color."),

            ("Q12: What is the CIE-LAB color space and why use it?",
             "CIE-LAB is designed to approximate human vision: <b>L</b> represents Lightness/Luminance, <b>A</b> is the Green–Red axis, and <b>B</b> is the Blue–Yellow axis. By isolating the 'B' channel, the system directly tracks yellow pigmentation changes independently of room brightness."),

            ("Q13: What is the YCrCb color space and what are its channels?",
             "YCrCb decomposes an image into: <b>Y</b> = Luminance (intensity), <b>Cr</b> = Chrominance-Red, and <b>Cb</b> = Chrominance-Blue. It is widely used in medical skin detection because discarding the Y channel renders skin tone analysis largely invariant to ambient illumination."),

            ("Q14: Which color channels are the most critical biomarkers for jaundice?",
             "The <b>Blue (B)</b> channel in RGB and the <b>Cb</b> channel in YCrCb. In the research paper's feature importance analysis, Cb scored the highest relative importance (~0.33) among all channels because bilirubin absorption specifically targets blue wavelengths."),

            ("Q15: What is the medical/optical reason why blue light absorption signifies jaundice?",
             "Bilirubin is a yellow organic pigment. In photobiology, yellow pigments have their peak optical absorption precisely in the blue spectrum (<b>450 nm – 460 nm</b>). When bilirubin accumulates in neonatal skin, it absorbs blue light, causing both the RGB Blue (B) and YCrCb (Cb) channel intensities to drop sharply compared to healthy skin.")
        ]),

        # SECTION 4
        ("Section 4: Machine Learning & Deep Learning Models", [
            ("Q16: Why did you implement two different models: YOLOv8 and XGBoost?",
             "They serve complementary purposes: <br/>"
             "• <b>YOLOv8:</b> An advanced Convolutional Neural Network that evaluates full-scene spatial visual patterns end-to-end.<br/>"
             "• <b>XGBoost:</b> A tabular clinical model that focuses exclusively on the paper's extracted skin colorimetric vector [R, G, B, Y, Cb, Cr]. Having both allows multi-modal verification and an ensemble option."),

            ("Q17: What is YOLOv8 and how is it used in classification mode?",
             "YOLOv8 (You Only Look Once, v8) by Ultralytics is a state-of-the-art vision architecture. We used <b>YOLOv8n-cls</b> (nano classification), which uses convolutional feature extractors and cross-stage partial bottlenecks to classify the baby image into 'Jaundice' or 'Normal' with a probability score."),

            ("Q18: What is XGBoost and how does it work?",
             "XGBoost stands for eXtreme Gradient Boosting. It builds an ensemble of decision trees sequentially. Unlike Random Forest where trees are built independently, each new tree in XGBoost is trained specifically to correct the gradient loss (errors) of the previous trees, optimizing both accuracy and execution speed."),

            ("Q19: What other Machine Learning models were evaluated in the research paper?",
             "The authors benchmarked four classical algorithms: <br/>"
             "1. Support Vector Machine (SVM) — 96.22% accuracy<br/>"
             "2. k-Nearest Neighbors (k-NN) — 98.25% accuracy<br/>"
             "3. Random Forest (RF) — 98.99% accuracy<br/>"
             "4. XGBoost — <b>99.63% accuracy</b> (selected as best)."),

            ("Q20: What is Random Forest and how did it perform?",
             "Random Forest is a bagging ensemble of multiple decision trees trained on random subsets of data and features. Its final decision is based on majority voting. In our experiments, Random Forest achieved <b>96.08%</b> test accuracy (98.99% in the paper), ranking second right behind XGBoost."),

            ("Q21: Why did SVM and k-NN perform lower than tree-based models?",
             "SVM tries to draw a single linear or kernel hyperplane across high-dimensional space, which struggles when skin color boundaries slightly overlap between borderline patients. k-NN calculates distance to neighbors, which is sensitive to outliers and feature scaling. Tree-based gradient boosting handles non-linear medical decision boundaries significantly better."),

            ("Q22: What is the Hybrid Ensemble model in the Streamlit app?",
             "The Hybrid Ensemble takes the predicted probabilities of both YOLOv8 (visual patterns) and XGBoost (skin colorimetry), averages their confidence scores, and determines the final diagnosis. This reduces variance and prevents a false reading from either single model.")
        ]),

        # SECTION 5
        ("Section 5: Evaluation, Metrics & Real-World Discrepancy", [
            ("Q23: What accuracy did your models achieve?",
             "• <b>YOLOv8-cls:</b> Achieved <b>98.68% validation top-1 accuracy</b> on unseen infant images.<br/>"
             "• <b>XGBoost:</b> Achieved <b>96.73% test accuracy</b> on held-out test data (and up to 99.63% in full clinical trials).<br/>"
             "• <b>Random Forest:</b> Achieved <b>96.08% test accuracy</b>."),

            ("Q24: What evaluation metrics did you use besides accuracy?",
             "We evaluated: <br/>"
             "• <b>Precision (95%–99%):</b> Of all babies predicted to have jaundice, what fraction actually had it?<br/>"
             "• <b>Recall / Sensitivity (93%–99%):</b> Of all true jaundice cases, what fraction was successfully caught? (Crucial in medicine to prevent false negatives).<br/>"
             "• <b>F1-Score:</b> Harmonic mean of precision and recall.<br/>"
             "• <b>Confusion Matrix:</b> Breakdown of True Positives, True Negatives, False Positives, and False Negatives."),

            ("Q25: Why did YOLO say 'Normal' but XGBoost say 'Jaundice' on the downloaded test photo?",
             "In that image, the jaundiced baby was lying on a <b>large bright blue blanket</b> covering ~40% of the frame. YOLO looks at the entire scene; the intense blue blanket artificially saturated the global color balance, confusing the CNN. However, XGBoost first extracted the baby's skin ROI, completely discarded the blue blanket, and saw that the baby's skin blue channel was <b>69.9</b> (severely depleted). Thus, XGBoost correctly diagnosed Jaundice with 99.3% certainty."),

            ("Q26: Which model should be preferred when baby photos have colorful blankets or clothes?",
             "<b>Skin Colorimetric XGBoost</b> is the gold standard for photos taken with non-hospital backgrounds because its LAB Otsu segmentation strips away surrounding clothing, bedding, and foreign objects, isolating pure biological skin features.")
        ]),

        # SECTION 6
        ("Section 6: Web Deployment, Limitations & Future Scope", [
            ("Q27: How does the Streamlit web application work?",
             "Streamlit provides a clean, reactive browser dashboard. The user uploads an image or selects a pre-loaded test case. In the backend, OpenCV extracts the skin ROI and computes the Cb heatmap, YOLO and XGBoost execute inference in real-time, and the front-end displays side-by-side visual stages, metrics, and risk status."),

            ("Q28: How is the confidence score calculated and displayed?",
             "The models output probability distributions using softmax (for YOLO) and logistic loss functions (for XGBoost). The positive probability is converted to a clean percentage (e.g., 99.34%), accompanied by a colored visual status bar (amber for Jaundice risk, emerald green for Normal)."),

            ("Q29: What are the current limitations of this system?",
             "1. Extreme lighting variations (e.g., yellow incandescent bulbs or direct harsh flash) can affect skin tones.<br/>"
             "2. The NJN dataset was collected primarily from one hospital region; broader multi-ethnic cohorts would enhance generalization across diverse skin pigmentations.<br/>"
             "3. It serves as a screening tool, not a full replacement for invasive laboratory blood tests."),

            ("Q30: What future improvements can be made?",
             "• Incorporating a standardized color calibration reference sticker (white/gray card) placed near the infant.<br/>"
             "• Integrating a mobile app (iOS/Android) using lightweight YOLO-ONNX or TFLite models for rural telemedicine.<br/>"
             "• Sclera (eye white) segmentation alongside skin analysis to detect early onset jaundice before skin discoloration manifests.")
        ])
    ]

    for cat_title, items in qa_list:
        story.append(Paragraph(cat_title, cat_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=secondary_color, spaceAfter=6))
        
        for q_text, a_text in items:
            q_flowable = Paragraph(q_text, q_style)
            a_flowable = Paragraph(f"<b>Answer:</b> {a_text}", a_style)
            
            box_table = Table([[q_flowable], [a_flowable]], colWidths=[letter[0] - 96])
            box_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), bg_box),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('BOX', (0, 0), (-1, -1), 0.5, border_box),
                ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#CBD5E1")),
            ]))
            
            story.append(KeepTogether([box_table, Spacer(1, 4)]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Viva Q&A PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    out_pdf = "/Users/tanmaykalra/Neonatal_Jaundice_Viva_30_QnA.pdf"
    build_pdf(out_pdf)
