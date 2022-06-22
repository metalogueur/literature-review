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

This will install all required dependencies, including these three:

- [habanero](https://habanero.readthedocs.io/) to make requests to the Crossref API;
- [pandas](https://pandas.pydata.org/) to convert the API responses into a DataFrame;
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) to save the resulting DataFrame into an ```.xlsx``` file.

## Usage

### journals.py script

To use the script as is, simply open a command line terminal from your
working directory and type this command:

```python journals.py```

Verbosity has been added to the script, so you'll see it working from
start to finish.

#### Customizing the script

*For complete reference, please refer to Crossref API's
[journals/{issn}/works/ endpoint](https://api.crossref.org/swagger-ui/index.html#/Journals/get_journals__issn__works)
and habanero's [Crossref journals method](https://github.com/sckott/habanero/blob/main/habanero/crossref/crossref.py#L759)
documentation.*

Here is what you can quickly customize in the script, so it suits your needs.

**Constants (lines 14-41)**

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

The ```METADATA``` constant contains the list of everything you need to retrieve
as publication data. The complete list of available metadata can be found in the
*Elements* section of the ```journals/{issn}/works``` endpoint's documentation.
Please make sure that all ```METADATA``` items have a corresponding key in the
```convert_to_dataframe``` function's ```data``` dictionary. Otherwise, the
data won't be saved in Excel.

**Functions (lines 44-153)**

The ```main``` function contains the script's algorithm. It is contained in a
```try... except``` block in order to gracefully terminate if something goes
wrong.

The ```convert_to_dataframe``` function takes the bare-bones dataset retrieved
from the Crossref API and converts that data into a Pandas DataFrame. As mentioned
in the *Constants* section, the ```data``` dictionary's keys must match the
```METADATA``` constant list items.

In the ```for item in dataset``` loop, only metadata returned in the form of
strings or lists are taken care of, along with the ```author``` metadata. If you
need to retrieved data that is from other classes, you'll have to edit that
loop accordingly.

Have fun! More examples will be published during summer and fall 2022.