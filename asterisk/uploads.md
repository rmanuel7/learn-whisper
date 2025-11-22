# [Asynchronous Javascript Asterisk Manager AJAM](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Allow-Manager-Access-via-HTTP/#configuring-managerconf)

# Allow Manager Access via HTTP

> [!WARNING]
> **AJAM is not supported and may have issues and may be removed in the future**.
> Do not use it if at all possible. Use standard TCP based AMI instead.

## [Configuring manager.conf](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Allow-Manager-Access-via-HTTP/#configuring-managerconf "Permanent link")

1.  Make sure you have **both** `"enabled = yes` and `webenabled = yes` setup in `/etc/asterisk/manager.conf`
2.  You may also use `httptimeout` to set a default timeout for HTTP connections.
3.  Make sure you have a manager `username`/`secret`

## [Usage of AMI over HTTP](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Allow-Manager-Access-via-HTTP/#usage-of-ami-over-http "Permanent link")

Once those configurations are complete you can `reload` or `restart` Asterisk and you should be able to point your web browser to specific URI's which will allow you to access various web functions. 

A complete list can be found by typing `http show status` at the Asterisk CLI.

### [Examples:](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Allow-Manager-Access-via-HTTP/#examples "Permanent link")

Be sure the syntax for the URLs below is followed precisely

*   http://localhost:8088/manager?action=login&username=foo&secret=bar

This logs you into the manager interface's "HTML" view. Once you're logged in, Asterisk stores a cookie on your browser (valid for the length of httptimeout) which is used to connect to the same session.

*   http://localhost:8088/rawman?action=status

Assuming you've already logged into manager, this URI will give you a "raw" manager output for the "status" command.

*   http://localhost:8088/mxml?action=status

This will give you the same status view but represented as AJAX data, theoretically compatible with RICO ([http://www.openrico.org](http://www.openrico.org)).

*   http://localhost:8088/static/ajamdemo.html

If you have enabled static content support and have done a make install, Asterisk will serve up a demo page which presents a live, but very basic, "astman" like interface. You can login with your username/secret for manager and have a basic view of channels as well as transfer and hangup calls. It's only tested in Firefox, but could probably be made to run in other browsers as well.

A sample library (astman.js) is included to help ease the creation of manager HTML interfaces.

!!! note \*\* For the demo, there is no need for \*\*any external web server.


```coffeescript
# Login
$LOGIN = curl.exe -i -X GET "http://localhost:8088/asterisk/manager?action=login&username=admin&secret=12345"

# Extraer cookie mansession_id
$COOKIE = ($LOGIN | Select-String 'mansession_id=([^;]+)' | % { $_.Matches[0].Groups[1].Value })

Write-Host "Cookie encontrada: $COOKIE"

# Subir archivo
curl.exe -v -X POST "http://192.168.1.3:8088/asterisk/recordings" `
            -H "Cookie: mansession_id=$COOKIE" `
            -F "file=@C:\var\local\auditorai\wav\exten-113-3004579622-20250802-120405-1754153905.5203765.wav" `
            -F "filename=exten-113-3004579622-20250802-120405-1754153905.5203765.wav"
```
