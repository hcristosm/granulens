import numpy as np
import cv2
import pytest
from granulens.segmentation import segment_grains, SegmentationResult


def test_segment_grains_synthetic():
    # Cria uma imagem sintética 200x200 com 2 grãos brancos em fundo preto
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(img, (50, 50), 20, (255, 255, 255), -1)
    cv2.circle(img, (140, 140), 30, (255, 255, 255), -1)

    result = segment_grains(img, min_distance=10)

    assert isinstance(result, SegmentationResult)
    assert result.num_particles >= 2
    assert result.markers.shape == (200, 200)
    assert result.binary_mask is not None


def test_segment_grains_separates_touching_circles():
    # Dois círculos brancos encostados (centros a 55px, raios 30) devem ser
    # detectados como 2 partículas distintas, não fundidos em uma só.
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    cv2.circle(img, (100, 100), 30, (255, 255, 255), -1)
    cv2.circle(img, (155, 100), 30, (255, 255, 255), -1)

    result = segment_grains(img, min_distance=15)

    assert result.num_particles == 2


def test_segment_grains_invert_threshold():
    # Grãos escuros em fundo claro só são detectados corretamente com
    # invert_threshold=True.
    img = np.full((200, 200, 3), 255, dtype=np.uint8)
    cv2.circle(img, (60, 60), 20, (0, 0, 0), -1)
    cv2.circle(img, (140, 140), 25, (0, 0, 0), -1)

    result = segment_grains(img, min_distance=10, invert_threshold=True)

    assert result.num_particles >= 2


def test_segment_grains_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        segment_grains("caminho/que/nao/existe.png")
