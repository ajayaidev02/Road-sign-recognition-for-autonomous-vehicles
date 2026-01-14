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

        header_style = {
            "adas": "bold white on blue",
            "safe": "bold white on green",
            "warn": "bold black on yellow",
            "ignore": "white on red",
            "unknown": "white on magenta",
        }.get(result.safety_tier, "white on blue")
        header_text = Text("Indian Road Sign Recognition", style=header_style)
        layout["header"].update(Panel(header_text, expand=True))

        body_layout = Layout()
        body_layout.split_row(
            Layout(name="detections"),
            Layout(name="llm"),
        )

        body_layout["detections"].update(self._detection_table(result))
        llm_panel = result.llm_explanation or "LLM explanation unavailable"
        body_layout["llm"].update(Panel(llm_panel, title="LLM", border_style="cyan"))
        layout["body"].update(body_layout)

        status = Text()
        status.append(f"Frame: {result.frame_id}  |  FPS: {result.fps:.1f}  |  Latency: {result.latency_ms:.1f} ms\n")
        if result.stage_latency:
            det_ms = result.stage_latency.get("detect_ms", 0)
            cls_ms = result.stage_latency.get("classify_ms", 0)
            prep_ms = result.stage_latency.get("preprocess_ms", 0)
            llm_ms = result.stage_latency.get("llm_ms", 0)
            status.append(f"Prep {prep_ms:.1f} ms | Det {det_ms:.1f} ms | Cls {cls_ms:.1f} ms | LLM {llm_ms:.1f} ms\n")
        status.append(f"Tier: {result.safety_tier} | Degraded: {result.degraded} | Manual: {result.manual_override}\n")
        status.append(f"Classification: {(result.classification.label if result.classification else 'n/a')}\n")
        if result.degraded:
            status.stylize("bold yellow")
        footer_panel = Panel(status, border_style="magenta")
        layout["footer"].update(footer_panel)

        return layout

    def _detection_table(self, result: FrameResult) -> Table:
        table = Table(title="Detections", expand=True, box=None)
        table.add_column("Label")
        table.add_column("Conf")
        table.add_column("Track")
        table.add_column("BBox")
        for det in result.detections:
            conf_style = "green" if det.confidence >= 0.6 else "yellow" if det.confidence >= 0.35 else "red"
            table.add_row(det.label, f"{det.confidence:.2f}", str(det.track_id or "-"), str(det.bbox), style=conf_style)
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
