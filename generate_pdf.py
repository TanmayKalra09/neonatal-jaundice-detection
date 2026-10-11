import os
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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#6B7280"))
        # Header rule & title (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Neonatal Jaundice Detection System — Technical & Clinical Report")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_str)
        self.drawString(54, 36, "Confidential — Computer Vision & Machine Learning Architecture")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

def create_report(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1E3A8A")   # Navy Blue
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_neutral = colors.HexColor("#1F2937")    # Charcoal
    light_bg = colors.HexColor("#F8FAFC")        # Soft background
    border_color = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=dark_neutral,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_neutral,
        leftIndent=15,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E40AF")
    )

    story = []

    # Title & Subtitle Banner
    story.append(Paragraph("Neonatal Jaundice Detection System", title_style))
    story.append(Paragraph("Computer Vision, Colorimetric Feature Extraction & Dual-Model Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=14))

    # SECTION 1
    story.append(Paragraph("1. System Overview: What Have We Built?", h1_style))
    story.append(Paragraph(
        "We engineered an end-to-end AI and Computer Vision screening system for neonatal jaundice (hyperbilirubinemia). "
        "The project is based directly on the peer-reviewed clinical research paper "
        "<i>'Real-Time Jaundice Detection in Neonates Based on Machine Learning Models'</i> (BioMedInformatics 2024, 4, 623–637) "
        "and trained using the clinical <b>NJN (Normal and Jaundiced Newborns)</b> dataset containing 767 infant samples.",
        body_style
    ))
    story.append(Paragraph("When an infant image is uploaded, the pipeline performs three sequential actions:", body_style))
    story.append(Paragraph("• <b>Skin ROI Segmentation:</b> Automatically isolates the newborn's skin pixels and discards background interference (bedding, incubator walls, diapers).", bullet_style))
    story.append(Paragraph("• <b>Colorimetric Channel Extraction:</b> Quantifies yellow bilirubin discoloration across RGB, CIE-LAB, and YCrCb color spaces.", bullet_style))
    story.append(Paragraph("• <b>Diagnostic Inference & Confidence Scoring:</b> Outputs an immediate diagnosis (<b>Jaundice Detected</b> vs. <b>Normal</b>) along with an exact probability score (e.g., 99.34%).", bullet_style))

    # SECTION 2
    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Computer Vision: How Skin ROI (Region of Interest) Is Extracted", h1_style))
    story.append(Paragraph(
        "In neonatal medicine, analyzing the entire raw photo leads to false readings because ambient surroundings "
        "(e.g., colored blankets, clothes, plastic tubes) skew the pixels. The system implements a robust 3-stage computer vision filter:",
        body_style
    ))
    
    story.append(Paragraph("<b>Step A: Color Space Transformation (RGB → CIE-LAB)</b>", h2_style))
    story.append(Paragraph(
        "Standard RGB images combine color and illumination, making them vulnerable to lighting changes. "
        "We convert the image to the <b>CIE-LAB</b> space where lightness (<b>L</b>) is separated from chrominance: "
        "<b>A</b> represents the Green–Red axis, and <b>B</b> represents the Blue–Yellow axis.",
        body_style
    ))

    story.append(Paragraph("<b>Step B: Otsu Automatic Thresholding</b>", h2_style))
    story.append(Paragraph(
        "The algorithm uses Otsu's mathematical binarization across the <i>A</i> and <i>B</i> chrominance channels. "
        "It automatically calculates the optimal intra-class variance threshold that separates human skin from textiles and foreign objects, "
        "producing a clean binary skin mask where skin pixels = 1 (white) and background = 0 (black).",
        body_style
    ))

    story.append(Paragraph("<b>Step C: Morphological Filtering & Color Decomposition</b>", h2_style))
    story.append(Paragraph(
        "An elliptical morphological erosion filter removes boundary noise, hair, and diaper tape. "
        "The pure skin mask is then mapped onto the image to compute mean intensities for: "
        "<b>Red (R)</b>, <b>Green (G)</b>, <b>Blue (B)</b>, <b>Luminance (Y)</b>, <b>Chrominance-Blue (Cb)</b>, and <b>Chrominance-Red (Cr)</b>.",
        body_style
    ))

    # SECTION 3
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Model Architecture: Why Two Models (YOLOv8 vs. XGBoost)?", h1_style))
    story.append(Paragraph(
        "To provide both modern deep learning visual capabilities and clinically validated colorimetric precision, "
        "our system includes two distinct model paradigms plus a hybrid ensemble:",
        body_style
    ))

    # Model comparison table
    model_table_data = [
        [
            Paragraph("<b>Evaluation Dimension</b>", table_header_style),
            Paragraph("<b>YOLOv8 Vision Classifier</b>", table_header_style),
            Paragraph("<b>XGBoost Colorimetric Model</b>", table_header_style)
        ],
        [
            Paragraph("<b>Model Family</b>", table_cell_bold),
            Paragraph("Convolutional Neural Network (CNN / Deep Learning)", table_cell_style),
            Paragraph("Gradient Boosted Decision Trees (Tabular ML)", table_cell_style)
        ],
        [
            Paragraph("<b>Input Data</b>", table_cell_bold),
            Paragraph("Raw 2D image matrix (224×224 pixels, full scene)", table_cell_style),
            Paragraph("Segmented Skin Vector: [R, G, B, Y, Cb, Cr]", table_cell_style)
        ],
        [
            Paragraph("<b>Background Invariance</b>", table_cell_bold),
            Paragraph("Moderate (sensitive to strong colored blankets)", table_cell_style),
            Paragraph("<b>High (Completely ignores background)</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Validation Accuracy</b>", table_cell_bold),
            Paragraph("<b>98.68%</b> on NJN test cohort", table_cell_style),
            Paragraph("<b>96.73%</b> test / <b>99.63%</b> paper benchmark", table_cell_style)
        ],
        [
            Paragraph("<b>Clinical Purpose</b>", table_cell_bold),
            Paragraph("End-to-end instant vision diagnosis", table_cell_style),
            Paragraph("Precise quantitative hyperbilirubinemia verification", table_cell_style)
        ]
    ]

    t_model = Table(model_table_data, colWidths=[1.5*inch, 2.75*inch, 2.75*inch])
    t_model.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
    ]))
    story.append(t_model)

    # SECTION 4
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Classical Machine Learning Benchmark: k-NN, SVM, RF, and XGBoost", h1_style))
    story.append(Paragraph(
        "In the foundational research paper (Abdulrazzak et al., 2024), the authors compared four prominent machine learning classifiers "
        "to determine which algorithm yields the highest diagnostic reliability for neonatal jaundice:",
        body_style
    ))

    ml_table_data = [
        [
            Paragraph("<b>Algorithm</b>", table_header_style),
            Paragraph("<b>Working Mechanism</b>", table_header_style),
            Paragraph("<b>Accuracy</b>", table_header_style),
            Paragraph("<b>Precision</b>", table_header_style),
            Paragraph("<b>Recall (Sens.)</b>", table_header_style),
            Paragraph("<b>F1 Score</b>", table_header_style)
        ],
        [
            Paragraph("<b>SVM</b><br/>(Support Vector Machine)", table_cell_bold),
            Paragraph("Constructs a maximum-margin hyperplane separating normal vs jaundiced feature vectors.", table_cell_style),
            Paragraph("96.22%", table_cell_style),
            Paragraph("95.74%", table_cell_style),
            Paragraph("98.38%", table_cell_style),
            Paragraph("97.03%", table_cell_style)
        ],
        [
            Paragraph("<b>k-NN</b><br/>(k-Nearest Neighbor)", table_cell_bold),
            Paragraph("Calculates Euclidean distances in color space to find the k nearest reference infants.", table_cell_style),
            Paragraph("98.25%", table_cell_style),
            Paragraph("97.84%", table_cell_style),
            Paragraph("99.41%", table_cell_style),
            Paragraph("98.61%", table_cell_style)
        ],
        [
            Paragraph("<b>Random Forest (RF)</b>", table_cell_bold),
            Paragraph("Ensemble of 100 bootstrapped decision trees with feature sub-sampling.", table_cell_style),
            Paragraph("98.99%", table_cell_style),
            Paragraph("99.12%", table_cell_style),
            Paragraph("99.26%", table_cell_style),
            Paragraph("99.19%", table_cell_style)
        ],
        [
            Paragraph("<b>XGBoost</b><br/>(Gradient Boost)", table_cell_bold),
            Paragraph("Sequential tree boosting that iteratively minimizes residuals and penalizes complexity.", table_cell_style),
            Paragraph("<b>99.63%</b>", table_cell_bold),
            Paragraph("<b>99.57%</b>", table_cell_bold),
            Paragraph("<b>99.85%</b>", table_cell_bold),
            Paragraph("<b>99.71%</b>", table_cell_bold)
        ]
    ]

    t_ml = Table(ml_table_data, colWidths=[1.5*inch, 2.5*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
    ]))
    story.append(t_ml)

    # SECTION 5
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Biophysical Principles: Why Blue (B) & Cb Channels Are Decisive", h1_style))
    story.append(Paragraph(
        "Hyperbilirubinemia occurs when an immature neonatal liver fails to metabolize bilirubin, "
        "causing yellow tetrapyrrole pigment to accumulate in subcutaneous skin tissue and sclera. "
        "The optical physics explains why colorimetric computer vision is so effective:",
        body_style
    ))
    story.append(Paragraph("• <b>Optical Absorption Spectrum:</b> Unconjugated bilirubin exhibits peak light absorption in the blue spectrum (<b>450 nm – 460 nm</b>).", bullet_style))
    story.append(Paragraph("• <b>Blue Channel Plummet:</b> As subcutaneous bilirubin concentrations rise, blue wavelengths are strongly absorbed while red/yellow wavelengths reflect. Consequently, <b>Blue (B)</b> channel intensity plummets from normal values (~120–150) down to < 100 in jaundiced neonates.", bullet_style))
    story.append(Paragraph("• <b>YCrCb Feature Importance:</b> In the YCrCb color space, luminance (Y) is decoupled. The Chrominance-Blue channel (<b>Cb</b>) exhibits the highest feature importance score (0.33) of all evaluated features (Section 2.3.2, Figure 2).", bullet_style))

    # SECTION 6
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Case Study: Explaining the Test Image Divergence", h1_style))
    story.append(Paragraph(
        "During live testing with sample image <code>679e0b6e965452aeff470497.jpg</code>, XGBoost classified the patient as "
        "<b>Jaundice (99.34% confidence)</b> whereas raw YOLOv8 classified it as <b>Normal (97.74% confidence)</b>. Here is the technical explanation:",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>1. What XGBoost Analyzed:</b> Our LAB Otsu filter stripped away the background entirely and measured pure cutaneous tissue: "
        "<code>Red=187.3</code>, <code>Green=145.9</code>, <code>Blue=69.9</code>, <code>Cb=83.0</code>. "
        "Because <b>Blue=69.9</b> is severely depressed below healthy clinical thresholds, XGBoost accurately diagnosed severe jaundice.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. What YOLOv8 Analyzed:</b> The infant was photographed lying on a <b>vibrant blue blanket</b> covering ~40% of the camera frame. "
        "Because YOLO was trained on NICU incubator photos taken on standard white sheets, the massive patch of blue fabric dominated the global "
        "convolutional receptive fields, tricking the end-to-end network into seeing high blue reflectance.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Clinical Takeaway:</b> For photos with non-standard backgrounds (blue or colored blankets/clothing), the "
        "<b>Skin Colorimetric XGBoost</b> model is the gold standard because it is completely invariant to background color.",
        bullet_style
    ))

    # SECTION 7
    story.append(Spacer(1, 10))
    story.append(Paragraph("7. Deployment & Streamlit Interface", h1_style))
    story.append(Paragraph(
        "The complete system is deployed as an interactive Streamlit web dashboard accessible at <b>http://localhost:8501</b>. "
        "It features dynamic image uploading, live skin ROI segmentation, Cb chrominance heatmaps, dual-model confidence meters, "
        "and American Academy of Pediatrics (AAP) risk evaluation guidance.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully at: {output_pdf_path}")

if __name__ == "__main__":
    out_path = "/Users/tanmaykalra/Neonatal_Jaundice_Detection_System_Report.pdf"
    create_report(out_path)
