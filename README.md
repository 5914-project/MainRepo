[![Contributors][contributors-shield]][contributors-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



## About the Project



## Getting Started



## Usage



## Contact



## Acknowledgments
<br>

to get the docker image:
<br>
```sh
docker pull schlys/5914-project:latest
```

to run docker container from wsl:
<br>
```sh
docker run -t -i -p 5000:5000 -e "PULSE_SERVER=${PULSE_SERVER}" -v /mnt/wslg/:/mnt/wslg/ schlys/5914-project:latest
```

to run docker container from mac/linux
<br>
```sh
docker run -t -i -p 5000:5000 --device /dev/snd schlys/5914-project:latest
```