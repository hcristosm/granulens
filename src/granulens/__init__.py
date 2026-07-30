from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np


@dataclass
class SegmentationResult:
    """Dataclass para armazenar as saídas do processo de segmentação."""
    original_image: np.ndarray
    gray_image: np.ndarray
    binary_mask: np.ndarray
    markers: np.ndarray
    num_particles: int


def segment_grains(
    image_input: str | Path | np.ndarray,
    min_distance: int = 15,
    blur_kernel: tuple[int, int] = (5, 5),
) -> SegmentationResult:
    """Segmenta grãos/partículas em uma imagem utilizando o algoritmo Watershed.

    Args:
        image_input: Caminho do arquivo de imagem ou matriz NumPy BGR.
        min_distance: Distância mínima estimada em pixels entre o centro de dois grãos.
        blur_kernel: Tamanho do kernel para o filtro Gaussiano.

    Returns:
        SegmentationResult contendo a imagem original, máscaras e número de partículas.
    """
    # 1. Carregamento da imagem
    if isinstance(image_input, (str, Path)):
        img = cv2.imread(str(image_input))
        if img is None:
            raise FileNotFoundError(f"Não foi possível carregar a imagem: {image_input}")
    else:
        img = image_input.copy()

    # 2. Pré-processamento: Conversão para escala de cinza e suavização
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)

    # 3. Binarização usando o método de Otsu (Inverso: grãos claros em fundo escuro)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Remoção de pequenos ruídos com operação morfológica de abertura
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # 4. Separação de áreas conhecidas (Fundo vs. Objeto)
    # Áreas garantidamente de fundo (background)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Transformada de Distância para identificar os centros dos grãos
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # O limiar determina o quão 'separados' os centros precisam estar
    thresh_value = 0.3 * dist_transform.max() if min_distance <= 0 else (min_distance / 100.0) * dist_transform.max()
    _, sure_fg = cv2.threshold(dist_transform, thresh_value, 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Região incerta (fronteiras entre grãos encostados)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 5. Algoritmo Watershed
    # Rotulagem dos componentes conectados (marcadores)
    num_labels, markers = cv2.connectedComponents(sure_fg)

    # Incrementa 1 em todos os rótulos para garantir que o fundo seja 1 em vez de 0
    markers = markers + 1

    # Marca a região desconhecida com 0 para o Watershed definir as fronteiras
    markers[unknown == 255] = 0

    # Aplica o algoritmo Watershed na imagem original
    markers = cv2.watershed(img, markers)

    # O número total de partículas detectadas exclui o fundo (rotulado como 1) e as bordas (-1)
    total_particles = int(np.max(markers) - 1)

    return SegmentationResult(
        original_image=img,
        gray_image=gray,
        binary_mask=opening,
        markers=markers,
        num_particles=total_particles,
    )