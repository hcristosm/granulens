from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np
from granulens.metrics import GranulometricSummary


def plot_segmented_overlay(
    original_image: np.ndarray,
    markers: np.ndarray,
    alpha: float = 0.35,
) -> np.ndarray:
    """Gera uma imagem com cada grão destacado por uma cor transparente e bordas realçadas.

    Args:
        original_image: Matriz BGR da imagem original.
        markers: Matriz de rótulos gerada pelo Watershed.
        alpha: Nível de transparência das cores dos grãos (0.0 a 1.0).

    Returns:
        Matriz BGR da imagem com a sobreposição visual (overlay).
    """
    overlay = original_image.copy()
    unique_markers = np.unique(markers)
    unique_markers = unique_markers[unique_markers > 1]  # Exclui fundo e bordas

    if len(unique_markers) == 0:
        return overlay

    # Semente fixa para garantir que as cores sejam reprodutíveis
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(unique_markers) + 2, 3), dtype=np.uint8)

    colored_mask = np.zeros_like(original_image, dtype=np.uint8)

    for idx, pid in enumerate(unique_markers):
        mask = markers == pid
        colored_mask[mask] = colors[idx]

    # Aplica transparência colorida sobre os grãos
    cv2.addWeighted(colored_mask, alpha, overlay, 1.0 - alpha, 0, overlay)

    # Desenha as bordas de separação do Watershed em amarelo forte
    overlay[markers == -1] = [0, 255, 255]

    return overlay


def plot_psd_curve(
    summary: GranulometricSummary,
    output_path: str | Path | None = None,
    title: str = "Curva Granulométrica Acumulada (PSD)",
) -> plt.Figure:
    """Gera o gráfico da curva acumulada com destaque para D10, D50 e D90.

    Args:
        summary: Objeto GranulometricSummary retornado pelo módulo de métricas.
        output_path: Caminho opcional para salvar a figura em disco (PNG/PDF).
        title: Título do gráfico.

    Returns:
        Objeto Figure do Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

    diameters, cumulative = summary.cumulative_curve

    # Curva principal acumulada
    ax.plot(
        diameters,
        cumulative,
        color="#1f77b4",
        linewidth=2.5,
        label="Acumulado (% passante)",
    )

    # Marcações horizontais e verticais para D10, D50 e D90
    indicators = [
        (summary.d10, 10, f"D10 = {summary.d10:.2f} mm", "#2ca02c"),
        (summary.d50, 50, f"D50 = {summary.d50:.2f} mm", "#ff7f0e"),
        (summary.d90, 90, f"D90 = {summary.d90:.2f} mm", "#d62728"),
    ]

    for d_val, pct, label, color in indicators:
        ax.axhline(pct, color=color, linestyle="--", linewidth=1, alpha=0.6)
        ax.axvline(d_val, color=color, linestyle="--", linewidth=1, alpha=0.6)
        ax.plot(d_val, pct, "o", color=color, label=label, markersize=7)

    ax.set_xlabel("Diâmetro Equivalente (mm)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Porcentagem Acumulada (%)", fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=15)
    ax.set_ylim(0, 105)
    ax.set_xlim(left=0)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", frameon=True)

    plt.tight_layout()

    if output_path:
        fig.savefig(str(output_path), bbox_inches="tight")

    return fig