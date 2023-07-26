.PHONY: inspect
inspect:
	splunk-appinspect inspect TA_s1datalake --included-tags splunk_appinspect

.PHONY: pack
pack:
	slim validate TA_s1datalake && \
	ucc-gen --source TA_s1datalake && \
	slim package output/TA_s1datalake -o release