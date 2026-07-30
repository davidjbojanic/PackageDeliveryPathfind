"""
display.py

Lightweight terminal presentation helpers for the WGUPS Routing Program.
Uses only ANSI escape codes from the standard library, so no third-party
packages are required (works in any modern terminal on macOS, Linux, or
Windows Terminal / PowerShell / VS Code's integrated terminal).

This module only affects *how* things are printed. It contains no
routing, hashing, or scheduling logic.
"""

import os
import re
from datetime import datetime, time as dtime

# Enable ANSI escape sequence processing on classic Windows consoles.
if os.name == "nt":
    os.system("")

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
GRAY = "\033[90m"
WHITE = "\033[97m"

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def _visible_len(s):
    """Length of a string, ignoring ANSI escape codes."""
    return len(_ANSI_RE.sub("", str(s)))


def color(text, code):
    return f"{code}{text}{RESET}"


def format_time(value):
    """Format a datetime / datetime.time value for display. Leaves
    plain strings (like 'NA') untouched."""
    if isinstance(value, datetime):
        return value.strftime("%I:%M %p").lstrip("0")
    if isinstance(value, dtime):
        return value.strftime("%I:%M %p").lstrip("0")
    return str(value)


def status_badge(status):
    status = str(status)
    if status == "delivered":
        return color("● delivered", GREEN)
    if status == "en route":
        return color("● en route", YELLOW)
    if status == "at the hub":
        return color("● at the hub", GRAY)
    return status


def banner(title, subtitle=None, width=64):
    top = "╔" + "═" * (width - 2) + "╗"
    bottom = "╚" + "═" * (width - 2) + "╝"
    print(color(top, CYAN))
    print(color("║", CYAN) + color(title.center(width - 2), BOLD + WHITE) + color("║", CYAN))
    if subtitle:
        print(color("║", CYAN) + color(subtitle.center(width - 2), DIM) + color("║", CYAN))
    print(color(bottom, CYAN))


def section(title):
    print()
    line = f"── {title} "
    fill = "─" * max(2, 60 - len(title))
    print(color(line, BOLD + CYAN) + color(fill, CYAN))


def menu(options):
    """options: list of (key, label) tuples"""
    print()
    for key, label in options:
        print(f"  {color(key, BOLD + CYAN)}  {label}")
    print()


def print_table(headers, rows, title=None):
    """Print a box-drawn table. Cells may contain ANSI color codes;
    column widths are computed on visible length only."""
    widths = [_visible_len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], _visible_len(cell))

    def fmt_row(cells):
        parts = []
        for cell, w in zip(cells, widths):
            pad = w - _visible_len(cell)
            parts.append(str(cell) + " " * pad)
        return " │ ".join(parts)

    top = "┌─" + "─┬─".join("─" * w for w in widths) + "─┐"
    mid = "├─" + "─┼─".join("─" * w for w in widths) + "─┤"
    bottom = "└─" + "─┴─".join("─" * w for w in widths) + "─┘"

    if title:
        print(color(title, BOLD + CYAN))
    print(color(top, GRAY))
    print(color("│ ", GRAY) + fmt_row([color(h, BOLD) for h in headers]) + color(" │", GRAY))
    print(color(mid, GRAY))
    for row in rows:
        print(color("│ ", GRAY) + fmt_row(row) + color(" │", GRAY))
    print(color(bottom, GRAY))
    if not rows:
        print(color("  (no packages loaded yet)", DIM))


def print_package_panel(package):
    """Pretty box display of a single package's attributes."""
    fields = [
        ("ID", package.id),
        ("Address", package.address),
        ("City", package.city),
        ("Zip", package.zip),
        ("Deadline", format_time(package.delivery_deadline)),
        ("Weight", package.weight),
        ("Status", status_badge(package.status)),
        ("Dropoff", format_time(package.dropoff)),
    ]
    label_w = max(len(label) for label, _ in fields)
    content_w = max(_visible_len(f"{label + ':':<{label_w + 1}} {value}") for label, value in fields)
    width = content_w + 2

    print(color("┌" + "─" * width + "┐", CYAN))
    for label, value in fields:
        text = f" {label + ':':<{label_w + 1}} {value}"
        pad = width - _visible_len(text)
        print(color("│", CYAN) + text + " " * pad + color("│", CYAN))
    print(color("└" + "─" * width + "┘", CYAN))


def mileage_summary(total_mileage):
    text = f" Total mileage: {round(total_mileage, 1)} mi "
    print(color("┏" + "━" * (len(text)) + "┓", YELLOW))
    print(color("┃", YELLOW) + color(text, BOLD + WHITE) + color("┃", YELLOW))
    print(color("┗" + "━" * (len(text)) + "┛", YELLOW))


def error(message):
    print(color(f"✗ {message}", RED))


def info(message):
    print(color(message, DIM))
