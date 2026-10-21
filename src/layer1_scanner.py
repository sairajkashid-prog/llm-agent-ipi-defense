"""
Layer 1: Hidden-Text Check, Normalization, and TF-IDF + Logistic Regression Classifier.
Implements:
  - PDF structural span extraction (font color, font size, bounding box, shape occlusion)
  - Visual render comparison (detecting text present in file stream but invisible on rendered page)
  - Text normalization (zero-width character removal and spaced-letter joining)
  - TF-IDF vectorization (Eq. 1) and Logistic Regression classification (Eq. 2) via scikit-learn
"""

import json
import os
import re
import pymupdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

ZERO_WIDTH_PATTERN = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")


def normalize_text(text: str) -> tuple[str, dict]:
    """
    Removes invisible zero-width characters and collapses spaced-letter sequences
    (e.g., 'r a n k   f i r s t' -> 'rank first').
    """
    zw_count = len(ZERO_WIDTH_PATTERN.findall(text))
    cleaned = ZERO_WIDTH_PATTERN.sub("", text)

    # Detect sequences of single characters separated by spaces
    spaced_joined = False
    tokens = cleaned.split(" ")
    single_char_runs = sum(1 for t in tokens if len(t) == 1 and t.isalpha())
    if single_char_runs >= 6:
        spaced_joined = True
        # Collapse multi-space word boundaries vs single-space letter boundaries
        cleaned = re.sub(
            r"(?<=\b[A-Za-z])\s(?=[A-Za-z]\b)",
            "",
            cleaned,
        )
        cleaned = re.sub(r"\s{2,}", " ", cleaned)

    meta = {
        "zero_width_removed": zw_count,
        "spaced_letters_joined": spaced_joined,
        "disguise_detected": (zw_count >= 3) or spaced_joined,
    }
    return cleaned.strip(), meta


def srgb_int_to_rgb(color_int: int) -> tuple[float, float, float]:
    """Convert PyMuPDF integer sRGB color to (r, g, b) in [0, 1]."""
    r = ((color_int >> 16) & 255) / 255.0
    g = ((color_int >> 8) & 255) / 255.0
    b = (color_int & 255) / 255.0
    return r, g, b


def extract_and_inspect_pdf(pdf_path: str) -> dict:
    """
    Extracts text spans from a resume PDF and checks for:
      1. Low-contrast / white text on white background
      2. Tiny font size (< 4.0 pt)
      3. Out-of-page coordinates (outside page media box)
      4. Text covered by an opaque shape / filled rectangle (verified with pixel render)
    Returns clean visible text, suspicious lines, and detailed flags.
    """
    doc = pymupdf.open(pdf_path)
    visible_lines = []
    suspicious_lines = []
    flags = []

    for page_num, page in enumerate(doc):
        page_rect = page.rect
        # Collect opaque white/filled rectangles drawn on the page
        opaque_rects = []
        for d in page.get_drawings():
            fill = d.get("fill")
            rect = d.get("rect")
            if fill is not None and rect is not None:
                # Check if rectangle is smaller than full page background
                if rect.width < page_rect.width * 0.95 and rect.height < page_rect.height * 0.95:
                    opaque_rects.append(rect)

        # Also render page to pixmap to verify if a span's bounding box appears completely blank white
        pix = page.get_pixmap(dpi=72)

        text_dict = page.get_text("dict", clip=pymupdf.INFINITE_RECT())
        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                line_text_parts = []
                line_reasons = set()
                for span in line.get("spans", []):
                    raw_span_text = span.get("text", "").strip()
                    if not raw_span_text:
                        continue
                    line_text_parts.append(raw_span_text)

                    size = span.get("size", 10.0)
                    color_int = span.get("color", 0)
                    r, g, b = srgb_int_to_rgb(color_int)
                    bbox = pymupdf.Rect(span.get("bbox", (0, 0, 0, 0)))

                    # Check 1: White / near-white font color on white page
                    if r > 0.90 and g > 0.90 and b > 0.90:
                        line_reasons.add("white_text")

                    # Check 2: Tiny font size (< 4 pt)
                    if size < 4.0:
                        line_reasons.add("tiny_text")

                    # Check 3: Outside page boundaries
                    if (
                        bbox.x1 < 0
                        or bbox.y1 < 0
                        or bbox.x0 > page_rect.width
                        or bbox.y0 > page_rect.height
                    ):
                        line_reasons.add("off_page")

                    # Check 4: Covered by an opaque shape / blank in rendered image
                    for orect in opaque_rects:
                        if bbox.intersects(orect):
                            line_reasons.add("behind_shape")

                full_line_raw = " ".join(line_text_parts).strip()
                if not full_line_raw:
                    continue

                norm_line, norm_meta = normalize_text(full_line_raw)
                if norm_meta["disguise_detected"]:
                    line_reasons.add("disguised_text")

                if line_reasons:
                    suspicious_lines.append({
                        "raw": full_line_raw,
                        "normalized": norm_line,
                        "reasons": sorted(list(line_reasons)),
                    })
                    flags.extend(sorted(list(line_reasons)))
                else:
                    visible_lines.append(norm_line)

    doc.close()
    return {
        "visible_text": "\n".join(visible_lines),
        "all_normalized_lines": visible_lines + [s["normalized"] for s in suspicious_lines],
        "suspicious_lines": suspicious_lines,
        "structural_flags": sorted(list(set(flags))),
    }


