from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.table import Table

console = Console()
progress = Progress(
    TextColumn("[bold blue]{task.description}[/bold blue]"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TextColumn("[green]{task.fields.get(\'downloaded_size\', \'\')}[/green] / [cyan]{task.fields.get(\'total_size\', \'\')}[/cyan]"),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    console=console,
)

def display_banner():
    banner_text = """
██████╗ ██╗   ██╗██╗   ██╗ ██████╗  ██████╗ ████████╗ ██╗  ██╗
██╔══██╗██║   ██║██║   ██║██╔═══██╗██╔═══██╗╚══██╔══╝ ██║  ██║
██████╔╝██║   ██║██║   ██║██║   ██║██║   ██║   ██║    ███████║
██╔═══╝ ██║   ██║██║   ██║██║   ██║██║   ██║   ██║    ██╔══██║
██║     ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝   ██║    ╚═╝  ╚═╝
                                                               
    The Professional All-in-One Media Downloader Tool
    Version: 1.1.0 | Developer: PyDragonX
    """
    console.print(Panel(banner_text, title="[bold green]PyDragonX[/bold green]", border_style="blue"))

def display_platforms_table():
    table = Table(title="Supported Platforms and Quality Schedule", style="bold magenta")
    table.add_column("Platform", style="cyan", justify="left")
    table.add_column("Video Support", style="green", justify="center")
    table.add_column("Audio Support (MP3)", style="green", justify="center")
    table.add_column("4K / 1080p Resolution", style="green", justify="center")

    table.add_row("YouTube", "✅", "✅", "✅ (Full Support)")
    table.add_row("Instagram", "✅", "✅", "✅ (Reels & IGTV)")
    table.add_row("Facebook", "✅", "✅", "✅ (HD Quality)")
    table.add_row("TikTok", "✅", "✅", "✅ (No Watermark)")

    console.print(table)

def display_info(message):
    console.print(f"[bold blue]INFO:[/bold blue] {message}")

def display_success(message):
    console.print(f"[bold green]SUCCESS:[/bold green] {message}")

def display_error(message):
    console.print(f"[bold red]ERROR:[/bold red] {message}")

def display_warning(message):
    console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")
