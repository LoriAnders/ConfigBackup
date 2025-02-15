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
    
    def backup_configs(self):
        """Backup all found configuration files"""
        configs = self.get_common_configs()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_session_dir = self.backup_dir / f"backup_{timestamp}"
        backup_session_dir.mkdir(exist_ok=True)
        
        backed_up = []
        for config_file in configs:
            try:
                # Create relative path structure in backup
                rel_path = config_file.relative_to(Path.home())
                backup_path = backup_session_dir / rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                if config_file.is_file():
                    shutil.copy2(config_file, backup_path)
                elif config_file.is_dir():
                    shutil.copytree(config_file, backup_path, dirs_exist_ok=True)
                
                backed_up.append(str(config_file))
                print(f"Backed up: {config_file}")
            except Exception as e:
                print(f"Failed to backup {config_file}: {e}")
        
        # Save backup metadata
        metadata = {
            "timestamp": timestamp,
            "backed_up_files": backed_up,
            "backup_dir": str(backup_session_dir)
        }
        
        with open(backup_session_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        return backup_session_dir

if __name__ == "__main__":
    backup = ConfigBackup()
    configs = backup.get_common_configs()
    print(f"Found {len(configs)} configuration files")
    
    if configs:
        print("\nStarting backup...")
        backup_dir = backup.backup_configs()
        print(f"\nBackup completed! Files saved to: {backup_dir}")
    else:
        print("No configuration files found to backup.")