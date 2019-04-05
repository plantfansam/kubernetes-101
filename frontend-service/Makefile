check-envs :
	test $(IMAGE_TAG)

docker-init:
	docker login

docker-build : check-envs
	docker build -t ponderosa/hs-pizza-frontend-service:${IMAGE_TAG} .

docker-push : check-envs docker-init
	docker push ponderosa/hs-pizza-frontend-service:${IMAGE_TAG}

docker-bp : docker-build docker-push

format:
	yapf -r -i .
