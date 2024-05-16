docker build -f .\dockerfiles\elastic_client.dockerfile -t elastic_client .
docker build -f .\dockerfiles\dummy_endpoint.dockerfile -t dummy_endpoint .
docker build -f .\dockerfiles\preprocess_client.dockerfile -t preprocess_client .
docker build -f .\dockerfiles/demo-app.dockerfile -t demo-app --build-arg ELASTIC_CLIENT=http://elastic_client:80 --build-arg DUMMY_CLIENT=http://dummy_endpoint:80 .
docker compose up -d


# To run the preprocess client separately with all gpus: 
# docker run --name preprocess_client_container --gpus all -t preprocess_client