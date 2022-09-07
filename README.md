# To Run the project
uvicorn Main:api --reload

# Docker command 
docker image build . -t rainproject:latest
docker image build ./test/TestStatusAPI -t rainproject-status-tester:latest
docker image build ./test/TestPredictionAPI -t rainproject-prediction-tester:latest
docker image build ./test/TestAuthentification -t rainproject-authentification-tester:latest
docker image build ./test/TestClassifierScoringInfoAPI -t rainproject-scoring-tester:latest
docker image build ./test/TestClassifierListAPI -t rainproject-list-tester:latest

cd ./test && docker-compose up

# Kubernetes command

kubectl create -f ./Kubernetes/rainproject-deployment.yml
kubectl create -f ./Kubernetes/rainproject-ingress.yml
kubectl create -f ./Kubernetes/rainproject-service.yml

minikube start
kubectl proxy 





