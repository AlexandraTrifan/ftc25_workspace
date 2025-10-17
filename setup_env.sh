#!/bin/bash

GNURADIO_WORKDIR=/home/analog/gnuradio-upgrade

sudo apt-get remove gnuradio gnuradio-dev --no-install-recommends
sudo apt-get install python3-matplotlib sfce4-screenshooter qtbase5-dev libgmp-dev libgsl27 \
libgslcblas0 libgsm1-dev libjs-mathjax libqt5opengl5 libqt5core5a \
libqt5dbus5 libqt5gui5 libqt5network5 libqt5opengl5 libqt5printsupport5 \
libqt5sql5 libqt5test5 libqt5widgets5 libqt5xml5 libqwt-qt5-6 libsdl1.2debian libsoapysdr0.8 \
libspdlog-dev libspdlog1.10 libthrift-0.17.0 libthrift-dev libts0 libuhd4.3.0 pybind11-dev \
pyqt5-dev-tools pyqt6-dev-tools python3-cffi-backend python3-click python3-click-plugins \
python3-colorama python3-contextlib2 python3-jsonschema python3-mako python3-markupsafe \
python3-opengl python3-py python3-pygccxml python3-pyqt6 python3-pyqt6.sip \
python3-pyqtgraph python3-pyrsistent python3-schema python3-thrift python3-zmq \
qtbase5-dev-tools qtchooser libqwt-qt5-dev libsndfile1-dev

python3 -m pip install 'numpy<2' --break-system-packages

mkdir -p $GNURADIO_WORKDIR

cd $GNURADIO_UPGRADE
git clone https://github.com/analogdevicesinc/libad9361-iio
mkdir libad9361-iio/build
cd libad9361-iio/build
cmake -DCMAKE_BUILD_TYPE=Release ..
make && sudo make install

cd $GNURADIO_UPGRADE
git clone --recursive https://github.com/gnuradio/volk
mkdir -p volk/build
cd volk/build
cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ..
make && make test && sudo make install
sudo ldconfig

cd $GNURADIO_UPGRADE
git clone https://github.com/gnuradio/gnuradio -b v3.10.11.0
mkdir -p gnuradio/build
cd gnuradio/build
cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ..
make && sudo make install
sudo ldconfig

cd /home/analog/Downloads
wget https://github.com/analogdevicesinc/scopy/releases/download/v2.1.0/Scopy-v2.1.0-Linux-arm64-AppImage.zip
unzip ./Scopy-v2.1.0*
sudo mv Scopy-v2.1.0*.AppImage /usr/local/bin/Scopy-v2.0.0-beta-rc2-Linux-arm64.AppImage

cp /usr/local/share/applications/scopy.desktop /home/analog/Desktop/
cp /usr/local/share/applications/gnuradio-grc.desktop /home/analog/Desktop
sudo chmod +x /home/analog/Desktop/scopy.desktop 
sudo chmod +x /home/analog/Desktop/gnuradio-grc.desktop



