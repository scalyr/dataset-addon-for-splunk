# Development

## Install Development Tools

We need following tools:
* AppInspect - https://dev.splunk.com/enterprise/reference/appinspect/appinspectcliref
  * Requires Python 3.8 - https://devguide.python.org/versions/
* UCC Framework - https://splunk.github.io/addonfactory-ucc-generator/quickstart/

So you should run following commands:

* Create venv with Python3.8: `python3.8 -m venv venv`
* Activate it: `source venv/bin/activate`
* Install dependencies:
  * `pip install "cython<3.0.0"`
  * `pip install wheel`
  * `pip install --no-build-isolation pyyaml==5.4.1`
  * `pip install --upgrade-strategy only-if-needed splunk-appinspect`
  * `pip install --upgrade-strategy only-if-needed splunk-add-on-ucc-framework`
  * `pip install --upgrade-strategy only-if-needed splunk-packaging-toolkit`

## Inspection Tool

Make sure, that the application is valid:
* `splunk-appinspect inspect S1DataLake --included-tags splunk_appinspect`

## Packaging

Use the UCC Framework to [pack the application](https://splunk.github.io/addonfactory-ucc-generator/quickstart/#build-already-existing-add-on).
* `ucc-gen --source S1DataLake`
* `slim package output/S1DataLake -o release`


## TroubleShooting

### ModuleNotFoundError

It was happening that some of the files were failing on:
```
Traceback (most recent call last):
  File "apps/TA_s1datalake/bin/dataset_search_command.py", line 13, in <module>
    from dataset_api import *
ModuleNotFoundError: No module named 'dataset_api'
```

I have fixed it by swapping order of imports. Initially there was `dataset_common` and after that `dataset_api`. After swapping it has started to work.

I have checked, that it works in UI, but also with:
```bash
cd /opt/splunk/etc

for f in `find apps/TA_s1datalake/bin/ -name '*.py'`; do
  echo $f;
  LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/opt/splunk/lib" /opt/splunk/bin/python3.7 $f;
done;
```
Many of these scripts are trying to perform some action which fails, but none of them fails on `ModuleNotFoundError`.

## Useful Links

* Configuration documentation - https://docs.splunk.com/Documentation/Splunk/9.1.0/Admin/Searchbnfconf
