from PIL import Image
import pytesseract
try:
    from sklearn.cluster import KMeans
    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False

from app.schemas.layout import LayoutResult, TextBlock
from app.utils.logger import setup_logger

logger = setup_logger("layout_analyzer")


def _cluster_columns(x_coords, max_k=3):
    if not x_coords or len(x_coords) < 3:
        return 1
    if not _HAS_SKLEARN:
        return 1
    best_k = 1
    best_score = -1
    xs = [[x] for x in x_coords]
    for k in range(1, min(max_k + 1, len(xs))):
        km = KMeans(n_clusters=k, n_init=1, random_state=0)
        labels = km.fit_predict(xs)
        if k == 1:
            best_k = 1
        else:
            from sklearn.metrics import silhouette_score
            if len(set(labels)) > 1:
                score = silhouette_score(xs, labels)
                if score > best_score:
                    best_score = score
                    best_k = k
    return best_k


class LayoutAnalyzer:
    def analyze(self, image: Image.Image) -> LayoutResult:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        n_boxes = len(data["text"])
        words = []
        for i in range(n_boxes):
            text = data["text"][i].strip()
            if not text:
                continue
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            words.append({
                "text": text,
                "x": x, "y": y, "w": w, "h": h,
                "x2": x + w, "y2": y + h,
            })

        if not words:
            return LayoutResult(blocks=[], full_text="", column_count=1, reading_order=[])

        column_count = _cluster_columns([w["x"] for w in words])

        raw_text = " ".join(w["text"] for w in words)

        group_threshold = 30
        words_sorted = sorted(words, key=lambda w: (w["y"], w["x"]))
        lines = []
        current_line = [words_sorted[0]]
        for w in words_sorted[1:]:
            if abs(w["y"] - current_line[-1]["y"]) < group_threshold:
                current_line.append(w)
            else:
                lines.append(current_line)
                current_line = [w]
        if current_line:
            lines.append(current_line)

        blocks = []
        for line_words in lines:
            line_words.sort(key=lambda w: w["x"])
            line_text = " ".join(w["text"] for w in line_words)
            avg_y = sum(w["y"] for w in line_words) // len(line_words)
            min_x = min(w["x"] for w in line_words)
            max_x2 = max(w["x2"] for w in line_words)
            max_y2 = max(w["y2"] for w in line_words)
            avg_h = sum(w["h"] for w in line_words) // len(line_words)

            block_type = "body"
            page_mid = (min(w["y2"] for w in words) + max(w["y2"] for w in words)) // 2
            if avg_y < page_mid * 0.15 and avg_h > 10:
                block_type = "header"
            elif column_count > 1:
                block_type = "column"

            blocks.append(TextBlock(
                text=line_text,
                bbox=(min_x, avg_y, max_x2, max_y2),
                block_type=block_type,
            ))

        reading_order = list(range(len(blocks)))

        return LayoutResult(
            blocks=blocks,
            full_text=raw_text,
            column_count=column_count,
            reading_order=reading_order,
        )

    def analyze_file(self, file_path: str) -> LayoutResult:
        image = Image.open(file_path)
        return self.analyze(image)


layout_analyzer = LayoutAnalyzer()
