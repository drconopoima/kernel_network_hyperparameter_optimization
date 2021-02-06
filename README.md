# kernel_network_hyperparameter_optimization

Kernel Network Tunables Hyperparameter Optimization.

Nim's HTTPbeast Server running in Raspberry Pi 4.

## Server Compilation

```sh
# Install httpbeast package
nimble install -y httpbeast --nim:"$HOME/.nimble/nim/bin/nim"
# Compile server
nim c -d:release --threads:on server/httpbeast_server.nim
```

## Run HTTP server

```sh
./server/httpbeast_server.nim
```

Server listens on port 9292.

## Run K6 loadtest in server mode

```sh
k6 run --quiet --linger -e ENDPOINT=localhost:9292 k6/loadtest_server.js
```

## Server Installation

### Compile nim from source

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
./bin/nimble refresh -y --nim:"$HOME/.nimble/nim/bin/nim"
# Install latest nimble
./bin/nimble install -y nimble --nim:"$HOME/.nimble/nim/bin/nim"
```

Add `$HOME/.nimble/bin/` to your path:

```sh
echo "PATH=\"$PATH:$HOME/.nimble/bin/\"" | tee -a $HOME/.bashrc
```
