"""
journals.py

An example of building a systematic literature review using the Crossref API's
journals/{issn}/works endpoint.
"""

# Imports
from pathlib import Path
from habanero import Crossref
import numpy as np
from pandas import DataFrame

# Constants
BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / 'literature_review.xlsx'
FILTERS = {
    'from-pub-date': '2007-01-01'
}
# The ISSN of all journals you need to fetch publications from
ISSN_LIST = [
    '0007-1080',
    '0019-7939',
    '0034-379X',
    '0268-1072',
    '2053-9517',
    '1477-7487'
]
# Be polite with the Crossref API. Enter your email address and the API
# will route your requests to a Polite Pool.
MAILTO = ''
# Comment out metadata fields you don't need below or add other fields.
METADATA = [
    'DOI',
    'author',
    'title',
    'container-title',
    'ISSN',
    'subject',
    'abstract'
]


# Functions
def convert_to_dataframe(dataset: list) -> DataFrame:
    """
    This function takes a list of publications (works) retrieved from the
    Crossref API and converts that list into a Pandas DataFrame.

    :param dataset:     The list of publications retrieved from Crossref.
    :type dataset:      list
    :return:            The Pandas DataFrame list conversion.
    """
    if not isinstance(dataset, list):
        msg = f"list object expected. Received {type(dataset)} instead"
        raise TypeError(msg)

    # Make sure that the keys in the data dictionary match the metadata fields
    # of the METADATA constant.
    data = {
        'DOI': [],
        'author': [],
        'title': [],
        'container-title': [],
        'ISSN': [],
        'subject': [],
        'abstract': []
    }

    for item in dataset:
        keys = item.keys()
        for key in item.keys():
            if isinstance(item[key], str):
                data[key].append(item[key])
            if isinstance(item[key], list) and key != 'author':
                data[key].append(','.join(item[key]))
            if key == 'author':
                authors = format_authors(item['author'])
                data[key].append(authors)

        na_metadata = [md for md in METADATA if md not in keys]
        for key in na_metadata:
            data[key].append(np.nan)

    return DataFrame(data)


def format_authors(author_list: list) -> str:
    """
    This function takes a list of authors retrieved from a publication (work)
    item and formats the list in a bibliographic reference style string.

    :param author_list:     The list of authors retrieved from the work item.
    :type author_list:      list
    :return:                The authors list formatted as a string.
    """
    if not isinstance(author_list, list):
        msg = f"list object expected. {type(author_list)} received instead."
        raise TypeError(msg)

    authors = []
    for author in author_list:
        author_data = author.keys()
        name_parts = []
        if 'family' in author_data:
            name_parts.append(author['family'].upper())
        if 'given' in author_data:
            name_parts.append(author['given'])
        authors.append(', '.join(name_parts))

    return ', '.join(authors)


def main():
    """
    This is the script's main function, where all the work is done.
    :return:
    """
    print('Hello World! Starting script...')

    try:
        print('Connecting to Crossref...')
        cr = Crossref(mailto=MAILTO, ua_string='literature-review/0.1')
        dataset = []

        for issn in ISSN_LIST:
            print(f"Fetching publications for journal ISSN {issn}...")
            response = cr.journals(ids=issn,
                                   works=True,
                                   filter=FILTERS,
                                   select=METADATA,
                                   cursor='*',
                                   progress_bar=True,
                                   warn=True)

            batches = [
                batch['message']['items']
                for batch in response if batch['status'] == 'ok'
            ]
            items = [item for batch in batches for item in batch]
            print(f"{len(items)} publications retrieved...")
            dataset += items

        print('Converting data to dataframe...')
        dataframe = convert_to_dataframe(dataset)

        print('Saving dataframe to Excel...')
        dataframe.to_excel(EXCEL_FILE, index=False)

    except Exception as e:
        print(f"Could not complete literature review because of {e}")
    finally:
        print('End of script.')


if __name__ == '__main__':
    import sys

    if sys.version_info.major < 3 or \
        (sys.version_info.major == 3 and sys.version_info.minor < 8):
        msg = f"Python 3.8 and over is required to run this script. " + \
            f"Current installation: {sys.version}"
        raise Exception(msg)

    main()

