import os
import shutil
from pathlib import Path
from datetime import datetime
import logging
import yaml
import json 

# Set up logging
logging.basicConfig(filename='logs/automation.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def backup_file(file_path: Path) -> Path:
    """Back up a file with timestamp."""
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
    try:
        shutil.copy(file_path, backup_path)
        logging.info(f"Backed up {file_path} to {backup_path}")
        return backup_path
    except Exception as e:
        logging.error(f"Failed to back up {file_path}: {e}")
        raise

def modify_config(file_path: Path, placeholder: str = "placeholder_value", new_value: str = "updated_value"):
    """Modify YAML or JSON file by replacing placeholder."""
    try:
        if file_path.suffix in ('.yaml', '.yml'):
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            # Recursive replace (simple version; expand for nested dicts if needed)
            def replace_in_dict(d):
                for k, v in d.items():
                    if isinstance(v, dict):
                        replace_in_dict(v)
                    elif v == placeholder:
                        d[k] = new_value
            replace_in_dict(data)
            with open(file_path, 'w') as f:
                yaml.safe_dump(data, f)
            logging.info(f"Modified {file_path}")
        
        elif file_path.suffix == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
            def replace_in_dict(d):
                for k, v in d.items():
                    if isinstance(v, dict):
                        replace_in_dict(v)
                    elif v == placeholder:
                        d[k] = new_value
            replace_in_dict(data)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Modified {file_path}")
        
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        logging.error(f"Parsing error in {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Failed to modify {file_path}: {e}")
        raise

def scan_and_backup(directory: str) -> list:
    """Scan directory for YAML/JSON files and back them up."""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory {directory} does not exist")
    
    files_backed_up = []
    for file_path in dir_path.glob('*.[yaml|json]*'):
        try:
            backup_path = backup_file(file_path)
            modify_config(file_path)
            files_backed_up.append(backup_path)
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
    return files_backed_up

# Test run (comment out later)
if __name__ == "__main__":
    scan_and_backup('configs')    




    