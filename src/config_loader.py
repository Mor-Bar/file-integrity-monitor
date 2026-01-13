"""
Configuration loader for File Integrity Monitor.
"""

import json
import os
from .constants import (
    DEFAULT_ALGORITHM,
    DEFAULT_BASELINE_FILE,
    DEFAULT_IGNORE_FILE,
    CHUNK_SIZE,
    LOG_FILE,
    SEPARATOR_LENGTH,
    HASH_DISPLAY_LENGTH
)
from .logger import logger


class ConfigLoader:
    """Load and manage configuration from file."""
    
    def __init__(self, config_file='config.json'):
        """
        Initialize configuration loader.
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Load configuration from file or use defaults.
        
        Returns:
            dict: Configuration dictionary
        """
        # Default configuration
        default_config = {
            'default_algorithm': DEFAULT_ALGORITHM,
            'default_baseline_file': DEFAULT_BASELINE_FILE,
            'default_ignore_file': DEFAULT_IGNORE_FILE,
            'chunk_size': CHUNK_SIZE,
            'logging': {
                'enabled': True,
                'log_file': LOG_FILE,
                'log_level': 'INFO',
                'console_output': True
            },
            'display': {
                'separator_length': SEPARATOR_LENGTH,
                'hash_display_length': HASH_DISPLAY_LENGTH,
                'verbose': True
            },
            'ignore_patterns': {
                'use_default_patterns': True,
                'custom_patterns': []
            }
        }
        
        # Try to load from file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                
                # Merge with defaults (file config overrides defaults)
                config = {**default_config, **file_config}
                logger.info(f"Configuration loaded from: {self.config_file}")
                return config
                
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid config file format: {e}. Using defaults.")
                return default_config
            except Exception as e:
                logger.warning(f"Could not load config file: {e}. Using defaults.")
                return default_config
        else:
            logger.info("No config file found. Using default configuration.")
            return default_config
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key (supports dot notation for nested keys)
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self):
        """
        Get all configuration.
        
        Returns:
            dict: Complete configuration dictionary
        """
        return self.config.copy()


# Global config instance
_config_loader = None


def get_config():
    """
    Get global configuration loader instance.
    
    Returns:
        ConfigLoader: Configuration loader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader


def reload_config(config_file='config.json'):
    """
    Reload configuration from file.
    
    Args:
        config_file (str): Path to configuration file
    """
    global _config_loader
    _config_loader = ConfigLoader(config_file)
    logger.info("Configuration reloaded")