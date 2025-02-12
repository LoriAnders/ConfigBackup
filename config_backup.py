#!/usr/bin/env python3
"""
ConfigBackup - A simple tool to backup and restore configuration files
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class ConfigBackup:
    def __init__(self, backup_dir="~/.config_backup"):
        self.backup_dir = Path(backup_dir).expanduser()
        self.backup_dir.mkdir(exist_ok=True)
        
    def get_common_configs(self):
        """Get list of common configuration files"""
        home = Path.home()
        common_configs = [
            home / ".bashrc",
            home / ".zshrc", 
            home / ".vimrc",
            home / ".gitconfig",
            home / ".ssh" / "config"
        ]
        return [config for config in common_configs if config.exists()]

if __name__ == "__main__":
    backup = ConfigBackup()
    configs = backup.get_common_configs()
    print(f"Found {len(configs)} configuration files")