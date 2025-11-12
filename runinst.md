To run the script later (plan only, since read-only mode):

1. Navigate to the project directory: cd /home/alexinorulz/projects/notionapi/bookquotesdb
2. Activate the virtual environment: . venv/bin/activate
3. Run the script: python bookquotesdb.py

Ensure the .env file has valid credentials and the quotes.md file exists. The script will append new quotes to existing Notion pages based on
fuzzy matching. In plan mode, I cannot execute—run these commands manually when ready.

To deactivate the venv:

Run deactivate in the terminal where the venv is activated. This returns to the system Python environment. The virtual environment is located at /home/alexinorulz/projects/notionapi/bookquotesdb/venv.
