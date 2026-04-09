import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from InquirerPy import inquirer

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    banner_text = """
[bold cyan]
██████╗ ██╗   ██╗██╗   ██╗ ██████╗  ██████╗ ████████╗ ██╗  ██╗
██╔══██╗██║   ██║██║   ██║██╔═══██╗██╔═══██╗╚══██╔══╝ ██║  ██║
██████╔╝██║   ██║██║   ██║██║   ██║██║   ██║   ██║    ███████║
██╔═══╝ ██║   ██║██║   ██║██║   ██║██║   ██║   ██║    ██╔══██║
██║     ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝   ██║    ╚═╝  ╚═╝
[/bold cyan]
[bold green]The Ultimate All-in-One Media Downloader System[/bold green]
[bold white]Version: 1.2.0 | Developer: PyDragonX | Powered by yt-dlp[/bold white]
    """
    console.print(Align.center(Panel(banner_text, border_style="blue", expand=False)))

def display_platforms_table():
    table = Table(title="[bold magenta]Supported Platforms & Quality Matrix[/bold magenta]", style="bold white", show_header=True, header_style="bold cyan")
    table.add_column("Platform", style="yellow", justify="left")
    table.add_column("Video", style="green", justify="center")
    table.add_column("Audio", style="green", justify="center")
    table.add_column("Max Quality", style="blue", justify="center")
    table.add_column("Status", style="green", justify="center")

    platforms = [
        ("YouTube", "✅", "✅", "4K / 8K", "Stable"),
        ("Instagram", "✅", "✅", "1080p", "Stable"),
        ("Facebook", "✅", "✅", "HD", "Stable"),
        ("TikTok", "✅", "✅", "No Watermark", "Stable"),
        ("Twitter (X)", "✅", "✅", "HD", "New"),
        ("Kwai", "✅", "✅", "HD", "New"),
        ("SoundCloud", "❌", "✅", "HQ Audio", "New"),
    ]

    for p in platforms:
        table.add_row(*p)

    console.print(Align.center(table))

def select_device_and_os():
    device_type = inquirer.select(
        message="[PyDragonX] Select your device type:",
        choices=["Phone", "Laptop/PC"],
        default="Laptop/PC"
    ).execute()

    if device_type == "Phone":
        os_type = inquirer.select(
            message="[PyDragonX] Select your Phone OS:",
            choices=["Android (Termux)", "iOS (iSH/Other)"],
            default="Android (Termux)"
        ).execute()
    else:
        os_type = inquirer.select(
            message="[PyDragonX] Select your Laptop/PC OS:",
            choices=["Windows", "Linux", "macOS"],
            default="Windows"
        ).execute()
    
    return device_type, os_type

def select_platform():
    return inquirer.select(
        message="[PyDragonX] Select Target Platform:",
        choices=[
            "YouTube",
            "Instagram",
            "Facebook",
            "TikTok",
            "Twitter (X)",
            "Kwai",
            "SoundCloud",
            "Auto-Detect (Clipboard)",
            "Exit"
        ],
        default="YouTube"
    ).execute()

def select_file_type():
    return inquirer.select(
        message="[PyDragonX] Select Output Format:",
        choices=[
            "Video (MP4) - Best Quality",
            "Audio (MP3) - High Quality",
            "Audio (WAV) - Lossless"
        ],
        default="Video (MP4) - Best Quality"
    ).execute()

def get_url_input():
    return inquirer.text(
        message="[PyDragonX] Paste Media Link:",
        validate=lambda result: len(result) > 0 or "URL cannot be empty!"
    ).execute()

def get_progress_bar():
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        BarColumn(bar_width=None, pulse_style="cyan"),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        TextColumn("[green]{task.fields[downloaded_size]}[/green] / [cyan]{task.fields[total_size]}[/cyan]"),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
        console=console,
    )

progress = get_progress_bar()

def display_info(message):
    console.print(f"[bold blue]ℹ INFO:[/bold blue] {message}")

def display_success(message):
    console.print(f"[bold green]✔ SUCCESS:[/bold green] {message}")

def display_error(message):
    console.print(f"[bold red]✘ ERROR:[/bold red] {message}")

def display_warning(message):
    console.print(f"[bold yellow]⚠ WARNING:[/bold yellow] {message}")
