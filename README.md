# drone-test

This is just a test repo to try [drone](http://docs.drone.io/) with python.

## Drone local installation

First we need to install [docker-compose](https://docs.docker.com/compose/):

```bash
    # download / install docker-compose:
    sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # make it executable:
    sudo chmod +x /usr/local/bin/docker-compose
```

To run a Dockerized Drone, we follow [this instructions](http://docs.drone.io/installation/).

Mainly, we define a `docker-compose`:
```yaml
version: '2'

services:
  drone-server:
    image: drone/drone:0.8

    ports:
      - 80:8000
      - 9000
    volumes:
      - drone-server-data:/var/lib/drone/
    restart: always
    environment:
      - DRONE_OPEN=true
      - DRONE_HOST=${DRONE_HOST}
      - DRONE_GITHUB=true
      - DRONE_GITHUB_CLIENT=${DRONE_GITHUB_CLIENT}
      - DRONE_GITHUB_SECRET=${DRONE_GITHUB_SECRET}
      - DRONE_SECRET=${DRONE_SECRET}

  drone-agent:
    image: drone/agent:0.8

    command: agent
    restart: always
    depends_on:
      - drone-server
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DRONE_SERVER=drone-server:9000
      - DRONE_SECRET=${DRONE_SECRET}

volumes:
  drone-server-data:
```

Alternatively you can also start them individually:

### drone server
```bash
docker run \
  --volume=/var/lib/drone:/data \
  --env=DRONE_AGENTS_ENABLED=true \
  --env=DRONE_GITHUB_SERVER=https://github.com \
  --env=DRONE_GITHUB_CLIENT_ID=${DRONE_GITHUB_CLIENT_ID} \
  --env=DRONE_GITHUB_CLIENT_SECRET=${DRONE_GITHUB_CLIENT_ID} \
  --env=DRONE_RPC_SECRET=${DRONE_RPC_SECRET} \
  --env=DRONE_SERVER_HOST=${DRONE_SERVER_HOST} \
  --env=DRONE_SERVER_PROTO=${DRONE_SERVER_PROTO} \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:1
```

### drone runner
```bash
docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DRONE_RPC_PROTO=https \
  -e DRONE_RPC_HOST=https://e7f2bb11.ngrok.io \
  -e DRONE_RPC_SECRET=${DRONE_RPC_SECRET} \
  -e DRONE_RUNNER_CAPACITY=2 \
  -e DRONE_RUNNER_NAME=${HOSTNAME} \
  -p 3000:3000 \
  --restart always \
  --name runner \
  drone/agent:1
```


To run `drone` locally we will also need [ngrok](https://ngrok.com/) to expose the needed url and ports
```bash
    ngrok http 80
```

With this url we authorize `drone` as an
[OAuth application in guthub](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/),
and we take note of the `client ID` and the `client secret` to populate the environment variables;
`DRONE_GITHUB_CLIENT` and `DRONE_GITHUB_SECRET`


Finally, we start drone:
```bash
    docker-compose up
```

Heading to the ngrok provided url we can connect the github repos we want.
That's it, for those selected repos any pull request, push or tag will trigger a call to drone's webhooks thus
starting a run.


## Repository configuration

The repository to be connected to `drone` needs a `.drone.yml` file specifying the pipeline configuration,
as an example:
```yaml
pipeline:
  build:
    image: python:3.6.1-alpine
    commands:
      - pip install -r requirements.txt
      - pip install -r test-requirements.txt
      - pytest .

```


