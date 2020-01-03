# author: OFShare
# date: Apr 26 10:27:56 CST 2019

adb push models/benchmark_model_arm32 /data/local/tmp
adb push models/benchmark_model_arm64 /data/local/tmp
adb shell chmod +x /data/local/tmp/benchmark_model_arm32
adb shell chmod +x /data/local/tmp/benchmark_model_arm64
adb push models/mobilenet_quant_v1_224.tflite /data/local/tmp
#adb shell /data/local/tmp/benchmark_model_arm32 \
#  --graph=/data/local/tmp/mobilenet_quant_v1_224.tflite \
#  --num_threads=4 \
#  --warmup_runs=1 \
#  --num_runs=50 \
#  --run_delay=-1 \
#  --use_nnapi=true \
#  --use_legacy_nnapi=true \
#  --use_gpu=true
echo '\n\n********************************************\n\n'
adb shell /data/local/tmp/benchmark_model_arm64 \
  --graph=/data/local/tmp/mobilenet_quant_v1_224.tflite \
  --num_threads=4 \
  --warmup_runs=1 \
  --num_runs=50 \
  --run_delay=-1 \
  --use_nnapi=true \
  --use_legacy_nnapi=true \
  --use_gpu=true
# reference: https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/tools/benchmark#reducing-variance-between-runs-on-android

