# Vulekamali publishes tabled year as "Main appropriation", not "Medium Term Estimates"

from datapackage_pipelines.wrapper import process

import logging

def modify_datapackage(datapackage, parameters, stats):
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    financial_year = parameters.get('financial_year')

    if row['Budget Phase'] == 'Medium Term Estimates' and row['FinYear'] == financial_year:
        row['Budget Phase'] = 'Main appropriation'

    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
