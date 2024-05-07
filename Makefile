CONTAINER_NAME=splunk
CONFIGURATION_BACKUP=$$(pwd)/.splunk_ta_dataset_config/
OUTPUT_PACKAGE=$$(pwd)/output/TA_dataset
SOURCE_PACKAGE=$$(pwd)/TA_dataset


.PHONY: docker-splunk-run
docker-splunk-run:
	make docker-splunk-run-shared FLAGS="-it"

.PHONY: docker-splunk-run-ci
docker-splunk-run-ci:
	make docker-splunk-run-shared FLAGS="-d"

docker-splunk-run-shared:
	docker run $(FLAGS) \
		-v "$(OUTPUT_PACKAGE):/opt/splunk/etc/apps/TA_dataset" \
		-e SPLUNK_START_ARGS=--accept-license \
		-e SPLUNK_PASSWORD=Test0101 \
		--platform=linux/amd64 \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		splunk/splunk:9.1 start

docker-splunk-run-vanilla:
	docker run -it \
		-e SPLUNK_START_ARGS=--accept-license \
		-e SPLUNK_PASSWORD=Test0101 \
		--platform=linux/amd64 \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		splunk/splunk:9.1 start

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

.PHONY: docker-splunk-kill
docker-splunk-kill:
	docker kill $(CONTAINER_NAME)

.PHONY: docker-splunk-show-app
docker-splunk-show-app:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -l /opt/splunk/etc/apps/TA_dataset/

.PHONY: docker-splunk-list-logs
docker-splunk-list-logs:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		ls -lrt \
			/opt/splunk/var/log/splunk/

.PHONY: docker-splunk-tail-log
docker-splunk-tail-log:
	docker exec $(CONTAINER_NAME) \
		bash -l -c "sudo -u splunk tail -f /opt/splunk/var/log/splunk/${LOG_NAME}"

.PHONY: docker-splunk-tail-logs-splunkd
docker-splunk-tail-logs-splunkd:
	make docker-splunk-tail-log LOG_NAME=splunkd.log

.PHONY: docker-splunk-tail-logs-python
docker-splunk-tail-logs-python:
	make docker-splunk-tail-log LOG_NAME=python.log

# TODO: Figure out, how to make this work!
.PHONY: docker-splunk-tail-logs-app-all
docker-splunk-tail-logs-app-all:
	make docker-splunk-tail-log LOG_NAME="TA_dataset*"

.PHONY: docker-splunk-tail-logs-app-search-command
docker-splunk-tail-logs-app-search-command:
	make docker-splunk-tail-log LOG_NAME="TA_dataset_search_command.log"

.PHONY: docker-splunk-tail-logs
docker-splunk-tail-logs-count:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		tail -n $(COUNT) \
			/opt/splunk/var/log/splunk/splunkd.log

.PHONY: docker-splunk-bash
docker-splunk-bash:
	docker exec -i $(CONTAINER_NAME) \
		sudo -u splunk bash

.PHONY: docker-splunk-remove
docker-splunk-remove:
	docker container rm $(CONTAINER_NAME)

docker-splunk-exec-search:
	docker exec $(CONTAINER_NAME) \
		sudo -u splunk \
		/opt/splunk/bin/splunk \
			cmd python \
			/opt/splunk/etc/apps/TA_dataset/bin/dataset_search_command.py


.PHONY: inspect
inspect:
	splunk-appinspect inspect TA_dataset --included-tags splunk_appinspect

.PHONY: pack
pack: clean
	find $(SOURCE_PACKAGE) -name __pycache__ -exec rm -rfv {} \;
	version=$$(jq -r '.meta.version' globalConfig.json) && \
	scripts/pack.sh \
		--version "$${version}" \
		--input TA_dataset \
		--output output \
		--release release

dev-wait-for-splunk:
	docker ps
        while [ "$(docker ps -f name=splunk --format 'table {{.Names}},{{.Status}}' | grep 'healthy' -c)" -ne 1 ]; do echo "waiting until splunk container is healthy"; sleep 1; done
        docker ps
	awaitedStatus=303; \
	status=900; \
	while [ "x$${status}" != "x$${awaitedStatus}" ]; do \
		status=$$(curl --connect-timeout 10 -s -o /dev/null -I -w "%{http_code}" http://localhost:8000/ ); \
		echo "Status: $${status}; Awaited: $${awaitedStatus}"; \
		docker ps; \
		sleep 5; \
	done; \
	docker ps;

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
	rsync -av $(SOURCE_PACKAGE)/lib/dataset_query_api_client/ $(OUTPUT_PACKAGE)/lib/dataset_query_api_client/

dev-install-dependencies-pack:
	pip install --upgrade-strategy only-if-needed -r requirements-pack.txt
dev-install-dependencies-pack-sudo:
	pip install --upgrade-strategy only-if-needed -r requirements-pack-sudo.txt

dev-install-dependencies-lib:
	pip install --upgrade-strategy only-if-needed -r TA_dataset/lib/requirements.txt

dev-install-dependencies-for-development:
	pip install --upgrade-strategy only-if-needed -r requirements-dev.txt

test:
	pytest

e2e-install:
	npm ci
	npm run playwright:install-browsers

e2e-test:
	npm run playwright
e2e-test-headed:
	npm run playwright:headed
e2e-test-ui:
	npm run playwright:ui

.PHONY: clean
clean:
	find $(SOURCE_PACKAGE) -name '.DS_Store' -exec rm -rfv {} \;
