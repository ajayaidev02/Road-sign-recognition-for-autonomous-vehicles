from typing import Optional
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..utils.types import FrameResult


class Dashboard:
    def __init__(self) -> None:
        self.console = Console()

    def _layout(self, result: FrameResult) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

        header_text = Text("Indian Road Sign Recognition", style="bold white on blue")
        layout["header"].update(Panel(header_text, expand=True))

        body_layout = Layout()
        body_layout.split_row(
            Layout(name="detections"),
            Layout(name="llm"),
        )

        body_layout["detections"].update(self._detection_table(result))
        body_layout["llm"].update(Panel(result.llm_explanation or "LLM explanation unavailable", title="LLM", border_style="cyan"))
        layout["body"].update(body_layout)

        status = Text()
        status.append(f"Frame: {result.frame_id}  |  FPS: {result.fps:.1f}  |  Latency: {result.latency_ms:.1f} ms\n")
        status.append(f"Degraded: {result.degraded}  |  Classification: {(result.classification.label if result.classification else 'n/a')}\n")
        if result.degraded:
            status.stylize("bold yellow")
        footer_panel = Panel(status, border_style="magenta")
        layout["footer"].update(footer_panel)

        return layout

    def _detection_table(self, result: FrameResult) -> Table:
        table = Table(title="Detections", expand=True, box=None)
        table.add_column("Label")
        table.add_column("Conf")
        table.add_column("BBox")
        for det in result.detections:
            conf_style = "green" if det.confidence >= 0.6 else "yellow" if det.confidence >= 0.35 else "red"
            table.add_row(det.label, f"{det.confidence:.2f}", str(det.bbox), style=conf_style)
        return table

    def run_live(self, result_stream):
        try:
            with Live(auto_refresh=True, console=self.console) as live:
                for result in result_stream:
                    live.update(self._layout(result))
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Interrupted by user. Shutting down...[/bold yellow]")
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {e}[/bold red]")
            raise
        finally:
            self.console.print("[dim]Dashboard closed.[/dim]")
