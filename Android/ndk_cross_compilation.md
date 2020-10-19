### 使用ndk编译jni代码

- 一般有两种方式`ndk-build`(Android.mk), `cmake`(CMakeLists.txt), 现在基本都是用cmake的方式

- 命令行构建编译

  - 在 Gradle 之外使用 CMake 进行构建时，`工具链文件本身`(即$ANDROID_NDK/build/cmake/android.toolchain.cmake文件)及其参数必须传递给 CMake

   ```shell
  export ANDROID_CMAKE=/Users/acui/Library/Android/sdk/cmake/3.6.4111459/bin/cmake
  export ANDROID_NDK=/Users/acui/Library/Android/sdk/ndk/android-ndk-r16b
  
  # get absolute path
  work_path=$(cd `dirname $0`; pwd)
  echo "work_path:$work_path"
  
  cd $work_path
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
  	-DANDROID_NATIVE_API_LEVEL=android-19
  	
  make -j4
   ```

  - 工具链参数

    - `ANDROID_ABI`: armeabi-v7a / arm64-v8a / armeabi-v7a with NEON / x86 / x86_64
    - `ANDROID_ARM_NEON`: 为 armeabi-v7a 启用或停用 NEON。对其他 ABI 没有影响。对于 API 级别（`minSdkVersion` 或 `ANDROID_PLATFORM`）23 或更高级别，默认为 true，否则为 false。
    - `ANDROID_NATIVE_API_LEVEL`: 是`ANDROID_PLATFORM`的别名(此值默认为所使用的 NDK 支持的最低 API 级别. 例如，对于 NDK r20，此值默认为 API 级别 16)
    - `ANDROID_STL`: c++\_static / c++\_shared / gnustl\_static / gnustl_shared / stlport\_static / stlport_shared, 一般默认情况下将使用 `c++_static`
    - `ANDROID_TOOLCHAIN_NAME`: llvm / arm-linux-androideabi-4.9 / aarch64-linux-android-4.9 / ...
    - `ANDROID_TOOLCHAIN`: clang / gcc, 一般clang和llvm配对
    - 工具链的参数都可以在这个文件里看到$NDK/build/cmake/android.toolchain.cmake

  - 了解CMake构建命令

    - 在调试 CMake 构建问题时，了解 Gradle 在为 Android 交叉编译时使用的具体构建参数会很有帮助。

    - Android Gradle 插件会将用于为每个 ABI 和[构建类型](https://developer.android.google.cn/studio/build/build-variants?hl=zh-cn)执行 CMake 构建的构建参数保存至 `cmake_build_command.txt`。这些文件位于以下目录中, (较旧版本的 Android Gradle 插件会将这些文件放入 .externalNativeBuild 目录，而不是 .cxx 目录)

      ```shell
      <project-root>/<module-root>/.cxx/cmake/<build-type>/<ABI>/
      ```

  - NDK 支持多种 C++ 运行时库, 每个应用一个 STL, "虽然我们努力保持 NDK 各个版本 ABI 的兼容性，但这并非总能实现。为了获得最佳的兼容性，您除了要使用与依赖项相同的 STL，还需尽可能使用相同版本的 NDK。"

  - 启用c++异常: -fexceptions, 启用 RTTI: -frtti

  - [Android NDK APP_STL gnustl_shared is no longer supported](https://stackoverflow.com/questions/52475177/android-ndk-app-stl-gnustl-shared-is-no-longer-supported)

  

- android studio里gradle构建编译, [ExternalNativeCmakeOptions](https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.ExternalNativeCmakeOptions.html)

  - `abiFilters`: Specifies the Application Binary Interfaces (ABI) that Gradle should build outputs for. The ABIs that Gradle packages into your APK are determined by NdkOptions.abiFilter()
  - `arguments`: Specifies arguments for CMake.
  - `cFlags`: Specifies flags for the C compiler.
  - `cppFlags`: Specifies flags for the C++ compiler.
  - `targets`: Specifies the library and executable targets from your CMake project that Gradle should build. If you don't configure this property, Gradle builds all executables and shared object libraries that you define in your CMake project. However, by default, Gradle packages only the shared libraries in your APK.

  ```groovy
  android {
      // Similar to other properties in the defaultConfig block, you can override
      // these properties for each product flavor in your build configuration.
      defaultConfig {
        	minSdkVersion 19
          targetSdkVersion 26
          
          externalNativeBuild {
              cmake {
                	// Passes optional arguments to CMake.
                  arguments "-DANDROID_ARM_NEON=TRUE", "-DANDROID_TOOLCHAIN=clang", "-DANDROID_STL=c++_shared"
                  
                  // Sets an optional flag for the C compiler.
                  cFlags "-D__STDC_FORMAT_MACROS"
                    
                  // Sets optional flags for the C++ compiler.
                  cppFlags "-std=c++11", "-fexceptions", "-frtti"
                    
                  // The following tells Gradle to build only the "libexample-one.so" and
                  // "my-executible-two" targets from the linked CMake project. If you don't
                  // configure this property, Gradle builds all executables and shared object
                  // libraries that you define in your CMake project. However, Gradle packages
                  // only shared libraries into your APK.
                  targets "libexample-one",
                          // You need to specify this executable and its sources in your
                          // CMakeLists.txt using the add_executable() CMake command. However,
                          // building executables from your native sources is optional, and
                          // building native libraries to package into your APK satisfies most
                          // project requirements.
                          "my-executible-demo"
              }
          }
        
        ndk {
              abiFilters 'armeabi', 'armeabi-v7a', 'arm64-v8a'
        }
      }
    
    	externalNativeBuild {
          cmake {
              path "CMakeLists.txt"
          }
      }
  }
  ```

  

- 通读/熟读[官方NDK文档](https://developer.android.google.cn/ndk/guides?hl=zh-cn), 其中[CMake](https://developer.android.google.cn/ndk/guides/cmake?hl=zh-cn#variables), [C++支持](https://developer.android.google.cn/ndk/guides/cpp-support?hl=zh-cn)这两部分部分更需要熟读

