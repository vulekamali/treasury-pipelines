# Treasury Datapackage Pipelines

Pipelines used to prepare data for upload to OpenSpending Packager while we're
not ready to use os-data-importers but need datapackage-pipelines

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