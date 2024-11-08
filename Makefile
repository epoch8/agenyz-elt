VERSION=$(shell poetry version -s)
BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

ifeq ($(BRANCH), master)
    FINAL_VERSION := $(VERSION)
else
    FINAL_VERSION := $(VERSION)-$(BRANCH)
endif

IMAGE=ghcr.io/epoch8/agenyz-elt:${FINAL_VERSION}

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