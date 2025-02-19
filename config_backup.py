#!/usr/bin/env python3
"""
ConfigBackup - A simple tool to backup and restore configuration files
"""

import os
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime

class ConfigBackup:
    def __init__(self, config_file="config.json", backup_dir="~/.config_backup"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.backup_dir = Path(self.config.get('backup_dir', backup_dir)).expanduser()
        self.backup_dir.mkdir(exist_ok=True)
    
    def _load_config(self):
        """Load configuration from JSON file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in config file: {e}")
                return {}
        return {}
        
    def get_common_configs(self):
        """Get list of configuration files from config or defaults"""
        config_files = self.config.get('config_files', [
            "~/.bashrc",
            "~/.zshrc", 
            "~/.vimrc",
            "~/.gitconfig",
            "~/.ssh/config"
        ])
        
        configs = []
        for config_path in config_files:
            path = Path(config_path).expanduser()
            if path.exists():
                configs.append(path)
            elif not self.config.get('ignore_missing', True):
                print(f"Warning: {config_path} not found")
        
        return configs
    
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
    
    def list_backups(self):
        """List all available backup sessions"""
        backup_dirs = []
        for item in self.backup_dir.iterdir():
            if item.is_dir() and item.name.startswith("backup_"):
                metadata_file = item / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    backup_dirs.append((item, metadata))
        
        backup_dirs.sort(key=lambda x: x[1]['timestamp'], reverse=True)
        return backup_dirs
    
    def restore_configs(self, backup_session_path):
        """Restore configuration files from a backup session"""
        backup_path = Path(backup_session_path)
        metadata_file = backup_path / "metadata.json"
        
        if not metadata_file.exists():
            raise ValueError("Invalid backup session - no metadata found")
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        home = Path.home()
        restored = []
        
        for backed_up_file in metadata['backed_up_files']:
            try:
                original_path = Path(backed_up_file)
                rel_path = original_path.relative_to(home)
                backup_file = backup_path / rel_path
                
                if backup_file.exists():
                    if backup_file.is_file():
                        shutil.copy2(backup_file, original_path)
                    elif backup_file.is_dir():
                        if original_path.exists():
                            shutil.rmtree(original_path)
                        shutil.copytree(backup_file, original_path)
                    
                    restored.append(str(original_path))
                    print(f"Restored: {original_path}")
                else:
                    print(f"Warning: {backup_file} not found in backup")
                    
            except Exception as e:
                print(f"Failed to restore {backed_up_file}: {e}")
        
        return restored

def main():
    if len(sys.argv) < 2:
        print("ConfigBackup - Configuration File Management Tool")
        print("\nUsage:")
        print("  python config_backup.py backup    - Backup configuration files")
        print("  python config_backup.py list      - List available backups")
        print("  python config_backup.py restore   - Restore from latest backup")
        return
    
    backup_tool = ConfigBackup()
    command = sys.argv[1].lower()
    
    if command == "backup":
        configs = backup_tool.get_common_configs()
        print(f"Found {len(configs)} configuration files")
        
        if configs:
            print("\nStarting backup...")
            backup_dir = backup_tool.backup_configs()
            print(f"\nBackup completed! Files saved to: {backup_dir}")
        else:
            print("No configuration files found to backup.")
            
    elif command == "list":
        backups = backup_tool.list_backups()
        if backups:
            print("Available backups:")
            for i, (backup_dir, metadata) in enumerate(backups):
                print(f"  {i+1}. {metadata['timestamp']} - {len(metadata['backed_up_files'])} files")
        else:
            print("No backups found.")
            
    elif command == "restore":
        backups = backup_tool.list_backups()
        if backups:
            latest_backup_dir, metadata = backups[0]
            print(f"Restoring from backup: {metadata['timestamp']}")
            restored = backup_tool.restore_configs(latest_backup_dir)
            print(f"\nRestore completed! {len(restored)} files restored.")
        else:
            print("No backups found to restore from.")
    else:
        print(f"Unknown command: {command}")
        print("Use 'backup', 'list', or 'restore'")

if __name__ == "__main__":
    main()