from datapackage_pipelines.wrapper import process
from pprint import pformat
from slugify import slugify
import logging
import os
import requests
import csv

portal_url = os.environ.get("PORTAL_URL", "https://vulekamali.gov.za/")

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
    financial_years = list(department_names.keys())
    sphere = parameters["sphere"]
    for fin_year in financial_years:
        governments = []
        listing_url_path = fin_year + "/departments.csv"
        listing_url = portal_url + listing_url_path
        r = requests.get(listing_url)
        if r.status_code != 200 and r.status_code != 404:
            r.raise_for_status()
        elif r.status_code == 404:
            logging.warning(f"Departments couldn't be found in URL ({listing_url})!")
            continue

        reader = csv.DictReader(r.text.splitlines(), delimiter=",")
        for row in reader:
            if row["government"] not in governments:
                department_names[fin_year][sphere][row["government"]] = {}
                governments.append(row["government"])

            department_names[fin_year][sphere][row["government"]][
                slugify(row["department_name"])
            ] = row["department_name"]
    logging.info(pformat(department_names))
    return datapackage


def process_row(row, row_index, resource_descriptor, resource_index, parameters, stats):
    authoritative_department_name = None
    financial_year = parameters.get("financial_year_column", "FinYear")
    department_column = parameters.get("department_column", "department")
    government_column = parameters.get("government_column", "government")
    department_slug = slugify(row[department_column])
    sphere = parameters["sphere"]
    if sphere == "national":
        government_name = "South Africa"
    elif sphere == "provincial":
        government_name = row[government_column]
    else:
        raise Exception("Unknown sphere: %r" % sphere)
    year = row[financial_year]
    fin_year = year + "-" + str(int(year[2:]) + 1)
    if (
        fin_year in department_names.keys()
        and government_name in department_names[fin_year][sphere].keys()
    ):
        authoritative_department_name = department_names[fin_year][sphere][
            government_name
        ].get(department_slug, None)

    if authoritative_department_name:
        row[department_column] = authoritative_department_name
    else:
        warning_key = (government_name, row[department_column])
        if warning_key not in warned:
            logging.warning(
                "No authoritative department name found for %s - %s (%s) in %s",
                government_name,
                row[department_column],
                department_slug,
                fin_year,
            )
            warned[warning_key] = True
    return row


process(modify_datapackage=modify_datapackage, process_row=process_row)
