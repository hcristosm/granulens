import numpy as np
from granulens.metrics import calculate_metrics, GranulometricSummary


def test_calculate_metrics():
    # Cria uma matriz de marcadores simulada (fundo=1, partícula_1=2, partícula_2=3)
    markers = np.ones((100, 100), dtype=np.int32)
    markers[10:30, 10:30] = 2  # Quadrado 20x20
    markers[50:85, 50:85] = 3  # Quadrado 35x35

    summary = calculate_metrics(markers, scale_mm_per_px=0.1)

    assert isinstance(summary, GranulometricSummary)
    assert summary.total_particles == 2
    assert summary.d10 <= summary.d50 <= summary.d90
    assert len(summary.particles) == 2
    assert summary.particles[0].area_mm2 > 0