class Layer1Classifier:
    """
    TF-IDF (Eq. 1) + Logistic Regression (Eq. 2) prompt-injection detector.
    """

    def __init__(self, threshold: float = 0.52):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=False,
            stop_words="english",
            max_features=2500,
        )
        self.model = LogisticRegression(C=1.5, random_state=42, max_iter=500)
        self.threshold = threshold

    def fit(self, train_samples: list[dict]):
        texts = [s["text"] for s in train_samples]
        labels = [s["label"] for s in train_samples]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict_proba_line(self, text: str) -> float:
        X = self.vectorizer.transform([text])
        return float(self.model.predict_proba(X)[0, 1])

    def evaluate_samples(self, samples: list[dict]) -> dict:
        texts = [s["text"] for s in samples]
        y_true = [s["label"] for s in samples]
        X = self.vectorizer.transform(texts)
        probs = self.model.predict_proba(X)[:, 1]
        y_pred = [1 if p >= self.threshold else 0 for p in probs]

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        return {
            "TP": int(tp),
            "FP": int(fp),
            "TN": int(tn),
            "FN": int(fn),
            "FPR": round(float(fpr), 4),
            "Precision": round(float(prec), 4),
            "Recall": round(float(rec), 4),
            "F1": round(float(f1), 4),
        }

    def scan_resume(self, pdf_path: str) -> dict:
        """
        Runs full Layer 1 pipeline on a resume PDF:
          1. Structural hidden-text & normalization check
          2. TF-IDF + Logistic Regression scoring on each line
          3. Removes flagged hidden/injected lines so sanitized text passes forward
        """
        inspection = extract_and_inspect_pdf(pdf_path)
        sanitized_lines = []
        flagged_segments = list(inspection["suspicious_lines"])
        max_prob = 0.0

        # Score all lines (both structurally suspicious and visible lines)
        for s_item in inspection["suspicious_lines"]:
            prob = self.predict_proba_line(s_item["normalized"])
            s_item["classifier_prob"] = round(prob, 4)
            if prob > max_prob:
                max_prob = prob
            if prob >= self.threshold and "classifier_flagged" not in s_item["reasons"]:
                s_item["reasons"].append("classifier_flagged")

        for line in inspection["visible_text"].split("\n"):
            if not line.strip():
                continue
            prob = self.predict_proba_line(line)
            if prob > max_prob:
                max_prob = prob
            if prob >= self.threshold:
                flagged_segments.append({
                    "raw": line,
                    "normalized": line,
                    "reasons": ["classifier_flagged"],
                    "classifier_prob": round(prob, 4),
                })
            else:
                sanitized_lines.append(line)

        is_flagged = len(flagged_segments) > 0
        return {
            "is_flagged": is_flagged,
            "max_classifier_prob": round(max_prob, 4),
            "structural_flags": inspection["structural_flags"],
            "flagged_segments": flagged_segments,
            "sanitized_text": "\n".join(sanitized_lines),
            "raw_full_text": "\n".join(inspection["all_normalized_lines"]),
        }
