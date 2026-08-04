from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np
from scipy import ndimage as ndi


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
    invert_threshold: bool = False,
) -> SegmentationResult:
    """Segmenta grãos/partículas em uma imagem utilizando o algoritmo Watershed.

    Args:
        image_input: Caminho do arquivo de imagem ou matriz NumPy BGR.
        min_distance: Distância mínima estimada em pixels entre o centro de dois grãos.
        blur_kernel: Tamanho do kernel para o filtro Gaussiano.
        invert_threshold: Se True, inverte a binarização (para grãos escuros em fundo claro).

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

    # 3. Binarização usando o método de Otsu
    thresh_type = cv2.THRESH_BINARY_INV if invert_threshold else cv2.THRESH_BINARY
    _, thresh = cv2.threshold(blurred, 0, 255, thresh_type + cv2.THRESH_OTSU)

    # Remoção de pequenos ruídos com operação morfológica de abertura
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # 4. Separação de áreas conhecidas (Fundo vs. Objeto)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Transformada de Distância para identificar os centros dos grãos
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # Marcadores via máximos locais da transformada de distância: cada pico
    # isolado por pelo menos `min_distance` pixels de outros picos vira a
    # semente de um grão distinto, permitindo ao Watershed separar grãos
    # encostados/sobrepostos em vez de tratá-los como um único blob.
    footprint_size = max(3, 2 * min_distance + 1)
    local_max = ndi.maximum_filter(dist_transform, size=footprint_size) == dist_transform
    local_max &= dist_transform > 0.05 * dist_transform.max()
    sure_fg = (local_max * 255).astype(np.uint8)

    unknown = cv2.subtract(sure_bg, sure_fg)

    # 5. Algoritmo Watershed
    num_labels, markers = cv2.connectedComponents(sure_fg)

    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(img, markers)

    total_particles = int(np.max(markers) - 1)

    return SegmentationResult(
        original_image=img,
        gray_image=gray,
        binary_mask=opening,
        markers=markers,
        num_particles=total_particles,
    )
