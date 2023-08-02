CONTAINER_NAME=splunk
CONFIGURATION_BACKUP=.splunk_ta_dataset_config

.PHONY: docker-run
docker-run:
	echo "$$(pwd)/output/TA_dataset:/opt/splunk/etc/apps/TA_dataset"
	docker run -it \
		-v "$$(pwd)/output/TA_dataset:/opt/splunk/etc/apps/TA_dataset" \
		-e SPLUNK_START_ARGS=--accept-license \
		-e SPLUNK_PASSWORD=Test0101 \
		--platform=linux/amd64 \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		splunk/splunk:latest start

.PHONY: docker-start
docker-start: docker-run

.PHONY: docker-restart
docker-restart:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		/opt/splunk/bin/splunk restart

.PHONY: docker-stop
docker-stop:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		/opt/splunk/bin/splunk stop

.PHONY: docker-show-app
docker-show-app:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/TA_dataset/

.PHONY: docker-tail-logs
docker-tail-logs:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		tail -f \
			/opt/splunk/var/log/splunk/splunkd.log \
			/opt/splunk/var/log/splunk/splunkd_stderr.log

.PHONY: docker-bash
docker-bash:
	docker exec -i $(CONTAINER_NAME) \
		sudo -u splunk bash

.PHONY: docker-remove
docker-remove:
	docker container rm $(CONTAINER_NAME)

.PHONY: inspect
inspect:
	splunk-appinspect inspect TA_dataset --included-tags splunk_appinspect

.PHONY: pack
pack:
	mkdir -p $(CONFIGURATION_BACKUP) && \
	echo "Validate package" && \
	slim validate TA_dataset && \
	echo "Preserve configuration" && \
	if [ -d ./output/TA_dataset/local/ ]; then \
  		cp -v ./output/TA_dataset/local/* $(CONFIGURATION_BACKUP); \
  	fi && \
	echo "Generate package" && \
	ucc-gen --source TA_dataset && \
	echo "Construct tarball" && \
	slim package output/TA_dataset -o release && \
	f=$$( ls -t release/TA_dataset* | head -n1 ) && \
	echo "Release file: $${f}" && \
	echo "Validate released tarball" && \
	slim validate $${f} && \
	echo "Check that secrets are not there" && \
	! $$( tar -tvf $${f} | grep "TA_dataset/local" ) && \
	echo "Move configuration back" && \
	mkdir -p ./output/TA_dataset/local/ && \
	cp -v $(CONFIGURATION_BACKUP)/* ./output/TA_dataset/local/


