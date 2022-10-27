# Systematic Literature Review in Crossref using Python

This is a series of examples that let you build systematic literature
reviews using the [Crossref API](https://api.crossref.org/) and Python.

Please star and/or watch this repository in order to be informed when new examples 
are published.

## Installation

Python 3.8 and over is required in order to use the examples.
Once Python is installed, all you have to do is download or clone this repository
in your working directory and, in a command line terminal, type this command:

```pip install -r requirements.txt```

This will install all required dependencies, including these four:

- [habanero](https://habanero.readthedocs.io/) to make requests to the Crossref API;
- [pandas](https://pandas.pydata.org/) to convert the API responses into a DataFrame;
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) to save the resulting DataFrame into an ```.xlsx``` file.

## Usage

### journals.py script

This script is used to build a systematic literature review of articles
from specific journals, using their ISSN, and save the results in an
Excel file.

### doi_from_titles.py script

This script is used to retrieve journal article DOIs using their title
only and save the results in an Excel file.

Perfect matches will return a DOI. Partial matches on the beginning of the
title with still return a DOI, but with a `[MATCH PARTIEL]` prefix.

## Customizing the scripts

*For complete reference, please refer to Crossref API's
[journals/{issn}/works/ endpoint](https://api.crossref.org/swagger-ui/index.html#/Journals/get_journals__issn__works)
and habanero's [Crossref journals method](https://github.com/sckott/habanero/blob/main/habanero/crossref/crossref.py#L759)
documentation.*

Here is what you can quickly customize in the scripts, so they suit your needs.

### Constants

The ```BASE_DIR``` and ```EXCEL_FILE``` constants are used to save the
resulting dataframe in an Excel file. Default is in the same directory as
the script.

The ```FILTERS``` constant lets you add/modify/delete filters for your query.

In the ```ISSN_LIST``` constant, you can add the ISSN of all the journals you
need to retrieve publications from. There is no limit on the number of ISSNs
you can put (well maybe there is, but you'll be warned by the API, not by the
script). 

The Crossref API asks that you play nice with its service (please refer to the
documentation's [Etiquette Section](https://api.crossref.org/swagger-ui/index.html#/)).
In order to do so, you'll have to add your email address to the ```MAILTO```
constant. By playing nice, you'll be rewarded with a more reliable service and
directed to the *Polite Pool* of users.

Have fun! More examples will be published as people ask for them.