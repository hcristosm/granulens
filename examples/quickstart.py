"""Exemplo mínimo de uso da API Python do GranuLens.

Execute a partir da raiz do repositório com:

    python examples/quickstart.py
"""

from pathlib import Path

from granulens import GranuLens

IMAGE_PATH = Path(__file__).parent / "sample_grains.png"
OUTPUT_DIR = Path(__file__).parent.parent / "results"


def main() -> None:
    # 1. Inicializa o analisador com o fator de escala (mm/px) da imagem
    analyzer = GranuLens(scale_mm_per_px=0.05, min_distance=15)

    # 2. Processa a imagem (segmentação + métricas)
    result = analyzer.process(IMAGE_PATH)

    # 3. Acessa o resumo estatístico
    summary = result.summary
    print(f"Partículas detectadas: {summary.total_particles}")
    print(f"D10: {summary.d10:.3f} mm")
    print(f"D50: {summary.d50:.3f} mm")
    print(f"D90: {summary.d90:.3f} mm")

    # 4. Salva os artefatos visuais e exporta os dados
    overlay_path, psd_path = result.save_plots(output_dir=OUTPUT_DIR)
    csv_path = result.export_csv(OUTPUT_DIR / "particle_metrics.csv")
    json_path = result.export_json(OUTPUT_DIR / "summary_stats.json")

    print(f"\nArquivos gerados em: {OUTPUT_DIR}")
    print(f"  - {overlay_path.name}")
    print(f"  - {psd_path.name}")
    print(f"  - {csv_path.name}")
    print(f"  - {json_path.name}")


if __name__ == "__main__":
    main()
