# Treasury Datapackage Pipelines

Pipelines used to prepare data for upload to OpenSpending Packager while we're
not ready to use os-data-importers but need [datapackage-pipelines](https://github.com/frictionlessdata/datapackage-pipelines)

## Setup

If not using docker, install Python dependencies:

[Set up and activate a python 3 virtual environment.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

Install the dependencies in the virtual environment using `pip install -r requirements.txt`

## Running pipelines

List available pipelines with

```
dpp
```

or using docker

```
docker run --rm -it -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines
```

run a pipeline with

```
DPP_PROCESSOR_PATH=$PWD dpp run --verbose ./2018-19/national/aene/aene-2018-19
```

or using docker

```
docker run --rm -it -e "DPP_PROCESSOR_PATH=/pipelines" -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines run --verbose ./2018-19/national/aene/aene-2018-19
```

**Note important options:**

- environment variable `DPP_PROCESSOR_PATH` - help it find out processors
- argument `--verbose`: Actually give is some output so we know where things break

## Unique dimensions

OpenSpending relies on each row ignoring amounts having a unique set of dimension values.

In database terms, the composite primary key for each row, made up of each of the classification columns, must be unique.

To check if your dataset has unique rows or needs additional processing to make it unique, use `csvkit`. Install it in a different python virtualenv from datapackage-pipelines.

First list the fields to get their indexes:

```bash
csvcut -n 2017-18/national/processed/aene-2017-18.csv
```

Then count the number of rows for each combination of classifying fields by selecting all fields except the amount field, and counting the duplicate rows. If there are duplicate fields, the last rows in the output of the following command would be more than 1:

```bash
csvcut -C 14 2017-18/national/processed/aene-2017-18.csv | sort | uniq -c| sort -n
```

e.g.

```
14 24,"Agriculture, Forestry and Fisheries",4,Trade Promotion and Market Access,2,International Relations and Trade,Current,Transfers and subsidies,Foreign governments and international organisations,Foreign governments and international organisations,Foreign governments and international organisations,2017,Total,Adjusted appropriation
14 24,"Agriculture, Forestry and Fisheries",4,Trade Promotion and Market Access,2,International Relations and Trade,Current,Transfers and subsidies,Foreign governments and international organisations,Foreign governments and international organisations,Foreign governments and international organisations,2017,Total,Voted (Main appropriation)
24 6,International Relations and Cooperation,5,International Transfers,2,Membership contribution,Current,Transfers and subsidies,Foreign governments and international organisations,Foreign governments and international organisations,Foreign governments and international organisations,2017,Total,Adjusted appropriation
24 6,International Relations and Cooperation,5,International Transfers,2,Membership contribution,Current,Transfers and subsidies,Foreign governments and international organisations,Foreign governments and international organisations,Foreign governments and international organisations,2017,Total,Voted (Main appropriation)
```

In this case you should verify that the kind of duplication that's happening can be solved by summing all the duplicates, and adding the `join` processor's _deduplication_ mode.

Troubleshooting:
----------------

`dpp` output like this (`'NoneType' object has no attribute 'startswith'` in particular) sometimes means a spec section is indented differently to the rest. This often happens when copying between specs.

```
- ./2016-17/provincial/are/are-2016-17
- ./2014-15/national/ene/ene-2014-15 (*)
- ./budget-vs-actual/national/budget-vs-actual-national (*)
Traceback (most recent call last):
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/bin/dpp", line 11, in <module>
    load_entry_point('datapackage-pipelines==2.0.0', 'console_scripts', 'dpp')()
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/core.py", line 764, in __call__
    return self.main(*args, **kwargs)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/core.py", line 717, in main
    rv = self.invoke(ctx)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/core.py", line 1114, in invoke
    return Command.invoke(self, ctx)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/core.py", line 956, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/core.py", line 555, in invoke
    return callback(*args, **kwargs)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/click/decorators.py", line 17, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/datapackage_pipelines/cli.py", line 20, in cli
    for spec in pipelines():  # type: PipelineSpec
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/datapackage_pipelines/specs/specs.py", line 73, in pipelines
    for prefix in prefixes):
  File "/home/jdb/projects/vulekamali/treasury-pipelines/env/lib/python3.7/site-packages/datapackage_pipelines/specs/specs.py", line 73, in <genexpr>
    for prefix in prefixes):
AttributeError: 'NoneType' object has no attribute 'startswith'
