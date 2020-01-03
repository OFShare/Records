[tag v1.13.1]
bazel build -c opt --cxxopt='--std=c++11' --config=android_arm64   //tensorflow/lite/examples/android:tflite_demo
bazel build -c opt --cxxopt='--std=c++11' --config=android_arm   //tensorflow/lite/examples/android:tflite_demo
