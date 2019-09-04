import csv

from datapackage_pipelines.wrapper import process
from pprint import pformat
from slugify import slugify
import logging
import os
import requests
import yaml

portal_url = os.environ.get('PORTAL_URL', "https://dynamicbudgetportal.openup.org.za/")

programme_names = {
    'national': {},
    'provincial': {},
}
warned = {}


def modify_datapackage(datapackage, parameters, stats):
    # No datapackage modification; acts as an initialization
    year_slug = parameters['financial_year']
    sphere = parameters['sphere']
    listing_url_path = year_slug + '/' + sphere + '/programmes.csv'
    listing_url = portal_url + listing_url_path
    logging.info(listing_url)
    r = requests.get(listing_url)
    r.raise_for_status()
    decoded_content = r.content.decode('utf-8')
    csv_reader = csv.reader(decoded_content.splitlines())

    first = False
    for row in csv_reader:
        if not first:  # skip headers
            first = True
            continue
        government = row[0]
        department = row[1]
        programme_name = row[2]
        programme_name_slug = slugify(programme_name)
        try:
            programme_names[sphere][government]
        except KeyError:
            programme_names[sphere][government] = {}
        try:
            programme_names[sphere][government][department]
        except KeyError:
            programme_names[sphere][government][department] = {}
        programme_names[sphere][government][department][programme_name_slug] = programme_name

    logging.info(programme_names)
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    prog_name_key = parameters.get('programme_name_column', 'Programme')
    dept_name_key = parameters.get('department_column', 'Department')
    gov_key = parameters.get('government_column', 'Province')
    sphere = parameters['sphere']

    if sphere == 'national':
        government_name = 'South Africa'
    elif sphere == 'provincial':
        government_name = row[gov_key]
    else:
        raise Exception("Invalid sphere parameter")

    department_name = row[dept_name_key]
    auth_prog_name \
        = programme_names[sphere][government_name][department_name].\
        get(slugify(row[prog_name_key]), None)
    if auth_prog_name:
        row[prog_name_key] = auth_prog_name
    else:
        warning_key = (government_name, row[dept_name_key], row[prog_name_key])
        if warning_key not in warned:
            logging.warning("No authoritative programme name found for %s - %s - %s (%s)",
                            government_name, row[dept_name_key], row[prog_name_key],
                            slugify(row[prog_name_key]))
            warned[warning_key] = True
    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
