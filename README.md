# ConfigBackup

A simple command-line tool for backing up and restoring personal configuration files.

## Features

- 🔧 Backup configuration files with timestamp-based organization
- 📋 Configurable file lists via JSON config
- 📁 Support for both files and directories
- 🔄 Easy restoration from any backup session
- 📊 Backup size tracking and detailed listing
- ⚙️ Customizable backup directory

## Usage

### Backup your configuration files
```bash
python3 config_backup.py backup
```

### List available backups
```bash
python3 config_backup.py list
```

### Restore from latest backup
```bash
python3 config_backup.py restore
```

### Show help
```bash
python3 config_backup.py help
```

## Configuration

Customize your backup settings by editing `config.json`:

```json
{
  "backup_dir": "~/.config_backup",
  "config_files": [
    "~/.bashrc",
    "~/.zshrc",
    "~/.vimrc",
    "~/.gitconfig",
    "~/.ssh/config",
    "~/.tmux.conf"
  ],
  "ignore_missing": true
}
```

## Supported Config Files

Currently supports backing up:
- `.bashrc`
- `.zshrc`
- `.vimrc` 
- `.gitconfig`
- `.ssh/config`

## Future Enhancements

- [ ] Custom config file lists
- [ ] Interactive restore selection
- [ ] Cloud sync support