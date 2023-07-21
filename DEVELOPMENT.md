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

## Useful Links

* Configuration documentation - https://docs.splunk.com/Documentation/Splunk/9.1.0/Admin/Searchbnfconf
