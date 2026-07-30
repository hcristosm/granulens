from pathlib import Path
import typer
from granulens.core import GranuLens

app = typer.Typer(
    name="granulens",
    help="Automated Digital Granulometry & Particle Size Distribution analysis.",
    add_completion=False,
)


@app.callback()
def main():
    """
    granulens - Ferramenta de Granulometria Digital e Processamento de Imagens
    """
    pass


@app.command("analyze")
def analyze(
    image_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Caminho para a imagem de grãos/partículas a ser analisada.",
    ),
    scale: float = typer.Option(
        1.0,
        "--scale",
        "-s",
        help="Fator de escala em mm por pixel (mm/px).",
    ),
    min_distance: int = typer.Option(
        15,
        "--min-distance",
        "-d",
        help="Distância mínima em pixels entre o centro de dois grãos encostados.",
    ),
    output: Path = typer.Option(
        Path("./results"),
        "--output",
        "-o",
        help="Diretório onde as imagens e relatórios serão salvos.",
    ),
    export_csv: bool = typer.Option(
        True,
        "--csv/--no-csv",
        help="Exportar arquivo CSV com métricas de cada grão.",
    ),
    export_json: bool = typer.Option(
        True,
        "--json/--no-json",
        help="Exportar arquivo JSON com o resumo estatístico.",
    ),
):
    """Analisa uma imagem de partículas e gera relatórios de granulometria."""
    typer.echo(f"🔬 Processando imagem: {image_path.name}...")

    try:
        analyzer = GranuLens(scale_mm_per_px=scale, min_distance=min_distance)
        result = analyzer.process(image_path)

        # Salva os plots de visualização (Overlay e PSD)
        overlay_path, psd_path = result.save_plots(output, prefix=image_path.stem)

        # Exibe resumo formatado no terminal
        summary = result.summary
        typer.secho("\n✅ Análise concluída com sucesso!", fg=typer.colors.GREEN, bold=True)
        typer.echo("─" * 40)
        typer.echo(f"📊 Partículas Detectadas: {summary.total_particles}")
        typer.echo(f"📏 Diâmetro Médio:      {summary.mean_diameter_mm:.3f} mm")
        typer.echo(f"🟢 D10 (10% passante):   {summary.d10:.3f} mm")
        typer.echo(f"🟠 D50 (Mediana):        {summary.d50:.3f} mm")
        typer.echo(f"🔴 D90 (90% passante):   {summary.d90:.3f} mm")
        typer.echo("─" * 40)

        typer.echo(f"🖼️  Overlay gerado: {overlay_path}")
        typer.echo(f"📈 Curva PSD gerada: {psd_path}")

        if export_csv:
            csv_path = result.export_csv(output / f"{image_path.stem}_metrics.csv")
            typer.echo(f"📄 Dados CSV salvos: {csv_path}")

        if export_json:
            json_path = result.export_json(output / f"{image_path.stem}_summary.json")
            typer.echo(f"📋 Dados JSON salvos: {json_path}")

    except Exception as e:
        typer.secho(f"\n❌ Erro durante o processamento: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
