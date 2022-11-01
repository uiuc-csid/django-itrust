ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}
ARG POETRY_VERSION=1.2.0

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Configure apt and install packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        xmlsec1 \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /workspace/opportunities

ENV DEBIAN_FRONTEND=dialog