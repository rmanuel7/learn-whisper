<small>`Version: 4.1`</small>
# Installing RabbitMQ

### Installation Guides
Linux, BSD, UNIX: [Debian, Ubuntu](https://www.rabbitmq.com/docs/install-debian)  

## Installing on Debian and Ubuntu

### Apt with Team RabbitMQ's Repositories: a Quick Start Script
Below is a shell snippet that performs the steps explained in this guide. It provisions RabbitMQ and Erlang from a Team RabbitMQ-hosted apt repository.

> [!IMPORTANT]
> This repository only provides `amd64` (`x86-64`) Erlang packages. For `arm64` (`aarch64`), this script must be modified to provision a supported Erlang series from Launchpad.


<small>`Ubuntu 24.04`</small>
```bash
#!/bin/sh

sudo apt-get install curl gnupg apt-transport-https -y

## Team RabbitMQ's signing key
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null

## Add apt repositories maintained by Team RabbitMQ
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Modern Erlang/OTP releases
##
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-erlang/ubuntu/noble noble main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-erlang/ubuntu/noble noble main

## Latest RabbitMQ releases
##
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-server/ubuntu/noble noble main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-server/ubuntu/noble noble main
EOF

## Update package indices
sudo apt-get update -y

## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```

### Create the script file

It opens a file named `setup-rabbitmq.sh` for editing. If the file does not exist, `vim` `**will create it**. The purpose of this step is to write or modify the installation commands that will be executed later. 

```bash
sudo vim setup-rabbitmq.sh
```

### Make the script executable 

The `+x` option adds the **"execute" permission** to the file. This is a crucial step that tells the operating system that `setup-rabbitmq.sh` is a script that can be run, not just a plain text file. 

```bash
sudo chmod +x setup-rabbitmq.sh
```

### Run the script

The `./` prefix is necessary to tell the shell to look for the script in the current directory, preventing it from confusing your script with a system command. The script will then run all the commands inside it, with administrative privileges granted by the initial `sudo` command. 

```bash
./setup-rabbitmq.sh
```

<br/>

## [Configuring RabbitMQ](https://www.rabbitmq.com/docs/configure)

### [Plugins](https://www.rabbitmq.com/docs/plugins)

Plugins are activated when a node is started or at runtime when a CLI tool is used. For a plugin to be activated at boot, it must be enabled. To enable a plugin, use the rabbitmq-plugins:

```bash
sudo rabbitmq-plugins enable <plugin-name>
```

A list of plugins available locally (in the node's plugins directory) as well as their status (enabled or disabled) can be obtained using rabbitmq-plugins list:

```bash
sudo rabbitmq-plugins list
```

### [Configuration File(s)](https://www.rabbitmq.com/docs/configure#configuration-files)

#### The Main Configuration File, `rabbitmq.conf`

The configuration file `rabbitmq.conf` allows the RabbitMQ server and plugins to be configured.

> [!NOTE]
> The RabbitMQ server source repository contains an example `rabbitmq.conf` file named [rabbitmq.conf.example](https://raw.githubusercontent.com/rabbitmq/rabbitmq-server/v4.1.4/deps/rabbit/docs/rabbitmq.conf.example).

```bash
user@server:~$ sudo systemctl status rabbitmq-server
● rabbitmq-server.service - RabbitMQ broker
     Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; ✅ enabled; preset: ✅ enabled)
     Active: ✅ active (running) since Fri 2025-10-10 21:21:53 UTC; 1min 29s ago
   Main PID: 13785 (beam.smp)
      Tasks: 60 (limit: 18890)
     Memory: 100.5M (peak: 127.2M)
        CPU: 1.578s
     CGroup: /system.slice/rabbitmq-server.service
             ├─13785 /usr/lib/erlang/erts-15.2.7.1/bin/beam.smp -W w -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs 512 -MMmcs 30 -pc unicode -P 1048576 -t 5000000 -stbt db -zdbbl 128000 -sbwt none -sbwtdcpu none -sbwtdio none -- ->
             ├─13795 erl_child_setup 32768
             ├─13850 /usr/lib/erlang/erts-15.2.7.1/bin/inet_gethost 4
             ├─13851 /usr/lib/erlang/erts-15.2.7.1/bin/inet_gethost 4
             └─13854 /bin/sh -s rabbit_disk_monitor

Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Doc guides:  https://www.rabbitmq.com/docs
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Support:     https://www.rabbitmq.com/docs/contact
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Tutorials:   https://www.rabbitmq.com/tutorials
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Monitoring:  https://www.rabbitmq.com/docs/monitoring
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Upgrading:   https://www.rabbitmq.com/docs/upgrade
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Logs: /var/log/rabbitmq/rabbit@reincar.log
Oct 10 21:21:53 reincar rabbitmq-server[13785]:         <stdout>
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Config file(s): (none) 💡
Oct 10 21:21:53 reincar rabbitmq-server[13785]:   Starting broker... completed with 0 plugins.
Oct 10 21:21:53 reincar systemd[1]: Started rabbitmq-server.service - RabbitMQ broker.
```

### Create the Config file(s)

It opens a file named `rabbitmq.conf` for editing. If the file does not exist, `vim` `**will create it**.

```bash
sudo vim /etc/rabbitmq/rabbitmq.conf
```

```bash
user@server:~$ sudo systemctl restart rabbitmq-server
```

```bash
user@server:~$ sudo systemctl status rabbitmq-server
● rabbitmq-server.service - RabbitMQ broker
     Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; ✅ enabled; preset: ✅ enabled)
     Active: ✅ active (running) since Fri 2025-10-10 22:00:31 UTC; 9s ago
   Main PID: 14587 (beam.smp)
      Tasks: 60 (limit: 18890)
     Memory: 122.9M (peak: 144.5M)
        CPU: 1.474s
     CGroup: /system.slice/rabbitmq-server.service
             ├─14587 /usr/lib/erlang/erts-15.2.7.1/bin/beam.smp -W w -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs 512 -MMmcs 30 -pc unicode -P 1048576 -t 5000000 -stbt db -zdbbl 128000 -sbwt none -sbwtdcpu none -sbwtdio none -- ->
             ├─14599 erl_child_setup 32768
             ├─14654 /usr/lib/erlang/erts-15.2.7.1/bin/inet_gethost 4
             ├─14655 /usr/lib/erlang/erts-15.2.7.1/bin/inet_gethost 4
             └─14658 /bin/sh -s rabbit_disk_monitor

Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Doc guides:  https://www.rabbitmq.com/docs
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Support:     https://www.rabbitmq.com/docs/contact
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Tutorials:   https://www.rabbitmq.com/tutorials
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Monitoring:  https://www.rabbitmq.com/docs/monitoring
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Upgrading:   https://www.rabbitmq.com/docs/upgrade
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Logs: /var/log/rabbitmq/rabbit@reincar.log
Oct 10 22:00:31 reincar rabbitmq-server[14587]:         <stdout>
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Config file(s): /etc/rabbitmq/rabbitmq.conf ✅
Oct 10 22:00:31 reincar rabbitmq-server[14587]:   Starting broker... completed with 3 plugins.
Oct 10 22:00:31 reincar systemd[1]: Started rabbitmq-server.service - RabbitMQ broker.
```
