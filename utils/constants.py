""" constants.py

This module constains all constants used throughout the project.
"""
# Imports
from pathlib import Path

# Project's base directory
BASE_DIR = Path(__file__).resolve().parent.parent
# Be polite with the Crossref API. Enter your email address and the API
# will route your requests to a Polite Pool.
MAILTO = ''
# Comment out metadata fields you don't need below or add other fields.
# This metadata is found in Crossref works.
METADATA = [
    'DOI',
    'author',
    'title',
    'container-title',
    'ISSN',
    'subject',
    'abstract'
]
UA_STRING = 'literature-review/0.2'