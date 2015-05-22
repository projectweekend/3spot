### Environment variables

* `AWS_ACCESS_KEY_ID`: The AWS Access Key associated with your account
* `AWS_SECRET_ACCESS_KEY`: The AWS Secret Access Key associated with your account
* `SPOTIFY_CLIENT_ID`: The Spotify Client ID for your app in the [Spotify Developer portal](https://developer.spotify.com/my-applications)
* `SPOTIFY_CLIENT_SECRET`: The Spotify Client Secret for your app in the [Spotify Developer portal](https://developer.spotify.com/my-applications)
* `ECHO_NEST_API_KEY`: The Echo Nest API Key from your [developer account page](https://developer.echonest.com/account/profile).


### Build a Docker image

```
docker build -t name_of_image .
```


### Launch worker container for local development

```
docker run -it \
-e AWS_ACCESS_KEY_ID=accessKeyValue \
-e AWS_SECRET_ACCESS_KEY=secretKeyValue \
-e SPOTIFY_CLIENT_ID=spotifyClientIdValue \
-e SPOTIFY_CLIENT_SECRET=spotifyClientSecretValue \
-e ECHO_NEST_API_KEY=echoNestApiKeyValue \
-v $PWD:/src name_of_image
```


### Launch worker container

```
docker run --rm \
-e AWS_ACCESS_KEY_ID=accessKeyValue \
-e AWS_SECRET_ACCESS_KEY=secretKeyValue \
-e SPOTIFY_CLIENT_ID=spotifyClientIdValue \
-e SPOTIFY_CLIENT_SECRET=spotifyClientSecretValue \
-e ECHO_NEST_API_KEY=echoNestApiKeyValue \
-- name name_of_container name_of_image
```
