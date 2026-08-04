import numpy as np
import pytest
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


def test_calculate_metrics_scale_applied():
    # Um quadrado 10x10 px com escala 2.0 mm/px deve ter área 400 mm².
    markers = np.ones((50, 50), dtype=np.int32)
    markers[10:20, 10:20] = 2

    summary = calculate_metrics(markers, scale_mm_per_px=2.0)

    particle = summary.particles[0]
    assert particle.area_mm2 == pytest.approx(particle.area_px * 4.0)
    assert particle.eq_diameter_mm == pytest.approx(particle.eq_diameter_px * 2.0)


def test_calculate_metrics_no_particles_raises():
    # Matriz sem nenhuma partícula (apenas fundo=1) deve levantar ValueError.
    markers = np.ones((50, 50), dtype=np.int32)

    with pytest.raises(ValueError):
        calculate_metrics(markers)
