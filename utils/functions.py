""" functions.py

This module contains all utility functions used througout the project.
"""
# Imports
import numpy as np
from pandas import DataFrame
import re
from .constants import METADATA


# Functions
def convert_to_dataframe(dataset: list) -> DataFrame:
    """
    This function takes a list of publications (works) retrieved from the
    Crossref API and converts that list into a Pandas DataFrame.

    :param dataset:     The list of publications retrieved from Crossref.
    :type dataset:      list
    :return:            The Pandas DataFrame list conversion.
    :TODO:              Replace this function with the new one once code is updated.
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


def convert_to_dataframe_new(dataset: list) -> DataFrame:
    """
    This WIP function will replace the original convert_to_dataframe() function.
    It takes a list of publications (works) retrieved from the
    Crossref API and converts that list into a Pandas DataFrame.

    :param dataset:     The list of publications retrieved from Crossref.
    :type dataset:      list
    :return:            The Pandas DataFrame list conversion.
    """

    if not isinstance(dataset, list):
        msg = f"list object expected. Received {type(dataset)} instead"
        raise TypeError(msg)

    data = {}

    for item in dataset:
        for key in item.keys():
            if key not in data.keys():
                data[key] = []
            if isinstance(item[key], str):
                data[key].append(item[key])
            if isinstance(item[key], list) and key != 'author':
                data[key].append(','.join(item[key]))
            if key == 'author':
                authors = format_authors(item['author'])
                data[key].append(authors)

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


def strip_non_word_chars(original_str: str) -> str:
    """
    This function takes a sentence-like string with punctuation and all and
    returns, strips that string from everything but words and returns the result.

    :param original_str:    The sentence-like string.
    :return:                The string striped of all non-word characters
    """
    if not isinstance(original_str, str):
        msg = f"String object expected. {type(original_str)} received instead."
        raise TypeError(msg)

    striped_string = re.split(r'\W+', original_str)
    return ' '.join(striped_string)
