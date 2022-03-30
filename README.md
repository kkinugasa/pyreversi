# PyReversi

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![coverage badge](./docs/figs/coverage.svg)

## Setup

### Install from this source code

```sh
git clone https://github.com/kkinugasa/pyreversi.git
poetry install
```

### Install with poetry

```sh
poetry add git+https://github.com/kkinugasa/pyreversi.git
```

### Install with pip

```sh
pip install git+https://github.com/kkinugasa/pyreversi.git
```

## Documentation

After pulling this repo and running `poetry install`, run the command:

```sh
poetry run mkdocs serve
```

Then access <http://127.0.0.1:8888>

## Play

`python -m pyreversi`

## Docker

Build

`make docker`

Play

```sh
export VERSION=$(sed -n 's/__version__ = "\(.*\)"/\1/p' pyreversi/_version.py)
docker run --rm -it pyreversi:$VERSION python -m pyreversi
```

## Kubernetes

Create cluster

```sh
kind create cluster --config kind.yaml
```

Deploy

```sh
skaffold run
```

Play

```sh
export PYREVERSI_POD=$(kubectl get pods --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
kubectl exec -it $PYREVERSI_POD -- python -m pyreversi
```

Delete cluster

```sh
skaffold delete
kind delete cluster
```
