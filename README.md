# neo-polling

## Usage
### How to run
1. clone 

```sh
git clone https://github.com/makino-makino/neo-polling
cd neo-polling
```

2. set env

```sh
PASSWORD="email password"
EMAIL_FROM="email address"
PRIVKEY="pkcs8 private key"
PUBKEY="pkcs8 public key"
TIME="time to start vote"
DEPLOY_HOST="server hostname" # default to localhost
SERV_ENV=dev # change to `prod` to run in production env
INCUBATOR_PASS="BASIC auth password"
```

3. create empty mount points
```sh
mkdir -p data/certbot/{www,conf}
```

4. compile crypto module

```sh
cd crypto
docker-compose up
```

5. (production deploy only) generate TLS certificate
```sh
cd ../
./init-letsencrypt.sh
```

NOTE: If you need to renew certificate, run following.

```sh
docker-compose up certbot
```

6. run server

```sh
cd ../  # if you ran 4., skip this
docker-compose up
```

### Administration
You can send blind signature email using `/incubator`.

It requires BASIC auth, with username `incubator` and password defined in `.env`.


## Testing
### Integrated test
First, run:

```sh
pip3 install -r requirements.txt
```

Then run `chromedriver-path`, and replace `chromedriver_path` variable string with the output. For example, 

```sh
$ chromedriver-path
/opt/homebrew/lib/python3.9/site-packages/chromedriver_binary
```

```py
chromedriver_path = "/opt/homebrew/lib/python3.9/site-packages/chromedriver_binary/chromedriver" # previous output
```

Finally, you can run the integrated test:

```
python3 integrated-test.py
```

## ログについて
Docker のログは、何もしなくても `/var/lib/docker/containers` 以下に保存される。

各コンテナのログを見るときは、以下のようにする。

```sh
docker inspect --format='{{.LogPath}}' neo-polling_api_1
# e.g.) /var/lib/docker/containers/4598a887451112374f717b28ab56b12eb9687d20be1db9033c700a3e6bc4e056/4598a887451112374f717b28ab56b12eb9687d20be1db9033c700a3e6bc4e056-json.log

sudo less /var/lib/docker/containers/4598a887451112374f717b28ab56b12eb9687d20be1db9033c700a3e6bc4e056/4598a887451112374f717b28ab56b12eb9687d20be1db9033c700a3e6bc4e056-json.log
```