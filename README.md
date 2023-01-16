# Auto-install
Auto-install is a command-line program that downloads and installs latest versions of specified programs, such as Firefox, 7-zip, and VSCode (including its extensions), for Windows Systems automatically.

# Important Note
This program is only compatible with Windows right now.

# Getting Started

To run the script, you will need the following:
- Python 3.6 or later
- [Rich](https://pypi.org/project/rich) library
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) library

You can install them using pip by running the following command:
```
pip install -U rich bs4
```

# Usage
To use Auto-install, you will need to have Python 3.x installed on your system. You can download the latest version of Python from the official website or Microsoft Store.

Once you have Python installed, you can clone this repository (or download as zip) and run the program using the command line.
```
git clone https://github.com/dkvc/auto-install.git
cd auto-install
python -m auto_install
```

# Working
The program uses a SQLite database `programs.db` to store the information of the programs and extensions that need to be installed.
The programs table has the following columns:
- **name**: name of the program
- **url**: download link of the program
- **filename**: file name of the program after downloading
- **args**: command line arguments for silent installation

The extensions table has the following columns:
- **name**: name of the extension
- **id**: identifier of the extension in the VSCode Marketplace

On running the program, it will check the prerequisites and install them if they are not already installed. 
Then it will check the `programs.db` and install the program or extension specified in the database.

The `Database.py` checks if [programs mentioned in this repository](./PROGRAMS.md) are already added in the database. In case if they don't exist, the script adds it to database.

# License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

[![License](https://img.shields.io/github/license/dkvc/auto-install?color=%236cc644&style=for-the-badge)](./LICENSE)

# Built With
- [rich](https://github.com/Textualize/rich) - For console styling and progress bar
- [BeautifulSoup4](https://github.com/wention/BeautifulSoup4) - For web scraping
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) - For database

# Planned Updates
- [ ] Add PowerShell Automation for Windows (more efficient)
- [ ] winget Support
- [ ] GUI Support for Selection of Programs
- [ ] Easier Addition of Programs instead of using entire database
- [ ] Support for Linux and macOS

**Note:** The above order of planned updates doesn't represent its priority.
