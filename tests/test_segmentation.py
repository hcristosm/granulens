import numpy as np
import cv2
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
