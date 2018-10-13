# drone-test

This is just a test repo to try [drone](http://docs.drone.io/) with python.

# Drone local installation

First we need to install [docker-compose](https://docs.docker.com/compose/):

```bash
    # download / install docker-compose:
    sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # make it executable:
    sudo chmod +x /usr/local/bin/docker-compose
```

To run a Dockerized Drone, we follow [this instructions](http://docs.drone.io/installation/).

Mainly, we define a `docker-compose`:
```bash
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


