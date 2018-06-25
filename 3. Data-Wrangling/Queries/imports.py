from pymongo import MongoClient
from pymongo import cursor
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import os
import datetime
import pprint
import csv
import json
import io
import re
import codecs
import pymongo

client = MongoClient('localhost:27017')
db = client.osmstreetmap