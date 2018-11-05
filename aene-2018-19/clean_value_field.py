from datapackage_pipelines.wrapper import process


def modify_datapackage(datapackage, parameters, stats):
    # Do something with datapackage
    return datapackage


def process_row(row, row_index,
                resource_descriptor, resource_index,
                parameters, stats):
    col_key = parameters.get('value_field', 'Value')
    value = row[col_key]
    row[col_key] = str(int(value.replace(",", "")) * 1000)
    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row)
