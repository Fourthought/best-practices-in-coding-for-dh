# usr/bin/env python
# coding: utf-8

"""
Named Entity Recognition for Henslow Correspondence Project

This script allows the user to generate named entity tags for any Henslow Correspondence Project XML letter
"""

from timeit import default_timer as timer
from datetime import timedelta

from pathlib import Path
from bs4 import BeautifulSoup
import json

import spacy
from spacy import displacy
import en_core_web_sm

nlp = en_core_web_sm.load()


def extract_text():
    """
    Extracts a text from a file

    Parameters
    ----------

    Returns
    -------
    list
        a text object with '&' replaced by 'and'

    """

    with open("../data/henslow/letters_152.xml", encoding="utf-8") as file:
        letter = BeautifulSoup(file, "lxml-xml")

    transcription = letter.find(type="transcription").text

    return transcription.replace("& ", "and ")


def ner(text):
    """
    Creates a spacy doc object from plain text

    Parameters
    ----------
    text : str
        The raw text for processing
    
    Returns
    -------
    document
        a spaCy doc object including named entities
    """

    document = nlp(text)

    for entity in document.ents:
        print(f"{entity.text}: {entity.label_}")

    return document


def write_json(document):
    """
    dumps json object of the named entities

    Parameters
    ----------
    document
        spaCy doc object

    Returns
    -------
        json object of named entities
    """

    doc_dict = document.to_json()

    ents_dict = {key: value for (key, value) in doc_dict.items() if key == "ents"}

    json.dumps(ents_dict)


def write_html_viz(document):
    """
    Writes a named entity visualisation of the doc object

    Parameters
    ----------
    document
        spaCy doc object

    Returns
    -------
    output_file
        a html visualisation ofVirtualenv named entities in a document
    """

    output_file = Path("../results/ent_viz.html")

    document.user_data["title"] = "Letter from William Christy, Jr., to John Henslow, 26 February 1831"

    html = displacy.render(document, style="ent", jupyter=False, page=True)

    output_file.open("w", encoding="utf-8").write(html)

def main():
    print("Extracting Text")
    text = extract_text()

    print("Parsing Text")
    document = ner(text)

    print("Writing json")
    write_json(document)

    print("creating viz")
    write_html_viz(document)


if __name__ == "__main__":
    main()
