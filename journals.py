"""
journals.py

An example of building a systematic literature review using the Crossref API's
journals/{issn}/works endpoint.
"""

# Imports
from habanero import Crossref
from utils.constants import *
from utils.functions import convert_to_dataframe


# Constants
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


def main():
    """
    This is the script's main function, where all the work is done.
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
