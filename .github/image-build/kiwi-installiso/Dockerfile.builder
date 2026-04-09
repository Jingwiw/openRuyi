ARG BASE_IMAGE=docker.io/opensuse/tumbleweed@sha256:ef83be77fac5207611adab5407f6c8b0ca5dd4f1924ad30682f53e807dd13f3d
FROM --platform=linux/amd64 ${BASE_IMAGE}

RUN zypper --non-interactive refresh && \
    zypper --non-interactive install -y bash curl dnf5 kiwi-systemdeps perl python3 python3-kiwi sudo && \
    zypper clean -a

WORKDIR /work
