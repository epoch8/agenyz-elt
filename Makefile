VERSION=$(shell poetry version -s)
IMAGE=ghcr.io/epoch8/agenyz-elt:${VERSION}

build:
	docker build -t ${IMAGE} --progress=plain --ssh default --platform=linux/amd64 . 

upload:
	docker push ${IMAGE}

register:
	python prefect_register.py

all:
	make build 
	make upload 
	make register