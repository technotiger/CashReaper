# CashReaper

A lightweight docker image running multiple passive income applications. Supports ARM and x86 architectures. 

Highlights:
---
- Works on raspberry pi
- Earn small amount of money (beer money) by sharing for your internet bandwidth
- 100% passive income, set and forget
- No continuous disk writes - particularly helpful for devices using flash storage like raspberry pi
- Only verified services with confirmed payouts
- Automatically claim honeygain lucky pot to maximize passive income.

<br>

# Quick start
1. Make sure `docker` is installed on your system.

2. git clone

```
git clone https://github.com/technotiger/CashReaper.git && cd CashReaper
```

3. Edit the `settings.conf` file using any text editor. Refer the following section for details. For example, to edit using nano:
```
nano settings.conf
```
Save the modified settings file.

4. Build the docker image and run the container. This can take a several minutes.

```
./run.sh
```

<b>Docker Logs: </b>The docker container created by run.sh script will have logs turned off to prevent unnesessary disk activity. You can change this behaviour by editing the run.sh script before executing it. For example, you can delete "```--log-driver none```" from the docker run command in the run.sh script to use the default docker log setting.
<br><br>

<br>

---
# Installed programs

# 1. Honeygain
Register for an account. In the settings file, add your email to `HG_EMAIL` and password to `HG_PASSWORD` and set the `USE_HONEYGAIN` to `y`.
<br><br>Example
```
# Honeygain
USE_HONEYGAIN=y
HG_EMAIL=example@example.com
HG_PASSWORD=MyP@$$W0rd
```
<br><br>
<b>Automatically claim lucky pot</b>
<br>
Honeygain offers additional credits in the form of lucky pot and achievements. Users need to visit their website everyday to claim these credits. You can automate this process by setting `USE_HONEYGAIN_AUTOCLAIM` to `y` in the settings file.

This feature will automatically claim the daily Honeygain lucky pot and available rewards, thereby maximizing your passive earnings.
<br><br>Example
```
USE_HONEYGAIN_AUTOCLAIM=y
```

<br>OPTIONAL: You can optionally specify how often the program checks the website for lucky pot by setting `HG_AUTOCLAIM_INTERVAL` to the desired time interval specified in seconds. This is not required.
<br><br>Example
```
HG_AUTOCLAIM_INTERVAL=12345
```
By default, the program checks the website every 3 hours until the lucky pot becomes available for the day. However, users have the flexibility to define their preferred interval within the range of 600 seconds (equivalent to 10 minutes) to 86400 seconds (equivalent to 24 hours).
<br><br>

# 2. Pawns.app
Register for an account. In the settings file, add your email to `PA_EMAIL` and password to `PA_PASSWORD` and set the `USE_PAWNSAPP` to `y`.
<br><br>Example
```
# Pawns.app
USE_PAWNSAPP=y
PA_EMAIL=example@example.com
PA_PASSWORD=MyP@$$W0rd
```
<br><br>

# 3. Earnapp
Register for an account. Set `USE_EARNAPP` to `y` in the `settings.conf` file.

The run.sh script will print a link that you need to paste into your browser to "link" the worker to your account. This needs to be repeated per container instance.
<br><br>
To get this link manually, you can use the following command.

``` 
docker exec -it cashreaper earnapp register | grep -Eo 'https.+'
```
<br>Example
```
# Earnapp
USE_EARNAPP=y
```
<br><b>Storage: </b>Persistent storage is recommend for Earnapp to ensure that you don't have to repeat the worker-account linking process when container is recreated. If you use the run.sh script, a docker volume named vol-cashreaper will be automatically created and used for this purpose.
<br><br>

# 4. Packet Stream
Register for an account. In the settings file set `USE_PACKET_STREAM` to `y` and `PS_ID` to your CID. To find your CID, navigate to the [download page](https://packetstream.io/dashboard/download) and find the linux/docker instructions. You will find your CID in the setup command listed there - look for CID=xxxx.
<br><br>Example
```
# Packet Stream
USE_PACKET_STREAM=y
PS_ID=ab12
```
<br><br>

# 5. Traffmonetizer
Register for an account. In the settings file, add your `Application Token` to `TRAFF_TOKEN` and set the `USE_TRAFFMONETIZER` to `y`.

You can find the `Application Token` on your [dashboard](https://app.traffmonetizer.com/dashboard).
<br><br>Example
```
# Traffmonetizer
USE_TRAFFMONETIZER=y
TRAFF_TOKEN=ZXhhbXBsZFVYQU1RTEVlaGFtcGxlRVhXTVBMRQo=
```
<br><br>

# 6. Bitping
Register for an account. In the settings file, add your email to `BP_EMAIL` and password to `BP_PASSWORD` and set the `USE_BITPING` to `y`.
<br><br>Example
```
# BitPing
USE_BITPING=y
BP_EMAIL=example@example.com
BP_PASSWORD=MyP@$$W0rd
```
<br><br>

---
# Accounts

You will need an account for each of the following services.
- [Register Honeygain](https://r.honeygain.me/TECHTA09A1)
- [Register Pawns.app](https://pawns.app?r=1358509)
- [Register Earnapp](https://earnapp.com/i/48Bwwfmz)
- [Register Packetstream](https://packetstream.io/?psr=56yi)
- [Register Traffmonetizer](https://traffmonetizer.com/?aff=1160018)
- [Register BitPing](https://app.bitping.com?r=j5mXMC7t)


<br>** Please use these links to support this project at no cost to you. You can receive a joining bonus for using these referral links.

<br>

---

# Credits
This project uses code from the following open-source projects:

<br>PiCash (https://github.com/chashtag/PiCash)
<br>Honeygain Auto Claim (https://github.com/MrLoLf/HoneygainAutoClaim)