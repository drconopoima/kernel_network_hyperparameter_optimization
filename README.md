# kernel_network_hyperparameter_optimization

Kernel Network Tunables Hyperparameter Optimization.

Tested against Nim's HTTPbeast Server running in a Raspberry Pi 4.

## Run K6 server externally-controlled executor

```sh
k6 run --quiet --linger --paused --env ENDPOINT=<host-address>:<host-port> k6/loadtest_server.js
```

If you use the sample Nim HTTPbeast server locally, you will need to set host address to localhost and port 9292

```sh
k6 run --quiet --linger --paused -e ENDPOINT=localhost:9292 k6/loadtest_server.js
```

## Dependencies

- Requests >= 2.25.0

### Installation

```sh
    python3 -m venv ./venv
    source ./venv/bin/activate
    python -m pip install -r requirements.txt
```

## Usage

### Show K6 Status

```sh
    ./kernel_network_hyperparameter_optimization.py -a "http://<k6url>:<k6port>" --status
```

### Pause/Unpause K6 server

```sh
    ./kernel_network_hyperparameter_optimization.py --address="http://localhost:6565" --[un]pause
```

## Sample Crystal HTTP Server

### Server Compilation

```sh 
crystal build -Dpreview_mt --release server/crystal_server.cr
```

### Run HTTP Server

```sh
./crystal_server 
```

Server listens on port 9292.

### Crystal Installation

#### Ubuntu/Debian Package

```sh
curl -fsSL https://download.opensuse.org/repositories/devel:languages:crystal/xUbuntu_22.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/archive_uri-https_download-opensuse-org_repositories_devel-languages-crystal_xUbuntu_22-04_Release-key.gpg > /dev/null
echo 'deb http://download.opensuse.org/repositories/devel:/languages:/crystal/xUbuntu_22.04/ /' | sudo tee /etc/apt/sources.list.d/archive_uri-https_download-opensuse-org_repositories_devel-languages-crystal_xUbuntu_22-04_Release-key.list
sudo apt update
sudo apt install crystal
```

## Sample HTTPbeast Server

### Server Compilation

```sh
# Install httpbeast package
nimble install -y httpbeast # --nim:"$HOME/.nimble/nim/bin/nim" # Optionally provide route to custom nim install

# Compile server
nim c -d:release --threads:on server/httpbeast_server.nim
```

### Run HTTP server

```sh
./server/httpbeast_server.nim
```

Server listens on port 9292.

### Nim Installation

#### Ubuntu/Debian Package

```sh
sudo apt-get install nim nim-doc
```

#### Compile nim from source

```sh
sudo apt-get install wget jq build-essential -y
mkdir -p sources/nim-lang/nim
cd sources/nim-lang/nim
# Download latest version
wget https://nim-lang.org/download/nim-$(curl -s https://api.github.com/repos/nim-lang/Nim/tags | jq '.[0].name' | tr -d '"' | tr -d 'v').tar.xz -O nim.tar.xz
# Extract
tar -xJf nim.tar.xz
cd $(find . -mindepth 1 -maxdepth 1 -type d -name "nim-[0-9].[0-9].[0-9]" -exec ls -td {} +)
./build.sh
./bin/nim c koch
./koch tools
./koch nimble
sh ./install.sh $HOME/.nimble
# Nimble refresh package list
# As of 2022-10-15, OpenSSL 3 isn't supported by nim, need to provide LD_LIBRARY_PATH to compiled libssl.so, see section [Compile OpenSSL 1.1.1 Ubuntu 22.04]() below
./bin/nimble refresh -y --nim:"$HOME/.nimble/nim/bin/nim"
# Install latest nimble
./bin/nimble install -y nimble --nim:"$HOME/.nimble/nim/bin/nim"
ln -s -T ~/.nimble/nim/bin/nim ~/.nimble/bin/nim 
```

Add `$HOME/.nimble/bin/` to your path:

```sh
echo "PATH=\"$PATH:$HOME/.nimble/bin/\"" | tee -a $HOME/.bashrc
```

#### Compile OpenSSL 1.1.1 Ubuntu 22.04
```sh
wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/openssl/1.1.1l-1ubuntu1.6/openssl_1.1.1l.orig.tar.gz
tar -xvf openssl_1.1.1l.orig.tar.gz
cd openssl-1.1.1l/
./config
make
cd ..
LD_LIBRARY_PATH=./openssl-1.1.1l ./bin/nimble refresh -y --nim:"$HOME/.nimble/nim/bin/nim"
LD_LIBRARY_PATH=./openssl-1.1.1l ./bin/nimble install -y nimble --nim:"$HOME/.nimble/nim/bin/nim"
cp ./openssl-1.1.1l/libssl.so "$HOME/.nimble/nim/"
```

## K6 Loadtest installation

### Snap package

```sh
sudo snap install k6
```
