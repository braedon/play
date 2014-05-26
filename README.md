play
====

Find and stream tracks from Google Play Music

You will need a Google Play Music account with All Access set up.

Add your account details to a config file called `play.cfg` and place it in the root directory.
```
[login]
email = <google account email>
password = <google account password>

[server]
host = localhost
port = 8080
debug = false
```

You will also need to install Bottle, Requests and GMusicApi
```
> sudo pip install bottle requests gmusicapi
```
