#
# Created by OFShare on 2019-11-01
#

#!/bin/bash

# some issue reference
# https://answers.opencv.org/question/174456/about-build-opencv_contribute-fatal-error-boostdesc_bgmi-and-vgg/

# turn off graphical
# sudo systemctl set-default multi-user.target
# sudo reboot

# turn on graphical
# sudo systemctl set-default graphical.target
# sudo reboot

echo "** Install requirement"
sudo apt-get update
sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install -y python2.7-dev python3.6-dev python-dev python-numpy python3-numpy
sudo apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install -y libv4l-dev v4l-utils qv4l2 v4l2ucp
sudo apt-get install -y curl
sudo apt-get update
 
folder="CV"
echo "** Download opencv-4.1.0"
cd $folder
curl -L https://github.com/opencv/opencv/archive/4.1.0.zip -o opencv-4.1.0.zip
curl -L https://github.com/opencv/opencv_contrib/archive/4.1.0.zip -o opencv_contrib-4.1.0.zip
unzip opencv-4.1.0.zip 
unzip opencv_contrib-4.1.0.zip 
cd opencv-4.1.0/

echo "** Building..."
mkdir release
cd release/
cmake \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=./ \
  -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.1.0/modules \
  -D CUDA_ARCH_BIN=5.3 \
  -D CUDA_ARCH_PTX="" \
  -D WITH_CUDA=ON \
  -D WITH_TBB=ON \
  -D BUILD_opencv_python3=ON \
  -D BUILD_opencv_python2=ON \
  -D BUILD_TESTS=OFF \
  -D BUILD_PERF_TESTS=OFF \
  -D WITH_V4L=ON \
  -D BUILD_EXAMPLES=OFF \
  -D WITH_OPENGL=ON \
  -D ENABLE_FAST_MATH=1 \
  -D CUDA_FAST_MATH=1 \
  -D WITH_CUBLAS=1 \
  -D WITH_NVCUVID=ON \
  -D WITH_GSTREAMER=ON \
  -D WITH_OPENCL=YES \
  -D BUILD_opencv_cudacodec=OFF ..
make -j2
sudo make install
echo "** Install opencv-4.1.0 successfully"
echo "** Bye :)"
