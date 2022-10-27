""" doi_from_titles.py

An example of fetching DOIs with only article titles. It takes an Excel sheet
as input containing two columns : Title and DOI.
"""
# Imports
from habanero import Crossref
import pandas as pd
from utils.constants import *
from utils.functions import *


# Functions
def main():
    """
    The script's main function.

    What this function needs to do :
    1) Open Excel file into DataFrame
    2) Filter out titles that already have DOIs
    3) For each title in table
        a) Split title string in a word list
        b) Build Crossref request using title
        c) Send request to Crossref API
        d) For each item retrieved in the response
            i) Search for the item with the matching title
            ii) Save its DOI in DataFrame
    4) Save resulting DataFrame in Excel
    """
    excel_file = BASE_DIR / 'Articles-DOI.xlsx'
    df = pd.read_excel(excel_file)
    df_without_doi = df[df['DOI'].isna()].copy()
    facets = 'type-name:journal-article'

    cr = Crossref(mailto=MAILTO, ua_string=UA_STRING)
    for row in df_without_doi.iterrows():
        index, data = row
        title = strip_non_word_chars(data['Title'])
        print(f"{index} : {title}")

        response = cr.works(query=title, facet=facets)
        if response['status'] == 'ok':
            references = [reference for reference in response['message']['items']]

            for reference in references:
                if 'title' in reference.keys():
                    ref_title = strip_non_word_chars(reference['title'][0]).lower()
                    lowered_title = title.lower()
                    if ref_title == lowered_title:
                        df.at[index, 'DOI'] = reference['DOI']
                        print(f"{index} : {reference['DOI']}")
                        break
                    if lowered_title.startswith(ref_title):
                        df.at[index, 'DOI'] = f"[MATCH PARTIEL] {reference['DOI']}"
                        print(f"{index} : [MATCH PARTIEL] {reference['DOI']}")
                        break

    df.to_excel(excel_file, sheet_name='results', index=False)


if __name__ == '__main__':
    main()
