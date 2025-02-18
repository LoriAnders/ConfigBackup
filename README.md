# ConfigBackup

A simple command-line tool for backing up and restoring personal configuration files.

## Features

- Backup configuration files to a designated directory
- Support for common config files (.vimrc, .bashrc, .gitconfig, etc.)
- Easy restoration of configs on new systems

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