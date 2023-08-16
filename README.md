# apache-airflow-learnings

## Standalone Installation

### Install Apache Airflow 


> pip install apache-airflow


### Initialize Airflow Database

> airflow db init


### Create a user for Airflow


> airflow users  create --role Admin --username krishna --email krishna --firstname krishna --lastname krishna --password krishna


### Start Airflow Server

> airflow webserver -p 8080


## Installing Apache Airflow with Docker


### Install Docker Desktop on Ubuntu

For non-Gnome Desktop environments, gnome-terminal must be installed:

 > sudo apt install gnome-terminal

 Uninstall the tech preview or beta version of Docker Desktop for Linux. Run:


 > sudo apt remove docker-desktop


 For a complete cleanup, remove configuration and data files at $HOME/.docker/desktop, the symlink at /usr/local/bin/com.docker.cli, and purge the remaining systemd service files.

 > rm -r $HOME/.docker/desktop

 > sudo rm /usr/local/bin/com.docker.cli

 > sudo apt purge docker-desktop

Set up the repository

Update the apt package index and install packages to allow apt to use a repository over HTTPS:

> sudo apt-get update

>  sudo apt-get install ca-certificates curl gnupg

Add Docker’s official GPG key:

> sudo install -m 0755 -d /etc/apt/keyrings

> curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

> sudo chmod a+r /etc/apt/keyrings/docker.gpg

Use the following command to set up the repository:

> echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  Update the apt package index:

  > sudo apt-get update

Download the [DEB package](https://docs.docker.com/desktop/install/ubuntu/)

> sudo apt-get install '''your deb file with path'''

Start Docker Dessktop

> systemctl --user start docker-desktop

First time Docker will ask you enter details like Name, Email.

Generate Credemtials for Docker

> gpg --generate-key



Install docker compose

> sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)"  -o /usr/local/bin/docker-compose


> sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose


> sudo chmod +x /usr/bin/docker-compose

Start Docker engine

> systemctl --user start docker-desktop 

Cross check installations

> docker --version
> docker-compose --version

To deploy Airflow in Docker

> curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'


After this command docker-compose.yaml file will be added to your directory


Change 

> AIRFLOW__CORE__EXECUTOR: CeleryExecutor

to 

> AIRFLOW__CORE__EXECUTOR: LocalExecutor

Delete

```yaml

 AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow> AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

 redis:
  condition: service_healthy

  redis:
    image: redis:latest
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
      start_period: 30s
    restart: always


airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully  
        
        
  flower:
    <<: *airflow-common
    command: celery flower
    profiles:
      - flower
    ports:
      - "5555:5555"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully        

```

Initiaizing Environment

```terminal

mkdir -p ./dags ./logs ./plugins ./config

```

If OS is Linux, execute this command

```terminal

echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Initialize db

```terminal

docker compose up airflow-init
```

Running Airflow

```terminal

docker compose up
```

If you want to run airflow in detached mode, i.e in background

```terminal

docker compose up -d
```

After starting, if you login at http://0.0.0.0:8080, you will get a airflow login page.  GIve username:airflow,  password: airflow and you will be able to see some example dags listed.

Stopping the airflow, if we use -v while shutting down 

```terminal

docker compose down -v

```

Before writing our own DAG, stop loading examples

```yaml

AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
```
to

```yaml

AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```

We have to do initialize the airflow db

```terminal

docker-compose up airflow-init
```


Let's start the airflow

```terminal

docker compose up -d
```


For DAG's implementation go through DAG files in dags folder.

Implemented 
  Bash Operator
  Python Operator

  
