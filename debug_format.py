import pathlib
import re

root = pathlib.Path('.')
for path in root.rglob('*.py'):
    if '.venv' in str(path):
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '%(' in text or '.format(' in text or 'format(' in text or '%s' in text or '%' in text:
        for i, line in enumerate(text.splitlines(), 1):
            if '%(' in line or '.format(' in line or 'format(' in line or '%s' in line or '%' in line:
                print(f'{path}:{i}:{line.strip()}')
