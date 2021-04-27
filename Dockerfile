FROM ubuntu:18.04

USER root

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install pkg-config -y
RUN apt-get install git -y

RUN apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio -y
RUN apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev -y
RUN apt install gstreamer1.0-tools -y
RUN apt install libgtk-3-dev -y
RUN apt install libgtk2.0-dev -y
RUN apt install libdc1394-22-dev -y

RUN apt-get install -y \
    python3 python3-pyqt5 python3-pip

RUN usermod -a -G audio root
RUN usermod -aG video root

RUN pip3 install --upgrade pip
RUN pip3 install wheel
RUN pip3 install numpy

RUN apt-get install cmake -y

RUN cd \
    && git clone https://github.com/opencv/opencv.git \
    && cd opencv \ 
    && git checkout 4.1.0 \
    && mkdir build \
    && cd build \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_GSTREAMER=ON -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D PYTHON_EXECUTABLE=$(which python3) -D BUILD_opencv_python2=OFF -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -D PYTHON3_EXECUTABLE=$(which python3) -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D BUILD_EXAMPLES=ON .. \
    && make -j$(nproc) \
    && make install \ 
    && ldconfig

RUN pip3 install imutils

WORKDIR "/app"

COPY . .

CMD ["python3", "./App2Run.py"]

# CMD ["python3", "check.py"]