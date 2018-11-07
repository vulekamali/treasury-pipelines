# Treasury Datapackage Pipelines

Datapackage used to prepare data for upload to OpenSpending Packager while we're
not ready to use os-data-importers but need datapackage-pipelines

list available pipelines with

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