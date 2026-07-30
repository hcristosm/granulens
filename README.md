======================================================================
GRANULENS - AUTOMATED DIGITAL GRANULOMETRY
======================================================================

DESCRICAO
---------
GranuLens e uma biblioteca e ferramenta de linha de comando em Python
projetada para automatizar a analise granulometrica digital a partir de
imagens de graos, sedimentos e particulas.

A ferramenta utiliza filtro Gaussiano, limiarizacao de Otsu, Transformada
de Distancia e o algoritmo Watershed para segmentar particulas encostadas
e calcular a curva de distribuicao acumulada (D10, D50, D90).


FUNCIONALIDADES
---------------
* Segmentacao precisa de graos adjacentes (Watershed).
* Metricas geometricas completas:
  - Area (px2 e mm2)
  - Diametro equivalente (deq)
  - Diametros de Feret (Minimo e Maximo)
  - Razao de aspecto e Esfericidade
* Analise Granulometrica (PSD): Calculo de D10, D50 e D90.
* Exportacao em PNG (overlay e grafico), CSV (particulas) e JSON (resumo).


INSTALACAO
----------
1. Dependencias do sistema (Linux / Codespaces):
   sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0

2. Instalar pacote em modo editavel:
   pip install -e ".[dev]"


COMO USAR VIA TERMINAL (CLI)
----------------------------
granulens analyze examples/sample_grains.png --scale 0.05 --output ./results

Opcoes:
  --scale, -s        Fator de conversao mm por pixel (padrao: 1.0)
  --min-distance, -d Distancia minima em px entre graos (padrao: 15)
  --output, -o       Diretorio de saida (padrao: ./results)


COMO USAR VIA PYTHON (BIBLIOTECA)
---------------------------------
from granulens.core import GranuLens

analyzer = GranuLens(scale_mm_per_px=0.05, min_distance=15)
result = analyzer.process("caminho/imagem.png")

print("D50:", result.summary.d50)
result.save_plots(output_dir="./results")
result.export_csv("./results/metricas.csv")
result.export_json("./results/resumo.json")


ESTRUTURA DO PROJETO
--------------------
granulens/
  ├── src/granulens/
  │     ├── __init__.py
  │     ├── segmentation.py
  │     ├── metrics.py
  │     ├── visualization.py
  │     ├── core.py
  │     └── cli.py
  ├── examples/
  │     └── generate_sample.py
  ├── tests/
  ├── pyproject.toml
  └── README.txt


EXECUCAO DE TESTES
------------------
pytest

======================================================================
Autor: Mateus Leptokarydis
======================================================================
