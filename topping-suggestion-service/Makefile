format:
	yapf -r -i .

docker-build :
	docker build -t ponderosa/hs-pizza-topping-suggestion-service:$(IMAGE_TAG) .

docker-push :
	docker push ponderosa/hs-pizza-topping-suggestion-service:$(IMAGE_TAG)

docker-build-slow-startup:
	docker build -t ponderosa/topping-suggestion-slow-startup:$(IMAGE_TAG) -f Dockerfile-slow-startup .

docker-push-slow-startup:
	docker push ponderosa/topping-suggestion-slow-startup:$(IMAGE_TAG)
