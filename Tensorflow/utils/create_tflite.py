import tensorflow as tf
import glob
from tensorflow.lite.python import lite_constants as constants

# def from_frozen_graph(cls,
#                         graph_def_file,
#                         input_arrays,
#                         output_arrays,
#                         input_shapes=None):
#        converter=tf.lite.TFLiteConverter.from_frozen_graph(pnet_model,["input_image"],["onet_cls_prob","onet_bbox_pred","onet_landmark_pred"],{"input_image" : [1,None,None, 3]})

def runPnet():
        pnet_model='/home/acui/Test2/newmodel/mtcnn_pnet.pb'
        #converter = tf.lite.TFLiteConverter.from_saved_model('/home/acui/Proj/FaceBoxes/export/1547780014/')
        converter=tf.lite.TFLiteConverter.from_frozen_graph(pnet_model,["input_image"],["pnet_cls_prob","pnet_bbox_pred"],{"input_image" : [6, 128, 128, 3]})
        tflite_model=tflite_model = converter.convert()
        open("pnet.tflite", "wb").write(tflite_model)


def runRnet():
        pnet_model='/home/acui/Test2/newmodel/mtcnn_rnet.pb'
        #converter = tf.lite.TFLiteConverter.from_saved_model('/home/acui/Proj/FaceBoxes/export/1547780014/')
        converter=tf.lite.TFLiteConverter.from_frozen_graph(pnet_model,["input_image"],["rnet_cls_prob","rnet_bbox_pred"],{"input_image" : [1, 24,24, 3]})
        tflite_model=tflite_model = converter.convert()
        open("rnet.tflite", "wb").write(tflite_model)


def runONet():
        pnet_model='/home/acui/Test2/newmodel/mtcnn_onet.pb'
        #converter = tf.lite.TFLiteConverter.from_saved_model('/home/acui/Proj/FaceBoxes/export/1547780014/')
        converter=tf.lite.TFLiteConverter.from_frozen_graph(pnet_model,["input_image"],["onet_cls_prob","onet_bbox_pred","onet_landmark_pred"],{"input_image" : [1, 48, 48, 3]})
        tflite_model=tflite_model = converter.convert()
        open("onet.tflite", "wb").write(tflite_model)

def runQuantizedTflite(usingQUANTIZED_UINT8=False):
        pnet_model='/home/acui/Test2/newmodel/mtcnn_pnet.pb'
       # converter = tf.lite.TFLiteConverter.from_saved_model('/home/acui/Proj/FaceBoxes/export/1547780014/')
        converter=tf.lite.TFLiteConverter.from_frozen_graph(pnet_model,["input_image"],["pnet_cls_prob","pnet_bbox_pred"],{"input_image" : [1, 128, 128, 3]})
        converter.post_training_quantize=True
        if(usingQUANTIZED_UINT8):
                converter.inference_input_type=constants.QUANTIZED_UINT8
                converter.quantized_input_stats={'input_image' : (0., 1.)}
        tflite_quantized_model = converter.convert()
        if(usingQUANTIZED_UINT8):
                open("converted_quantized_with_QUANTIZED_UINT8_model.tflite", "wb").write(tflite_quantized_model)
        else:
                open("pnet_quantized_model.tflite", "wb").write(tflite_quantized_model)
if __name__=='__main__':
        # runQuantizedTflite()
        runPnet()
        runRnet()
        runONet()
        runQuantizedTflite(True)
