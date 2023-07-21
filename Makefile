.PHONY: inspect
inspect:
	splunk-appinspect inspect S1DataLake --included-tags splunk_appinspect

.PHONY: pack
pack:
	ucc-gen --source S1DataLake && \
	slim package output/S1DataLake -o release