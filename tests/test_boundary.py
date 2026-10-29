from pathlib import Path
import unittest


class PublicBoundary(unittest.TestCase):
    def test_no_model_training_or_result_artifacts(self):
        root=Path(__file__).resolve().parents[1]
        excluded={'.git','target','node_modules','__pycache__','.venv','.dart_tool'}
        forbidden={'model.py','train.py','core.py','checkpoint.pt','fixtures.json','rows.json','rows.jsonl'}
        for file in root.rglob('*'):
            if not file.is_file() or any(part in excluded for part in file.relative_to(root).parts):continue
            self.assertNotIn(file.name,forbidden)
            self.assertNotIn(file.suffix,{'.safetensors','.pt','.pth','.bundle','.parquet','.gz'})
