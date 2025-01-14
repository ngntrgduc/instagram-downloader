from pathlib import Path

def clear_file(file_name: str) -> None:
    open(file_name, 'w').close()
    print(f'File {file_name} was cleared.')

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
    length = len(files)

    # Grouped logging
    renamed_groups = []
    current_group = {'old': [], 'new': []}

    # Rename files
    for i, file in enumerate(files, start=1):
        new_name = f'{i}{file.suffix}'
        if new_name == file.name:
            continue

        new_path = folder / new_name
        try:
            file.rename(new_path)
            # print(f'Renamed: {file.name} -> {new_name}')
            current_group['old'].append(int(file.stem))
            current_group['new'].append(i)
        except Exception as e:
            print(f'Failed to rename {file.name}: {e}')
    
        # Log the current group if a gap in consecutive renaming is detected
        if i < length:
            current_file_name = int(files[i].stem)
            last_file_name = int(files[i - 1].stem)
            if current_file_name != last_file_name + 1:
                renamed_groups.append(current_group)
                current_group = {'old': [], 'new': []}

    # Add the last group if not empty
    if current_group['old']:
        renamed_groups.append(current_group)

    # Print grouped rename logs
    for group in renamed_groups:
        olds, news = group['old'], group['new']
        old_range = f'({min(olds)}-{max(olds)})' if len(olds) > 1 else f'{olds[0]}'
        new_range = f'({min(news)}-{max(news)})' if len(news) > 1 else f'{news[0]}'
        print(f'Renamed: {old_range}.jpg -> {new_range}.jpg')

if __name__ == '__main__':
    bulk_rename('Downloaded')
