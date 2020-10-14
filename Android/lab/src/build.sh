#!/bin/bash
#
# Created by OFShare@outlook.com on 2020-10-14
#

export ANDROID_NDK=/Users/acui/Library/Android/sdk/ndk/android-ndk-r16b

work_path=$(dirname $0)
cd $work_path
rm -rf android_release_v8a
mkdir android_release_v8a
cd android_release_v8a

cmake .. \
	-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
	-DANDROID_TOOLCHAIN_NAME=llvm \
	-DANDROID_TOOLCHAIN=clang \
	-DCMAKE_BUILD_TYPE=Release \
	-DANDROID_ABI="arm64-v8a" \
	-DANDROID_ARM_NEON=ON \
	-DANDROID_STL=c++_shared \
	-DANDROID_NATIVE_API_LEVEL=android-19
	
make -j4
