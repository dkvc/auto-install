import re
import sqlite3
import urllib.request

from bs4 import BeautifulSoup

def create_database():
    with sqlite3.connect("programs.db") as conn:
        cursor = conn.cursor()

        # Create a table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS programs 
        (name text PRIMARY KEY, 
        url text UNIQUE, 
        filename text, 
        args text)
        """)

        # Firefox
        firefox_url = "https://download.mozilla.org/?product=firefox-latest&os=win&lang=en-US"
        cursor.execute("""
        INSERT OR IGNORE INTO programs
        VALUES ('Firefox', ?, 'Firefox.exe', '-ms')
        """, (firefox_url,))

        # 7-zip
        zip7_url = "https://www.7-zip.org/download.html"
        page = urllib.request.urlopen(zip7_url)
        soup = BeautifulSoup(page, 'html.parser')

        match = soup.find("a", href=re.compile("a/7z.*exe"))
        if match:
            download_link = match['href']
            version = re.search("7z(\d{4}-x64)", download_link).group(1)
            zip7_url = f"https://www.7-zip.org/{download_link}"
            cursor.execute("""
            INSERT OR IGNORE INTO programs 
            VALUES ('7-zip', ?, '7zip.exe', '/S')
            """, (zip7_url,))
        else:
            raise Exception("Could not find the latest version of 7zip.")

        # VSCode
        vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
        cursor.execute("""
        INSERT OR IGNORE INTO programs 
        VALUES ('VSCode', ?, 'VSCode.exe', '/VERYSILENT /MERGETASKS=!runcode')
        """, (vscode_url,))

        # Create another table for VSCode extensions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS extensions 
        (name text, 
        id text PRIMARY KEY)
        """)

        # Insert extensions into new table
        extensions = """
            INSERT OR IGNORE INTO extensions (name, id) 
            VALUES ('Python', 'ms-python.python'),
                    ('iSort', 'ms-python.isort'),
                    ('Jupyter', 'ms-toolsai.jupyter'),
                    ('Jupyter-Keymap', 'ms-toolsai.jupyter-keymap'),
                    ('Jupyter-Notebook-Renderers', 'ms-toolsai.jupyter-renderers'),
                    ('Jupyter-Cell-Tags', 'ms-toolsai.vscode-jupyter-cell-tags'),
                    ('Jupyter-Slideshow', 'ms-toolsai.vscode-jupyter-slideshow'),
                    ('Pylance', 'ms-python.vscode-pylance'),
                    ('Material-Icon-Theme', 'PKief.material-icon-theme')
            """
        cursor.executescript(extensions)

        conn.commit()