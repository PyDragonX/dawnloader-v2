"""Rich terminal interface for PyDragonX."""

from __future__ import annotations

import os
from urllib.parse import urlparse

from InquirerPy import inquirer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table

console = Console()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_banner() -> None:
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
[bold white]Version: 2.0.0 | Developer: PyDragonX | Powered by yt-dlp[/bold white]
    """
    console.print(Align.center(Panel(banner_text, border_style="blue", expand=False)))


def display_platforms_table() -> None:
    table = Table(
        title="[bold magenta]Supported Platforms & Quality Matrix[/bold magenta]",
        style="bold white",
        show_header=True,
        header_style="bold cyan",
    )
    for name, style in (("Platform", "yellow"), ("Video", "green"), ("Audio", "green"), ("Max Quality", "blue"), ("Status", "green")):
        table.add_column(name, style=style, justify="center" if name != "Platform" else "left")
    for row in [
        ("YouTube", "✅", "✅", "4K / 8K", "Stable"),
        ("Instagram", "✅", "✅", "1080p", "Stable"),
        ("Facebook", "✅", "✅", "HD", "Stable"),
        ("TikTok", "✅", "✅", "Best available", "Stable"),
        ("Twitter (X)", "✅", "✅", "HD", "Supported"),
        ("Kwai", "✅", "✅", "HD", "Supported"),
        ("SoundCloud", "❌", "✅", "HQ Audio", "Supported"),
    ]:
        table.add_row(*row)
    console.print(Align.center(table))


def select_device_and_os() -> tuple[str, str]:
    device_type = inquirer.select(
        message="[PyDragonX] Select your device type:",
        choices=["Phone", "Laptop/PC"],
        default="Laptop/PC",
    ).execute()
    if device_type == "Phone":
        os_type = inquirer.select(
            message="[PyDragonX] Select your Phone OS:",
            choices=["Android (Termux)", "iOS (iSH/Other)"],
            default="Android (Termux)",
        ).execute()
    else:
        os_type = inquirer.select(
            message="[PyDragonX] Select your Laptop/PC OS:",
            choices=["Windows", "Linux", "macOS"],
            default="Linux",
        ).execute()
    return device_type, os_type


def select_platform() -> str:
    return inquirer.select(
        message="[PyDragonX] Select Target Platform:",
        choices=["YouTube", "Instagram", "Facebook", "TikTok", "Twitter (X)", "Kwai", "SoundCloud", "Auto-Detect (Clipboard)", "Exit"],
        default="YouTube",
    ).execute()


def select_file_type() -> str:
    return inquirer.select(
        message="[PyDragonX] Select Output Format:",
        choices=["Video (MP4) - Best Quality", "Audio (MP3) - High Quality", "Audio (WAV) - Lossless"],
        default="Video (MP4) - Best Quality",
    ).execute()


def is_valid_media_url(value: str) -> bool:
    """Accept HTTP(S) media URLs and reject malformed/local input."""
    if not isinstance(value, str) or len(value.strip()) > 4096:
        return False
    try:
        parsed = urlparse(value.strip())
        hostname = parsed.hostname or ""
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and "." in hostname


def get_url_input() -> str:
    return inquirer.text(
        message="[PyDragonX] Paste Media Link:",
        validate=lambda value: True if is_valid_media_url(value) else "Enter a valid http/https media URL.",
    ).execute().strip()


def get_progress_bar() -> Progress:
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


def display_info(message: str) -> None:
    console.print(f"[bold blue]ℹ INFO:[/bold blue] {message}")


def display_success(message: str) -> None:
    console.print(f"[bold green]✔ SUCCESS:[/bold green] {message}")


def display_error(message: str) -> None:
    console.print(f"[bold red]✘ ERROR:[/bold red] {message}")


def display_warning(message: str) -> None:
    console.print(f"[bold yellow]⚠ WARNING:[/bold yellow] {message}")
