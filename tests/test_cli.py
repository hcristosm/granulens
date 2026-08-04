import cv2
import numpy as np
from typer.testing import CliRunner
from granulens.cli import app

runner = CliRunner()


def _write_sample_image(path) -> None:
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(img, (60, 60), 25, (255, 255, 255), -1)
    cv2.circle(img, (140, 140), 30, (255, 255, 255), -1)
    cv2.imwrite(str(path), img)


def test_analyze_command(tmp_path):
    image_path = tmp_path / "grains.png"
    _write_sample_image(image_path)
    output_dir = tmp_path / "results"

    result = runner.invoke(
        app,
        ["analyze", str(image_path), "--scale", "0.1", "--output", str(output_dir)],
    )

    assert result.exit_code == 0
    assert "Partículas Detectadas" in result.stdout
    assert (output_dir / "grains_overlay.png").exists()
    assert (output_dir / "grains_metrics.csv").exists()
    assert (output_dir / "grains_summary.json").exists()


def test_analyze_command_no_csv_no_json(tmp_path):
    image_path = tmp_path / "grains.png"
    _write_sample_image(image_path)
    output_dir = tmp_path / "results"

    result = runner.invoke(
        app,
        [
            "analyze",
            str(image_path),
            "--scale",
            "0.1",
            "--output",
            str(output_dir),
            "--no-csv",
            "--no-json",
        ],
    )

    assert result.exit_code == 0
    assert not (output_dir / "grains_metrics.csv").exists()
    assert not (output_dir / "grains_summary.json").exists()


def test_analyze_command_missing_file(tmp_path):
    result = runner.invoke(app, ["analyze", str(tmp_path / "nao_existe.png")])

    assert result.exit_code != 0
