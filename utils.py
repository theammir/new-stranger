def get_length(file: str) -> int:
    if ('__pycache__' not in file and '.' in file):
        with open(file, 'r', encoding = 'utf-8') as f:
            return len(list(filter(lambda i: i not in ['\n', ''] and not i.startswith('#'), f.readlines())))
    else:
        return 0