# PyQt5-Photobooth-App

Photobooth App using PyQt5 and OpenCV

For running the [Docker version](https://github.com/berodimas/pyqt5-photobooth-app/tree/feature/docker-version), you need to configure the GStreamer for OpenCV. Actually you also can configure the GStreamer pipeline to not using the udpsink method.

Run python files:
```
1. Create venv
2. Run pip install -r requirements.txt
3. Run python boomgate.py
```

Docker usage:
```
1. docker build -t berodimas/photobooth-app:1.0 -f Dockerfile .
2. docker-compose up -d
3. gst-launch-1.0 mfvideosrc device-index=1 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000
```
> Notes: Change display Environtment on [docker-compose.yml](https://github.com/berodimas/pyqt5-photobooth-app/blob/feature/docker-version/docker-compose.yml) 
> Change the videosource from gst-launch command based on your device environtment

Tested on:

| Software | Description |
| --- | --- |
| python | 3.7.9 |
| OpenCV | 4.5.2 |
| Gstreamer | 1.18.4 |
| Windows | Windows 10 Pro 64-bit |

