filepath        :=      $(PWD)
versionfile     :=      $(filepath)/docker-image-version
version         :=      $(shell cat $(versionfile))

format:
	yapf -r -i .

docker-build:
	docker build -t ponderosa/topping-suggestion:$(version) .

docker-push:
	docker push ponderosa/topping-suggestion:$(version)


docker-build-slow-startup:
	docker build -t ponderosa/topping-suggestion-slow-startup:$(version) -f Dockerfile-slow-startup .

docker-push-slow-startup:
	docker push ponderosa/topping-suggestion-slow-startup:$(version)
