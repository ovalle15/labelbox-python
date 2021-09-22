
build:
	docker build -t local/labelbox-python:test .


test-dev: build
	docker run -it -v ${PWD}:/usr/src -w /usr/src \
		-e LABELBOX_INSTANCE_ID=${LABELBOX_INSTANCE_ID} \
		-e LABELBOX_TEST_API_KEY=${LABELBOX_TEST_API_KEY} \
		local/labelbox-python:test pytest tests/integration -svv

