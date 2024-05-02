# ScholarPDF-Renamer
ScholarPDF-Renamer is a tool designed to automate the extraction of bibliographic information from academic PDF files and rename them according to a standardized format: `year_surname of the last author_journal_title`. 

## How does it work?
The scirpt extracts the DOI or arXiv IDs from the pdf file and retrieves the necessary data from online bibliographic databases.

## How to Get Started?
### Prerequisites
- Python 3.11.7 or higher, preferably installed via Anaconda.
- Internet connection to access online databases.

### Installation
Install the required packages using pip:
```bash
pip install pdfminer.six
pip install PyPDF2
pip install requests
