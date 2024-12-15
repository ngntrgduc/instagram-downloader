from pathlib import Path

def bulk_rename(folder_name: str = 'Downloaded'):
    """Renaming all downloaded images using increasing numerical order"""
    folder = Path(folder_name)
    if not folder.is_dir():
        raise ValueError(f'The folder {folder_name} does not exist or is not a directory.')

    files = [f for f in folder.iterdir() if f.is_file()]
    if not files:
        print(f'No files found in {folder_name}.')
        return

    # Sort files for consistent renaming
    files.sort(key=lambda f: int(f.stem))

    # Rename files
    for i, file in enumerate(files, start=1):
        new_name = f'{i}{file.suffix}'
        if new_name == file.name:
            continue

        new_path = folder / new_name
        try:
            file.rename(new_path)
            print(f'Renamed: {file.name} -> {new_name}')
        except Exception as e:
            print(f'Failed to rename {file.name}: {e}')

if __name__ == '__main__':
    bulk_rename('Downloaded')
