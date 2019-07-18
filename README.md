# 1. Description

This project is a demo project to use Aiven services.

The first part will publish events to a Kafka topic.
The second part will receive events from a Kafka topic and insert the information to a Postgres database.

# 2. Requirements

## a. Postgres

You will need to have a postgres instance runnning with SSL configured.
You need to have a database created and specified in your config file. In this file you need to create a table called
event. You should use the provided sql file in sql directory to create this table in your database.

## b. Kafka

You need a Kafka instance running with SSL configured
You will also need a Kafka topic created. By default the application uses aiven_event as the topic name. This needs to
exist before you start the application

# 3. Installation

## a. Clone this git repo

```shell
git clone https://github.com/alexandv/aiven_demo
```

Then switch to the directory.

## b. Create the configuration file

This is the file that specifies how to connect to the Kafka broker and to the postgres database.
There is a template available in config.ini.template.

You need to provide all the parameters present in this file.

## c - option 1. Build using Docker

### - Requirements:
A recent verion of docker with the daemon currently running on your machine

### - Installation:
First build the image using the following command while inside the root directory:
```shell
docker build . -t aiven
```

This could take a few minutes depending on how fast your connection is.

Then try to run the image using the following:
docker run aiven
Without any additional arguments this will display usage for the tool.
If this worked you can then skip to the third section.

## c - option 2. Install packages using Python

### - Requirements:
python3 with a version greater than 3.4
(optionally) virtualenv

### - Installation:
This will install the required package in the current virtual environment or globally if you are not in any:
```shell
pip3 install -r pip/requirements.txt
```

Update the configuration file.
By default this file is located in the root directory and named config.ini.

# 3. How to use

## a. Consumption

This will start a subscriber on the topic specified and for each message received insert it into the postgres database
specified in the config.ini file.
Note that the table event needs to exist before starting the consumer. See requirements on how to create this table.

### - If you used docker:
```shell
docker run -v `pwd`:/aiven/config aiven --config config/<Path to your config file> sub
```

### - Using python:
```shell
python3 aiven/aiven_cmd.py --config <Path to your config file>
```

## b. Publication

This will publish a message on the Kafka topic specified using the configuration provided in the config file.

### - If you used docker:
```shell
docker run aiven --config <Path to your config file> post
```

### - Using python:
```shell
python3 aiven/aiven_cmd.py --config <Path to your config file> post
```

# TODO

### Add unit testing and functional testing.

### Improve error handling.

### Add more configuration options
