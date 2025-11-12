
# Epy2Notion Quote uploader

A tool to extract quotes from epub files and upload them to Notion.

## Requirements

- Python 3.8+: For running the upload script.
- pipx: For installing Python tools like epy-reader and python-dotenv (or use pip in a virtual environment).
- [epy-reader](https://github.com/wustho/epy): Command-line tool for extracting text from epub files (install via pipx install epy-reader). -- Note: Epy is required for the [quotemaker.sh] script usage, however, you can just create a [quotes.md] file to store your quotes and follow the same formatting for the python script to work. You can alternatively create your own script to allow for other E-book readers to automatically store your quotes into the file.
- Bash shell: For executing the quote extraction script (available on Linux/WSL/macOS).
- A notion account with a single data source database containing your books, formatting is up to the user as long as the title property (Name) contains the book title. You can get free [templates](https://www.notion.com/templates/category/books) from notion and build your database from there.
- (Optional): A Virtual environment tool like venv (built-in with Python) for managing dependencies.

> ### Accounts and Access
> 
> - Notion Account: With a workspace containing a database for quotes.
> - Notion API Integration: Created at https://www.notion.com/my-integrations, with the database shared to the integration. Requires an API token.
> 
> ### Files and Configuration
> 
> - Epub Files: Source books in .epub format, placed in a directory (e.g., ~/Downloads/books).
> - Environment File (.env): Containing NOTION_TOKEN, DATABASE_ID, and FILE_PATH to the quotes markdown file.
> - Quotes Markdown File: [quotes.md] to store extracted quotes (initially empty or with existing content).
> 
> ### System Requirements
> 
> - Operating System: Linux, macOS, or WSL on Windows.
> - Permissions: Read/write access to directories for scripts, epub files, and output files.

## Setup

1. Install dependencies: pipx install epy-reader, pip install requests python-dotenv.
2. Set up Notion API: Create your integration, share your database to your integration, get a token/ID, obtain your database ID number.
3. Create .env with NOTION_TOKEN, DATABASE_ID, FILE_PATH. Note that FILE_PATH is the path to your quotes.md file.
4. Run bash script: ./quotemaker.sh <book_dir> <output_file>. Where <book_dir> is the path to your books directory and <output_file> is the path to your quotes.md file.
5. Run the Python script: python bookquotesdb.py.

## Usage

- Bash: Extracts quotes with context to a markdown file with the appropriate formatting.
- Python: Uploads to Notion using fuzzy matching for book titles, skipping duplicates and splitting long quotes to avoid API rate limit issues.


## Troubleshooting

- API errors: Check token, database ID, and permissions.
- Path issues: Ensure directories exist and are accessible.

For details, see scripts. License: MIT.

