CONTAINER_NAME=splunk
CONFIGURATION_BACKUP=$$(pwd)/.splunk_ta_dataset_config/
OUTPUT_PACKAGE=$$(pwd)/output/TA_dataset
SOURCE_PACKAGE=$$(pwd)/TA_dataset


.PHONY: docker-run
docker-splunk-run:
	docker run -it \
		-v "$(OUTPUT_PACKAGE):/opt/splunk/etc/apps/TA_dataset" \
		-e SPLUNK_START_ARGS=--accept-license \
		-e SPLUNK_PASSWORD=Test0101 \
		--platform=linux/amd64 \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		splunk/splunk:latest start

.PHONY: docker-splunk-start
docker-splunk-start:
	docker start -a $(CONTAINER_NAME)

.PHONY: docker-splunk-restart
docker-splunk-restart:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		/opt/splunk/bin/splunk restart

.PHONY: docker-splunk-stop
docker-splunk-stop:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		/opt/splunk/bin/splunk stop

.PHONY: docker-splunk-show-app
docker-splunk-show-app:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/TA_dataset/

.PHONY: docker-splunk-tail-logs
docker-splunk-tail-logs:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		tail -f \
			/opt/splunk/var/log/splunk/splunkd.log \
			/opt/splunk/var/log/splunk/splunkd_stderr.log

.PHONY: docker-splunk-bash
docker-splunk-bash:
	docker exec -i $(CONTAINER_NAME) \
		sudo -u splunk bash

.PHONY: docker-splunk-remove
docker-splunk-remove:
	docker container rm $(CONTAINER_NAME)


.PHONY: inspect
inspect:
	splunk-appinspect inspect TA_dataset --included-tags splunk_appinspect

.PHONY: pack
pack:
	mkdir -p $(CONFIGURATION_BACKUP) && \
	echo "Validate package" && \
	slim validate TA_dataset && \
	version=$$(jq -r '.meta.version' globalConfig.json) && \
	echo "Generate package - $${version}" && \
	ucc-gen --source TA_dataset --ta-version $${version} && \
	echo "Construct tarball" && \
	slim package output/TA_dataset -o release && \
	echo "Validate released tarball" && \
	slim validate release/TA_dataset-$${version}.tar.gz

dev-config-backup:
	mkdir -p $(CONFIGURATION_BACKUP) && \
	if [ -d $(OUTPUT_PACKAGE)/local/ ]; then \
		cp -v $(OUTPUT_PACKAGE)/local/* $(CONFIGURATION_BACKUP)/; \
	fi

dev-config-restore:
	mkdir -p $(CONFIGURATION_BACKUP) && \
	if [ -d $(CONFIGURATION_BACKUP) ]; then \
		mkdir -p $(OUTPUT_PACKAGE)/local/; \
		cp -v $(CONFIGURATION_BACKUP)/* $(OUTPUT_PACKAGE)/local/ ; \
	fi

dev-update-source:
	rsync -av $(SOURCE_PACKAGE)/bin/ $(OUTPUT_PACKAGE)/bin/
	rsync -av $(SOURCE_PACKAGE)/default/ $(OUTPUT_PACKAGE)/default/

dev-install-dependencies-pack:
	pip install --upgrade-strategy only-if-needed -r requirements-pack.txt
	sudo pip install --upgrade-strategy only-if-needed -r requirements-pack-sudo.txt

dev-install-dependencies-lib:
	pip install --upgrade-strategy only-if-needed -r TA_dataset/lib/requirements.txt

dev-install-dependencies-dev:
	pip install --upgrade-strategy only-if-needed -r requirements-dev.txt
