filepath        :=      $(PWD)
versionfile     :=      $(filepath)/docker-image-version
version         :=      $(shell cat $(versionfile))

format:
	yapf -r -i .

docker-build:
	docker build -t ponderosa/intellipod:$(version) .

docker-push:
	docker push ponderosa/intellipod:$(version)
