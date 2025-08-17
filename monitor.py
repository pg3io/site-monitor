#!/usr/bin/env python3
"""
Real-time website monitoring tool that checks the availability and response time of websites.
"""

import requests
import time
from datetime import datetime
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
import argparse
import os
from collections import defaultdict, deque

# Constants
TIMEOUT = 5
DEFAULT_INTERVAL = 10
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
HISTORY_SIZE = 50

# Force enable terminal features and colors
os.environ["TERM"] = "xterm-256color"
# Initialize rich console with forced terminal features
console = Console(force_terminal=True, color_system="truecolor")

# Global history storage (lost when program stops)
response_history = defaultdict(lambda: deque(maxlen=HISTORY_SIZE))

def create_sparkline(values: List[float]) -> str:
    """
    Create a sparkline from a list of response times.
    
    Args:
        values (List[float]): List of response times in ms
        
    Returns:
        str: Sparkline representation
    """
    if not values:
        return ""
    
    # Sparkline characters from low to high
    chars = "▁▂▃▄▅▆▇█"
    
    # Normalize values to 0-7 range
    min_val = min(values)
    max_val = max(values)
    
    if max_val == min_val:
        return chars[4] * len(values)  # Middle character for flat line
    
    normalized = []
    for val in values:
        # Scale to 0-7 range
        scaled = int(((val - min_val) / (max_val - min_val)) * 7)
        normalized.append(min(7, max(0, scaled)))
    
    return "".join(chars[i] for i in normalized)

def check_site(url: str) -> Dict:
    """
    Check site availability and return status and response time.

    Args:
        url (str): The URL to check

    Returns:
        Dict: Result containing timestamp, url, status, response time and availability
    """
    timestamp = datetime.now().strftime(TIME_FORMAT)
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Store response time in history
        response_history[url].append(response_time)
        
        return {
            'timestamp': timestamp,
            'url': url,
            'status': f"UP ({response.status_code})",
            'response_time': f"{response_time:.0f}ms",
            'response_time_raw': response_time,
            'is_up': response.status_code < 400
        }
        
    except requests.Timeout:
        status = 'DOWN (Timeout)'
    except requests.ConnectionError:
        status = 'DOWN (Connection Error)'
    except requests.SSLError:
        status = 'DOWN (SSL Error)'
    except requests.RequestException:
        status = 'DOWN (Unknown Error)'
    
    # For failed requests, don't add to response history
    return {
        'timestamp': timestamp,
        'url': url,
        'status': status,
        'response_time': 'N/A',
        'response_time_raw': None,
        'is_up': False
    }

def create_sparkline_panel(url: str, result: Dict) -> Panel:
    """
    Create a panel with sparkline for a specific site.
    
    Args:
        url (str): The URL being monitored
        result (Dict): Latest check result
        
    Returns:
        Panel: Rich panel with sparkline and current status
    """
    history = list(response_history[url])
    sparkline = create_sparkline(history) if history else "No data"
    
    # Pad sparkline to minimum width for better visual consistency
    if len(sparkline) < 20:
        sparkline = sparkline.ljust(20, "▁")
    
    # Create status text with current response time
    status_color = "green" if result['is_up'] else "red"
    status_text = f"[{status_color}]{result['response_time']} {result['status']}[/]"
    
    # Truncate URL for display
    display_url = url if len(url) <= 25 else url[:22] + "..."
    
    panel_content = f"{sparkline}\n{status_text}"
    return Panel(panel_content, title=display_url, title_align="left", width=35)

def create_table(results: List[Dict], current_time: str, interval: int) -> Table:
    """
    Create a rich table with monitoring results.

    Args:
        results (List[Dict]): List of check results
        current_time (str): Current timestamp
        interval (int): Check interval in seconds

    Returns:
        Table: Formatted rich table with results
    """
    title = f"Last Check: {current_time} | Check Interval: {interval}s"
    table = Table(title=title, title_style="bold blue", padding=(0, 1))
    
    # Add columns with consistent styling
    table.add_column("Time", justify="center", style="cyan")
    table.add_column("Site", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Response Time", justify="right", style="magenta")
    table.add_column("Trend", justify="center", width=25)

    # Add rows with full line coloring
    for result in results:
        style = "green" if result['is_up'] else "red"
        
        # Get sparkline for this site
        history = list(response_history[result['url']])
        sparkline = create_sparkline(history) if history else ""
        
        # Pad sparklines to consistent width to prevent overlap
        sparkline_padded = sparkline.ljust(20) if sparkline else "".ljust(20)
        
        table.add_row(
            result['timestamp'],
            result['url'],
            result['status'],
            result['response_time'],
            sparkline_padded,
            style=style
        )
    
    return table

def monitor_sites(sites: List[str], interval: int = DEFAULT_INTERVAL) -> None:
    """
    Monitor a list of sites with given interval.

    Args:
        sites (List[str]): List of URLs to monitor
        interval (int, optional): Check interval in seconds. Defaults to DEFAULT_INTERVAL.
    """
    try:
        # Clear terminal at startup
        console.clear()
        console.print("[bold blue]Starting monitoring...[/]")
        
        with Live(console=console, auto_refresh=False) as live:
            while True:
                # Check all sites concurrently using list comprehension
                results = [check_site(site) for site in sites]
                
                # Create and update table
                current_time = datetime.now().strftime(DATE_FORMAT)
                table = create_table(results, current_time, interval)
                
                # Clear and update display
                console.clear()
                live.update(table, refresh=True)
                
                # Wait for next check
                time.sleep(interval)
                
    except KeyboardInterrupt:
        console.print("\nStopping monitoring...", style="yellow")

def main() -> None:
    """
    Main function to handle command line arguments and start monitoring.
    """
    parser = argparse.ArgumentParser(
        description='Real-time website monitoring tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'sites',
        nargs='+',
        help='List of URLs to monitor'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=DEFAULT_INTERVAL,
        help='Check interval in seconds'
    )
    
    args = parser.parse_args()
    monitor_sites(args.sites, args.interval)

if __name__ == "__main__":
    main() 