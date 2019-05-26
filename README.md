#  X-o-Bot project

**Credits**: [@teamL](https://github.com/comp3300-comp9900-term-1-2019/capstone-project-teaml/) 

Warning !!!

This project is based on python3.6.

Please install python3.6 first!!! RASA does not support python3.7 for now.

Pip3's version has to be in python3.6 too.

## Install package
### 1. install frontend related package

Download node.js in
https://nodejs.org/en/download/

jquery:
```
npm install jquery
```

### 2. Install backend related package
```
pip3 install -r requirements.txt

python3 -m spacy download en

python3 
import nltk
nltk.download('wordnet')
```
Database config:
Change the database url and port in mongo_config.ini if you want to use your own database
```
vi rasa/mongo_config.ini
```

## Running the application
### 3. start system

```
bash start.sh
```

## input your question in comp9315
### 4. input in bar
User interface is on localhost:3000
```
You might need to wait for 15 seconds until the program being loaded
Input your question directly in the send bar, then click send
```


## Using docker
Dockerfile provided will give you an system with preinstalled nodejs,npm,python3.6

Build the docker image
```
docker build -t chatbot-bot .
```
start an container 

```
sudo docker run -it -p 3000:3000 -p 7001:7001 -p 5055:5055 --name <container_name> base bash

```
Then just following the instruction below. Program is in chat-bot
