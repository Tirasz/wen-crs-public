# Setup
**Dataset**  

You will need a .json dataset containing objects that follow the structure:

    {
      "_id": {
        "$binary": {
          "base64": string,
          "subType": string
        }
      },
      "channelId": {
        "$binary": {
          "base64": string,
          "subType": string
        }
      },
      "userId": string,
      "timestamp": {
        "$date": string
      },
      "updateTimestamp": {
        "$date": string
      }
      "content": string,
      "embeds": [
        {
          "type": string,
          "subType": string
          "fullUrl": string
        }
      ]
    }

This dataset needs to be copied into `'/src/dummy_endpoint/dummy/dataset.json'` 
Also put the mariadb dumps into `'/src/dummy_endpoint/dummy/mariadb/'` 

**Config**  

The `'/src/config.json'` file specifies the sentence-transformer and spacy models to be used to preprocess the dataset, and the index and pipeline names for the elasticsearch server.
 Make sure to change the `requirements.txt` files if you change the spacy models.  

The `'.env'` file specifies the docker container memory-limits, and the ports to expose the containers services on, among some other elastic-search specific configuration parameters.

**Docker images**  

Run the commands found in the `'run.sh'` file from the root directory to build the docker images:
  
**Docker compose**  

After all the custom images have been built, run the following command to start all the containers needed:

    docker compose up -d

This will spin up the elasticsearch server, and index all the documents found in your dataset after preprocessing. 

**Demo app**

Install the angular app's dependencies by running `'npm install'` and then serve the demo app with `'ng serve'` from the `'/src/demo-app'` directory.
