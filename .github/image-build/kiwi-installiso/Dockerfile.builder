ARG BASE_IMAGE=git.openruyi.cn/openruyi/creek-x86-64@sha256:ca64fcdb246b38a775ee586e8369d4432899a6d30f6c76340f2397d88efb865e
FROM ${BASE_IMAGE}

RUN dnf5 install -y \
        bash \
        curl \
        kiwi \
        kiwi-systemdeps \
        python3 \
        python3-kiwi \
        sudo && \
    dnf5 clean all

WORKDIR /work
