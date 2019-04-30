from datapackage_pipelines.wrapper import process
import logging


def modify_datapackage(datapackage, parameters, stats):
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    value_field = parameters.get('value_field', 'value')
    try:
        row[value_field] = round(row[value_field])
        return row
    except:
        logging.exception("Error with row %r", row)
        raise


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
