# CSE5914
CSE 5914 Repository

to get the docker image:
<br>
```docker pull schlys/5914-project:flask-app```

to run docker container from wsl:
<br>
```docker run -t -i -p 5000:5000 -e "PULSE_SERVER=${PULSE_SERVER}" -v /mnt/wslg/:/mnt/wslg/ flask-app```

to run docker container from mac/linux
<br>
```docker run -t -i -p 5000:5000 --device /dev/snd flask-app```