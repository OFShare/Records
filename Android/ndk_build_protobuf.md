### 使用ndk编译[protobuf](https://github.com/protocolbuffers/protobuf)

- 下载你想要的[releases](https://github.com/protocolbuffers/protobuf/releases), 如v3.2.0版本
- 修改`cmake/CMakeLists.txt`, 注释167 ~ 179行, 这样就只编译`protobuf-lite`
- 下面的编译脚本在v3.2.0测试且通过

```cmake
#!/bin/bash
#
# Created by OFShare@outlook.com on 2020-08-31
#

export ANDROID_CMAKE=/Users/acui/Library/Android/sdk/cmake/3.6.4111459/bin/cmake
export ANDROID_NDK=/Users/acui/Library/Android/sdk/ndk/android-ndk-r16b

# get absolute path
work_path=$(cd `dirname $0`; pwd)
echo "work_path:$work_path"

# --------------------------
# arm64-va8
# --------------------------
cd $work_path/cmake
rm -rf android_release_v8a
mkdir android_release_v8a
cd android_release_v8a

$ANDROID_CMAKE .. \
 -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
 -DANDROID_TOOLCHAIN_NAME=llvm \
 -DANDROID_TOOLCHAIN=clang \
 -DCMAKE_BUILD_TYPE=Release \
 -DANDROID_ABI="arm64-v8a" \
 -DANDROID_ARM_NEON=ON \
 -DANDROID_STL=c++_shared \
 -DANDROID_NATIVE_API_LEVEL=android-19 \
 -DANDROID_LINKER_FLAGS="-landroid -llog" \
 -DBUILD_SHARED_LIBS=ON \
 -Dprotobuf_BUILD_TESTS=OFF \
 
make -j8
#make install
#exit

# --------------------------
# armeabi-v7a
# --------------------------
cd $work_path/cmake
rm -rf android_release_v7a
mkdir android_release_v7a
cd android_release_v7a

$ANDROID_CMAKE .. \
 -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
 -DANDROID_TOOLCHAIN_NAME=llvm \
 -DANDROID_TOOLCHAIN=clang \
 -DCMAKE_BUILD_TYPE=Release \
 -DANDROID_ABI="armeabi-v7a" \
 -DANDROID_ARM_NEON=ON \
 -DANDROID_STL=c++_shared \
 -DANDROID_NATIVE_API_LEVEL=android-19 \
 -DANDROID_LINKER_FLAGS="-landroid -llog" \
 -DBUILD_SHARED_LIBS=ON \
 -Dprotobuf_BUILD_TESTS=OFF \

make -j8

cd $work_path
rm -rf output
mkdir -p output/arm64-v8a
mkdir -p output/armeabi-v7a
cp -r $work_path/cmake/android_release_v7a/libprotobuf-lite.so output/armeabi-v7a/
cp -r $work_path/cmake/android_release_v8a/libprotobuf-lite.so output/arm64-v8a/

cd $work_path/cmake
rm -rf android_release_v7a
rm -rf android_release_v8a
echo "----------------------------"
echo "Build successfully, enjoy it"
echo "output is here: $work_path/output/"
echo "----------------------------"

```

