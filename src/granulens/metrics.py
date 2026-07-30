from dataclasses import dataclass
import cv2
import numpy as np


@dataclass
class ParticleMetrics:
    """Métricas geométricas individuais de uma única partícula/grão."""

    particle_id: int
    area_px: float
    area_mm2: float
    eq_diameter_px: float
    eq_diameter_mm: float
    min_feret_mm: float
    max_feret_mm: float
    aspect_ratio: float
    sphericity: float


@dataclass
class GranulometricSummary:
    """Resumo estatístico granulométrico consolidado da amostra."""

    total_particles: int
    d10: float
    d50: float
    d90: float
    mean_diameter_mm: float
    std_diameter_mm: float
    particles: list[ParticleMetrics]
    diameters_mm: np.ndarray
    cumulative_curve: tuple[np.ndarray, np.ndarray]  # (diâmetros_ordenados, porcentagens_acumuladas)


def calculate_metrics(
    markers: np.ndarray,
    scale_mm_per_px: float = 1.0,
) -> GranulometricSummary:
    """Calcula as métricas geométricas de cada grão e a curva granulométrica acumulada.

    Args:
        markers: Matriz de rótulos do Watershed (fundo=1, bordas=-1, partículas>=2).
        scale_mm_per_px: Fator de conversão de escala (milímetros por pixel).

    Returns:
        GranulometricSummary contendo estatísticas individuais e os valores de D10, D50 e D90.
    """
    particle_ids = np.unique(markers)
    # Filtra o fundo (1), as bordas (-1) e áreas inválidas (<= 0)
    particle_ids = particle_ids[particle_ids > 1]

    particles: list[ParticleMetrics] = []
    diameters_mm: list[float] = []

    for pid in particle_ids:
        # Isolamento do contorno da partícula atual
        mask = np.uint8(markers == pid)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            continue

        cnt = contours[0]
        area_px = float(cv2.contourArea(cnt))
        if area_px <= 0:
            continue

        perimeter_px = float(cv2.arcLength(cnt, True))

        # Diâmetro equivalente: d_eq = 2 * sqrt(Area / pi)
        eq_diameter_px = 2.0 * np.sqrt(area_px / np.pi)

        # Conversão de unidades para milímetros
        area_mm2 = area_px * (scale_mm_per_px**2)
        eq_diameter_mm = eq_diameter_px * scale_mm_per_px

        # Retângulo delimitador de área mínima para os Diâmetros de Feret
        rect = cv2.minAreaRect(cnt)
        (width_px, height_px) = rect[1]

        min_feret_px = min(width_px, height_px)
        max_feret_px = max(width_px, height_px)

        min_feret_mm = min_feret_px * scale_mm_per_px
        max_feret_mm = max_feret_px * scale_mm_per_px

        # Forma e esfericidade
        aspect_ratio = max_feret_px / min_feret_px if min_feret_px > 0 else 1.0
        sphericity = (
            (4.0 * np.pi * area_px) / (perimeter_px**2)
            if perimeter_px > 0
            else 0.0
        )
        sphericity = min(sphericity, 1.0)  # Ajuste de discretização

        particle = ParticleMetrics(
            particle_id=int(pid),
            area_px=area_px,
            area_mm2=area_mm2,
            eq_diameter_px=eq_diameter_px,
            eq_diameter_mm=eq_diameter_mm,
            min_feret_mm=min_feret_mm,
            max_feret_mm=max_feret_mm,
            aspect_ratio=aspect_ratio,
            sphericity=sphericity,
        )

        particles.append(particle)
        diameters_mm.append(eq_diameter_mm)

    if not particles:
        raise ValueError(
            "Nenhuma partícula válida foi encontrada na imagem para cálculo de métricas."
        )

    diameters_arr = np.array(diameters_mm)

    # Estatísticas e diâmetros característicos D10, D50 e D90
    d10 = float(np.percentile(diameters_arr, 10))
    d50 = float(np.percentile(diameters_arr, 50))
    d90 = float(np.percentile(diameters_arr, 90))

    mean_diameter_mm = float(np.mean(diameters_arr))
    std_diameter_mm = float(np.std(diameters_arr))

    # Curva granulométrica acumulada
    sorted_diameters = np.sort(diameters_arr)
    cumulative_percentages = np.linspace(
        100.0 / len(sorted_diameters), 100.0, len(sorted_diameters)
    )

    return GranulometricSummary(
        total_particles=len(particles),
        d10=d10,
        d50=d50,
        d90=d90,
        mean_diameter_mm=mean_diameter_mm,
        std_diameter_mm=std_diameter_mm,
        particles=particles,
        diameters_mm=sorted_diameters,
        cumulative_curve=(sorted_diameters, cumulative_percentages),
    )