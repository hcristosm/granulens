from pathlib import Path
import cv2
import numpy as np


def generate_sample_grains(output_path: str = "examples/sample_grains.png"):
    """Gera uma imagem sintética com grãos de tamanhos variados para teste."""
    # Imagem cinza escuro (fundo)
    img = np.full((600, 800, 3), 30, dtype=np.uint8)

    # Semente aleatória fixa para reprodutibilidade
    np.random.seed(42)

    # Desenha 40 grãos circulares e elípticos claros
    for _ in range(40):
        cx = np.random.randint(50, 750)
        cy = np.random.randint(50, 550)
        axes = (np.random.randint(15, 45), np.random.randint(15, 45))
        angle = np.random.randint(0, 180)
        color = (
            np.random.randint(200, 245),
            np.random.randint(200, 245),
            np.random.randint(200, 245),
        )

        cv2.ellipse(img, (cx, cy), axes, angle, 0, 360, color, -1)

    # Salva a imagem na pasta examples/
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), img)
    print(f"✅ Imagem de teste criada em: {out}")


if __name__ == "__main__":
    generate_sample_grains()