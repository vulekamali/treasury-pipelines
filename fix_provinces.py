from datapackage_pipelines.wrapper import process
import logging

PROVINCE_MAPPING = {
    'NORTH WEST': 'North West',
    'GAUTENG': 'Gauteng',
    'EASTERN CAPE': 'Eastern Cape',
    'WESTERN CAPE': 'Western Cape',
    'NORTHERN CAPE': 'Northern Cape',
    'LIMPOPO': 'Limpopo',
    'KWAZULU-NATAL': 'KwaZulu-Natal',
    'FREE STATE': 'Free State',
    'MPUMALANGA': 'Mpumalanga'
}

def modify_datapackage(datapackage, parameters, stats):
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    government_column = parameters.get('government_column', 'government')
    try:
        row[government_column] = PROVINCE_MAPPING[row[government_column]]
        return row
    except:
        logging.exception("Error with row %r", row)
        raise


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
