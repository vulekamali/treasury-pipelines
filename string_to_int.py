from datapackage_pipelines.wrapper import process
import logging


def modify_datapackage(datapackage, parameters, stats):
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    column_name = parameters.get('column_name')
    try:
        val = row[column_name]
        if isinstance(val, str):
            if "." in val:
                val = float(val)
            row[column_name] = int(val)
        return row
    except:
        logging.exception("Error with row %r", row)
        raise


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
