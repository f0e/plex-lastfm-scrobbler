FROM python:3.12-alpine

WORKDIR /app

# install uv dependencies
RUN apk add --no-cache curl ca-certificates

# install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# ensure uv is in path
ENV PATH="/root/.local/bin/:$PATH"

ENV IN_DOCKER=true

COPY . .

# sync the project into a new environment, using the frozen lockfile
RUN uv sync --frozen

CMD ["uv", "run", "plex-last-fm-scrobbler"]
