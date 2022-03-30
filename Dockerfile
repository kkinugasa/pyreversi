# syntax=docker/dockerfile:1

FROM python:3.8.13-slim-bullseye as builder
WORKDIR /usr/src/app
ARG POETRY_VERSION=1.1.12
COPY pyproject.toml poetry.lock ./
RUN pip install --disable-pip-version-check --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.8.13-slim-bullseye
ARG PIP_VERSION=22.0.3
ARG USERNAME=python
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends\
RUN pip install --no-cache-dir --upgrade pip==${PIP_VERSION} && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf \
        requirements.txt \
        /tmp/* \
        /bin/mount \
        /bin/umount \
        /bin/su \
        /usr/bin/chage \
        /usr/bin/chfn \
        /usr/bin/chsh \
        /usr/bin/expiry \
        /usr/bin/gpasswd \
        /usr/bin/newgrp \
        /usr/bin/passwd \
        /usr/bin/wall \
        /sbin/unix_chkpwd \
        /var/lib/apt/lists/* && \
    groupadd -r ${USERNAME} && \
    useradd --no-log-init -r -g ${USERNAME} ${USERNAME}
COPY . .
USER ${USERNAME}:${USERNAME}
