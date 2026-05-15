from pathlib import Path
from app.utils.file_parser import FileParser


class OCRService:
    def __init__(self):
        self.parser = FileParser()

    def process_document(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        return self.parser.extract_text(file_path)

    def process_batch(self, file_paths: list[str]) -> dict[str, str]:
        results = {}
        for fp in file_paths:
            try:
                results[fp] = self.process_document(fp)
            except Exception as e:
                results[fp] = f"ERROR: {e}"
        return results
