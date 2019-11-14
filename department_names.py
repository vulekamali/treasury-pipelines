from datapackage_pipelines.wrapper import process
from pprint import pformat
from slugify import slugify
import logging
import os
import requests
import csv

portal_url = os.environ.get('PORTAL_URL', "https://vulekamali.gov.za/")

department_names = {
    "2014-15": {"national": {}, "provincial": {},},
    "2015-16": {"national": {}, "provincial": {},},
    "2016-17": {"national": {}, "provincial": {},},
    "2017-18": {"national": {}, "provincial": {},},
    "2018-19": {"national": {}, "provincial": {},},
    "2019-20": {"national": {}, "provincial": {},},
}

warned = {}


def modify_datapackage(datapackage, parameters, stats):
    # We're not modifying the datapackage but we execute here to execute once
    # before processing rows.
    financial_years = ["2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20"]
    sphere = parameters["sphere"]
    for fin_year in financial_years:
        listing_url_path = fin_year + "/departments.csv"
        listing_url = portal_url + listing_url_path
        r = requests.get(listing_url)
        r.raise_for_status()
        reader = csv.DictReader(r.text.splitlines(), delimiter=",")
        for row in reader:
            department_names[fin_year][sphere][row["government"]] = {}
            department_names[fin_year][sphere][row["government"]][
                slugify(row["department_name"])
            ] = row["department_name"]

    logging.info(pformat(department_names))
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    financial_year = parameters.get("financial_year_column", "FinYear")
    department_column = parameters.get("department_column", "department")
    government_column = parameters.get("government_column", "government")
    department_slug = slugify(row[department_column])
    sphere = parameters['sphere']
    if sphere == 'national':
        government_name = 'South Africa'
    elif sphere == 'provincial':
        government_name = row[government_column]
    else:
        raise Exception("Unknown sphere: %r" % sphere)
    authoritative_department_name = department_names[financial_year][sphere][
        government_name
    ].get(department_slug, None)
    if authoritative_department_name:
        row[department_column] = authoritative_department_name
    else:
        warning_key = (government_name, row[department_column])
        if warning_key not in warned:
            logging.warning("No authoritative department name found for %s - %s (%s)",
                         government_name, row[department_column], department_slug)
            warned[warning_key] = True
    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
