import os
from pathlib import Path

def add_story(category, title, content):
    # Ensure category directory exists
    category_dir = Path(__file__).parent.parent / 'content' / category
    category_dir.mkdir(parents=True, exist_ok=True)
    # Generate filename from title
    filename = title.lower().replace(' ', '-').replace('.', '').replace(',', '')
    file_path = category_dir / (filename + '.md')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{content}\n")
    print(f"Story '{title}' added to category '{category}'.")

if __name__ == '__main__':
    cat = input('Category: ').strip()
    title = input('Story Title: ').strip()
    print('Enter story content (end with a blank line):')
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    content = '\n'.join(lines)
    add_story(cat, title, content)
