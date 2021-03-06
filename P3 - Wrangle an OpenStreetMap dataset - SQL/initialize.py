#importing required modules - XML, CSV, SQLite and plotting
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import sqlite3
import string as s
import pandas as pd
import matplotlib.pyplot as plt
import plotly as pltly
from plotly.graph_objs import *

OSM_FILE='NYC.OSM'
DATABASE='OpenStreetMap.db'
mapbox_access_token='pk.eyJ1IjoibWVldG5hcmVuIiwiYSI6ImNqM3htbWtrMjAwMXUyd3BteXlpb2lmOXkifQ.tOV33V0Iv2N_Lqw--qqUwg'

pltly.tools.set_credentials_file(username='meetnaren', api_key='02FpawrSfFQjW88Ry5UA')

# Helper functions for connecting to database, fetching elements from XML file
def connect_db(db=DATABASE):
    """This function connects to the database and returns the cursor.

    Args:
        db (str): The name of the database file. Defaults to DATABASE

    Returns:
        c (cursor): The cursor of the connection established with the database
    """
    conn=sqlite3.connect(db)
    c=conn.cursor()
    return c

def execute_query(cursor, query):
    """This function executes the query and returns the results.

    Args:
        cursor (cursor) : The cursor of the connection established with the database
        query (str)     : The query that needs to be executed against the database

    Returns:
        A Pandas DataFrame with the results of the query passed
    """
    return pd.DataFrame(cursor.execute(query).fetchall())

def get_element(osm_file, tags=('node', 'way')):
    """Yield element if it is the right type of tag

    Args:
        osm_file (str): the name of the XML file
        tags (tuple)  : all the types of elements that need to be included in the database

    Yields:
        XML Element: the next element in the XML file
    """

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# This code is from the case study
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
