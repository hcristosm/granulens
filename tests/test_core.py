import json
import cv2
import numpy as np
from granulens import GranuLens
from granulens.core import GranuLensResult


def _sample_image() -> np.ndarray:
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(img, (60, 60), 25, (255, 255, 255), -1)
    cv2.circle(img, (140, 140), 30, (255, 255, 255), -1)
    return img


def test_process_returns_result():
    analyzer = GranuLens(scale_mm_per_px=0.1, min_distance=10)
    result = analyzer.process(_sample_image())

    assert isinstance(result, GranuLensResult)
    assert result.summary.total_particles == 2
    assert result.overlay_image.shape == (200, 200, 3)


def test_export_csv(tmp_path):
    analyzer = GranuLens(scale_mm_per_px=0.1, min_distance=10)
    result = analyzer.process(_sample_image())

    csv_path = result.export_csv(tmp_path / "metrics.csv")

    assert csv_path.exists()
    content = csv_path.read_text(encoding="utf-8")
    assert "particle_id" in content
    assert content.count("\n") == 3  # cabeçalho + 2 partículas


def test_export_json(tmp_path):
    analyzer = GranuLens(scale_mm_per_px=0.1, min_distance=10)
    result = analyzer.process(_sample_image())

    json_path = result.export_json(tmp_path / "summary.json")

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["total_particles"] == 2
    assert len(data["particles"]) == 2


def test_save_plots(tmp_path):
    analyzer = GranuLens(scale_mm_per_px=0.1, min_distance=10)
    result = analyzer.process(_sample_image())

    overlay_path, psd_path = result.save_plots(tmp_path)

    assert overlay_path.exists()
    assert psd_path.exists()
