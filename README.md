# plex last.fm scrobbler

Made this because the official Plex Last.fm scrobbler can't filter by library and isn't the best.

## features

- Scrobbles to Last.fm
- Has a library filter so you don't scrobble audiobooks etc
- Shows currently playing song in Last.fm

## environment variables

- PLEX_SERVER_URL: Your plex server URL.
- PLEX_TOKEN: A [Plex token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token).
- PLEX_LIBRARIES: Comma-separated list of libraries that will be scrobbled.
- LASTFM_API_KEY: A [Last.fm API key](https://www.last.fm/api/account/create).
- LASTFM_API_SECRET: A [Last.fm API secret for the API key provided](https://www.last.fm/api/account/create).
- LASTFM_USERNAME: Your Last.fm username.
- LASTFM_PASSWORD: Your Last.fm password. _(I have no idea why, but you need username+password in order to perform any write operations like scrobbling. Seems strange, but it's hashed before being sent to Last.fm so it's fine I guess. Might make the environment variable take a hashed input too for security)_
