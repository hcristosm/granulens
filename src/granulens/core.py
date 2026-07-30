import csv
from dataclasses import dataclass
import json
from pathlib import Path
import cv2
from granulens.metrics import GranulometricSummary, calculate_metrics
from granulens.segmentation import SegmentationResult, segment_grains
from granulens.visualization import plot_psd_curve, plot_segmented_overlay
import numpy as np


@dataclass
class GranuLensResult:
    """Resultado consolidado do processamento granulométrico."""

    segmentation: SegmentationResult
    summary: GranulometricSummary
    overlay_image: np.ndarray

    def save_plots(
        self, output_dir: str | Path, prefix: str = "granulens"
    ) -> tuple[Path, Path]:
        """Salva a imagem rotulada (overlay) e o gráfico da curva PSD no diretório informado."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        overlay_path = out / f"{prefix}_overlay.png"
        psd_path = out / f"{prefix}_psd_curve.png"

        # Salva imagem com transparência dos grãos
        cv2.imwrite(str(overlay_path), self.overlay_image)

        # Salva gráfico da curva acumulada
        fig = plot_psd_curve(self.summary, output_path=psd_path)
        fig.clf()

        return overlay_path, psd_path

    def export_csv(self, output_path: str | Path) -> Path:
        """Exporta as métricas individuais de cada grão para um arquivo CSV."""
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "particle_id",
            "area_px",
            "area_mm2",
            "eq_diameter_px",
            "eq_diameter_mm",
            "min_feret_mm",
            "max_feret_mm",
            "aspect_ratio",
            "sphericity",
        ]

        with open(out_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.summary.particles:
                writer.writerow(p.__dict__)

        return out_path

    def export_json(self, output_path: str | Path) -> Path:
        """Exporta o resumo estatístico consolidado e lista de partículas para JSON."""
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "total_particles": self.summary.total_particles,
            "d10": self.summary.d10,
            "d50": self.summary.d50,
            "d90": self.summary.d90,
            "mean_diameter_mm": self.summary.mean_diameter_mm,
            "std_diameter_mm": self.summary.std_diameter_mm,
            "particles": [p.__dict__ for p in self.summary.particles],
        }

        with open(out_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return out_path


class GranuLens:
    """Interface principal de alto nível para análise de granulometria digital."""

    def __init__(self, scale_mm_per_px: float = 1.0, min_distance: int = 15):
        self.scale_mm_per_px = scale_mm_per_px
        self.min_distance = min_distance

    def process(self, image_input: str | Path | np.ndarray) -> GranuLensResult:
        """Executa a pipeline completa: segmentação -> métricas -> sobreposição visual."""
        seg_res = segment_grains(image_input, min_distance=self.min_distance)
        summary = calculate_metrics(
            seg_res.markers, scale_mm_per_px=self.scale_mm_per_px
        )
        overlay = plot_segmented_overlay(
            seg_res.original_image, seg_res.markers
        )

        return GranuLensResult(
            segmentation=seg_res,
            summary=summary,
            overlay_image=overlay,
        )