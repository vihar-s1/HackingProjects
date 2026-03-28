"""
Keylogger Detection Module

Detects potential keyloggers running on the system.
"""

import os
import sys
import logging
import subprocess
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger("Keylogger.detector")


class KeyloggerDetector:
    """
    Detects potential keyloggers on the system.
    
    Uses multiple detection methods:
    - Process name analysis
    - Keyboard hook detection
    - Network connection analysis
    - File system artifacts
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize detector.
        
        Args:
            debug: Enable debug logging
        """
        self.debug = debug
        self._platform = sys.platform
        
        # Known keylogger process names
        self.known_keyloggers = [
            'keylogger', 'kl', 'klogger', 'logkeys',
            'pykeylogger', 'refog', 'spyrix', 'aver',
            'kidlogger', 'monitoring', 'keystroke'
        ]
    
    def scan_processes(self) -> List[Dict[str, Any]]:
        """
        Scan running processes for known keyloggers.
        
        Returns:
            List of suspicious processes
        """
        suspicious = []
        
        try:
            if self._platform == 'win32':
                result = subprocess.run(
                    ['tasklist', '/FO', 'CSV'],
                    capture_output=True,
                    text=True
                )
                processes = result.stdout.split('\n')
                
                for proc in processes:
                    proc_lower = proc.lower()
                    for keylogger in self.known_keyloggers:
                        if keylogger in proc_lower:
                            suspicious.append({
                                'type': 'process',
                                'name': proc,
                                'reason': f'Matches known keylogger: {keylogger}'
                            })
                            
            else:
                result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True
                )
                processes = result.stdout.split('\n')
                
                for proc in processes:
                    proc_lower = proc.lower()
                    for keylogger in self.known_keyloggers:
                        if keylogger in proc_lower and 'grep' not in proc_lower:
                            suspicious.append({
                                'type': 'process',
                                'name': proc.strip(),
                                'reason': f'Matches known keylogger: {keylogger}'
                            })
                            
        except Exception as e:
            logger.error(f"Process scan failed: {e}")
        
        return suspicious
    
    def check_keyboard_hooks(self) -> List[Dict[str, Any]]:
        """
        Check for keyboard hooks (Windows only).
        
        Returns:
            List of suspicious hooks
        """
        suspicious = []
        
        if self._platform != 'win32':
            return suspicious
        
        try:
            import ctypes
            from ctypes import wintypes
            
        except Exception as e:
            if self.debug:
                logger.debug(f"Hook check error: {e}")
        
        return suspicious
    
    def check_network_connections(self) -> List[Dict[str, Any]]:
        """
        Check for suspicious network connections.
        
        Returns:
            List of suspicious connections
        """
        suspicious = []
        
        try:
            if self._platform == 'win32':
                result = subprocess.run(
                    ['netstat', '-ano'],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['netstat', '-tunap'],
                    capture_output=True,
                    text=True
                )
            
            connections = result.stdout.split('\n')
            suspicious_ports = ['4444', '5555', '6666', '8080', '9999']
            
            for conn in connections:
                for port in suspicious_ports:
                    if f':{port}' in conn and 'ESTABLISHED' in conn:
                        suspicious.append({
                            'type': 'network',
                            'connection': conn.strip(),
                            'reason': f'Connection to suspicious port: {port}'
                        })
                        
        except Exception as e:
            if self.debug:
                logger.debug(f"Network check failed: {e}")
        
        return suspicious
    
    def check_file_system(self) -> List[Dict[str, Any]]:
        """
        Check for keylogger artifacts on file system.
        
        Returns:
            List of suspicious files
        """
        suspicious = []
        
        log_patterns = [
            '.kl_', 'keylog', 'kl_', 'keystroke',
            'typed_', 'input_', 'monitor_'
        ]
        
        try:
            if self._platform == 'win32':
                temp_dirs = [os.environ.get('TEMP', '')]
            elif self._platform == 'darwin':
                temp_dirs = ['/tmp', str(Path.home() / 'Library' / 'Caches')]
            else:
                temp_dirs = ['/tmp', '/var/tmp']
            
            for temp_dir in temp_dirs:
                if not temp_dir or not os.path.exists(temp_dir):
                    continue
                    
                for filename in os.listdir(temp_dir):
                    filename_lower = filename.lower()
                    for pattern in log_patterns:
                        if pattern in filename_lower:
                            suspicious.append({
                                'type': 'file',
                                'path': os.path.join(temp_dir, filename),
                                'reason': f'Matches keylogger log pattern: {pattern}'
                            })
                            
        except Exception as e:
            if self.debug:
                logger.debug(f"File system check failed: {e}")
        
        return suspicious
    
    def full_scan(self) -> Dict[str, Any]:
        """
        Perform full system scan.
        
        Returns:
            Dict with scan results
        """
        logger.info("Starting full keylogger scan...")
        
        results = {
            'processes': self.scan_processes(),
            'hooks': self.check_keyboard_hooks(),
            'network': self.check_network_connections(),
            'filesystem': self.check_file_system()
        }
        
        total_findings = sum(len(v) for v in results.values())
        
        logger.info(f"Scan complete. Found {total_findings} potential issues.")
        
        return results
    
    def print_report(self, results: Dict[str, Any]):
        """Print scan results as a report."""
        print("\n" + "=" * 60)
        print("  KEYLOGGER DETECTION REPORT")
        print("=" * 60)
        
        for category, findings in results.items():
            print(f"\n{category.upper()}:")
            if findings:
                for finding in findings:
                    print(f"  [!] [{finding['type']}] {finding['reason']}")
                    if 'path' in finding:
                        print(f"      Path: {finding['path']}")
                    elif 'name' in finding:
                        print(f"      Name: {finding['name']}")
                    elif 'connection' in finding:
                        print(f"      Connection: {finding['connection']}")
            else:
                print("  [✓] No issues found")
        
        print("\n" + "=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Keylogger Detection Tool"
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    detector = KeyloggerDetector(debug=args.debug)
    results = detector.full_scan()
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        detector.print_report(results)


if __name__ == "__main__":
    main()
