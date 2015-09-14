play
====

Find and stream tracks from Google Play Music

You will need a Google Play Music account with All Access set up.

Add your account details to a config file called `play.cfg` and place it in the root directory.
The id for an android device is required for some endpoints. If a `device` is not specified, the computer's MAC address will be used as an ID. This usually works, but if not, set it manually. The current devices associated with your account can be retrieved with `/devices`.
```
[login]
email = <google account email>
password = <google account password>
device = <registered device id>

[server]
host = localhost
port = 8080
debug = false
```

You will also need to install Bottle, Paste, Requests and GMusicApi
```
> sudo pip install bottle paste requests gmusicapi
```
