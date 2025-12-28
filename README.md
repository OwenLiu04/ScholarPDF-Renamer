# ScholarPDF-Renamer
ScholarPDF-Renamer is a tool to automate the extraction of bibliographic information from academic PDF files and rename them according to a standardized format: `year_surname of the last author_journal_title`. 

## How does it work?
The scirpt extracts the DOI or arXiv IDs from the pdf file and retrieves the necessary data from online bibliographic databases.

## How to Get Started?
### Prerequisites
- Python 3.11.7 or higher, preferably installed via Anaconda.
- Internet connection to access online databases.

### Using the Script
To use the Python script directly, install the required packages using pip first:
```bash
pip install pypdf requests
```
Then you can run the scirpt in an Integrated Development Environment (IDE). Note: Running the `python script` outside of an IDE may result in no visible status updates or errors. For a better user experience, it is recommended to execute the script within an IDE, where you can see real-time updates. 

For `Windows users`, an executable file is provided and no installation is required. The script's status updates will be displayed in a terminal window.

## Known Issues
1. PDF Compatibility:  
   The script is unable to process PDF files that lack a DOI or an arXiv ID.   

## Contribution and Maintenance
Contributors: OwenLiu04, Hangyu Ge. 

For issues and support, please contact the maintainers via email at 69543538@qq.com or open an issue in this repository. 

If you're interested in helping us improve ScholarPDF-Renamer, please feel free to contribute!
