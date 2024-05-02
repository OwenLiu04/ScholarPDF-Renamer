# -*- coding: utf-8 -*-
"""
Author: OwenLiu04
Version: 1.0
License: GNU General Public License v3 (GPLv3)
Email: 69543538@qq.com

Script Functionality:
    This script automates the extraction of bibliographic information from PDF files. 
    It then renames the PDF files according to a standardized format: year_surname of the last author_journal_title. 
    This process involves extracting either a DOI or an arXiv ID directly from the PDF and subsequently retrieving the bibliographic details from online databases.
Requirements:
    Internet Connection: 
        Required for accessing online bibliographic databases.
    Python Environment:
        Python Version: 3.11.7 (packaged by Anaconda, Inc.)
        Installed Packages:
            pdfminer.six Version 20231228
            PyPDF2 Version 3.0.1
            requests Version 2.31.0
        Installation of Dependencies:
            The above Python packages can be installed using the following commands:
            pip install pdfminer.six
            pip install PyPDF2
            pip install requests
Known Issues:
    PDF Compatibility: 
        The script is unable to process PDF files that lack a DOI or an arXiv ID. 
        Additionally, it may occasionally fail to recognize the arXiv ID in some documents.
    Performance Note: 
        The script requires access to an online database, which can cause delays that may seem as if the application has become unresponsive. 
        Please be patient during these periods, as the script is actively downloading the necessary information from the database.
"""

import os
import re
import tkinter as tk
from tkinter import filedialog
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
import requests
import shutil
from urllib.request import urlopen
from xml.dom import minidom

def select_pdf_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )
    root.destroy()
    return file_paths

def extract_doi(text):
    match = re.search(r'\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
    if match:
        return match.group(0)
    return None

def fetch_publication_details(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['message']
        last_author = data['author'][-1]['family'] if data['author'] else 'Surname Not Found'
        publication_year = data.get('published-print', data.get('published-online', {'date-parts': [[0]]})).get('date-parts', [[0]])[0][0]
        title = data.get('title', ['Title Not Found'])[0]
        journal_abbreviation = data.get('short-container-title', ['Journal Name Not Found'])[0] if data.get('short-container-title') else data.get('container-title', ['Journal Name Not Found'])[0]
        return {'year': publication_year, 'last_author': last_author, 'title': title, 'journal_abbreviation': journal_abbreviation}
    else:
        return None

def extract_arxiv_id(pdf_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        # Create a PDF reader object
        reader = PdfReader(file)
        
        # Extract text from the first page
        first_page_text = reader.pages[0].extract_text()
        
        # Define regular expression pattern to find the arXiv string
        pattern = r'arXiv:(\d+\.\d+v\d+)\s+\[\S+\]\s+\d+\s\w+\s(\d+)'
        
        # Search for the pattern in the text
        match = re.search(pattern, first_page_text)
        
        if match:
            arxiv_id = match.group(1)
            return arxiv_id
        else:
            return None

def extract_bib_information(arxiv_id):
    usock = urlopen(f'http://export.arxiv.org/api/query?id_list={arxiv_id}')
    xmldoc = minidom.parse(usock)
    usock.close()
    entry = xmldoc.getElementsByTagName("entry")[0]
    year = entry.getElementsByTagName("updated")[0].firstChild.data[:4]
    title = entry.getElementsByTagName("title")[0].firstChild.data
    authors = [node.getElementsByTagName("name")[0].firstChild.data.split()[-1] for node in entry.getElementsByTagName("author")]
    last_author = authors[-1] if authors else "Surname Not Found"
    return {'year': year, 'last_author': last_author, 'title': title}

def sanitize_filename(title):
    # Remove invalid file name characters and other potential problematic characters
    invalid_chars = '<>:"/\\|?*\n\r\t'
    for char in invalid_chars:
        title = title.replace(char, '')
    # Replace any sequences of spaces with a single space
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def rename_pdf(original_path, details):
    sanitized_title = sanitize_filename(details['title'])
    new_filename = f"{details['year']}_{details['last_author']}_{details.get('journal_abbreviation', 'arXiv')}_{sanitized_title}.pdf"
    new_path = os.path.join(os.path.dirname(original_path), new_filename)
    try:
        shutil.move(original_path, new_path)
        print(f"Renamed {os.path.basename(original_path)} to {os.path.basename(new_path)}")
    except OSError as e:
        print(f"Failed to rename {original_path} due to OS error: {e}")

def process_pdfs():
    pdf_files = select_pdf_files()
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            text = extract_text(file)
        doi = extract_doi(text)
        if doi:
            details = fetch_publication_details(doi)
            if details:
                rename_pdf(pdf_file, details)
                continue
        arxiv_id = extract_arxiv_id(pdf_file)
        if arxiv_id:
            details = extract_bib_information(arxiv_id)
            rename_pdf(pdf_file, details)
            continue
        print(f"No DOI or arXiv ID found in {os.path.basename(pdf_file)}. File not renamed.")

if __name__ == "__main__":
    process_pdfs()