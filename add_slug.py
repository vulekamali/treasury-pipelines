from datapackage_pipelines.wrapper import process
from slugify import slugify

def modify_datapackage(datapackage, parameters, stats):
    datapackage['resources'][0]['schema']['fields'].append({
      'name': parameters['new-column-name'],
      'type': 'string'
    })
    return datapackage

def process_row(row, row_index, resource_descriptor, resource_index, parameters, stats):
    slug_string = row[parameters['slug-from-1']] + '-' + row[parameters['slug-from-2']]
    slug = slugify(slug_string, to_lower=True)
    print(slug)
    row[parameters['new-column-name']] = slug
    return row

process(modify_datapackage=modify_datapackage,
        process_row=process_row)