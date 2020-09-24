/* Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

package com.baidu.paddle.liteeeeee;

/**
 * Tensor class provides the Java APIs that users can get or set the shape or
 * the data of a Tensor.
 */
public class Tensor {

    /**
     * Java doesn't have pointer. To maintain the life cycle of underneath C++
     * PaddlePredictor object, we use a long value to maintain it.
     */
    private long cppTensorPointer;

    /**
     * Is this tensor read-only. This field is also used at C++ side to know whether
     * we should interpret the C++ tensor pointer to "Tensor" pointer or "const
     * Tensor" pointer.
     */
    private boolean readOnly;


    /** Deletes C++ Tensor pointer when Java Tensor object is destroyed */
    protected void finalize() throws Throwable {
        if (cppTensorPointer != 0L) {
            deleteCppTensor(cppTensorPointer);
            cppTensorPointer = 0L;
        }
        super.finalize();
    }

    /**
     * @return whether this Tensor is read-only.
     */
    public boolean isReadOnly() {
        return readOnly;
    }

    /**
     * Resizes the tensor shape.
     *
     * @param dims long array of shape.
     * @return true if resize successfully.
     */
    public boolean resize(long[] dims) {
        if (readOnly) {
            return false;
        }
        return nativeResize(dims);
    }

    /**
     * Set the tensor float data.
     *
     * @param buf the float array buffer which will be copied into tensor.
     * @return true if set data successfully.
     */
    public boolean setData(float[] buf) {
        if (readOnly) {
            return false;
        }
        return nativeSetData(buf);
    }

    /**
     * Set the tensor byte data.
     *
     * @param buf the byte array buffer which will be copied into tensor.
     * @return true if set data successfully.
     */
    public boolean setData(byte[] buf) {
        if (readOnly) {
            return false;
        }
        return nativeSetData(buf);
    }

    /**
     * Set the tensor int data.
     *
     * @param buf the int array buffer which will be copied into tensor.
     * @return true if set data successfully.
     */
    public boolean setData(int[] buf) {
        if (readOnly) {
            return false;
        }
        return nativeSetData(buf);
    }

    /**
     * @return shape of the tensor as long array.
     */
    public native long[] shape();

    /**
     * @return the tensor data as float array.
     */
    public native float[] getFloatData();

    /**
     * @return the tensor data as byte array.
     */
    public native byte[] getByteData();

    /**
     * @return the tensor data as int array.
     */
    public native int[] getIntData();

    private native boolean nativeResize(long[] dims);

    private native boolean nativeSetData(float[] buf);

    private native boolean nativeSetData(byte[] buf);

    private native boolean nativeSetData(int[] buf);

    /**
     * Delete C++ Tenor object pointed by the input pointer, which is presented by a
     * long value.
     * 
     * @param nativePointer a long value which is reinterpret_cast of the C++
     *                      pointer.
     * @return true if deletion success.
     */
    private native boolean deleteCppTensor(long nativePointer);

    public native void feedInputData(long serviceId, float[] inputData, int inputBatch, int inputChannel, int inputHeight, int inputWidth, int inputGraphId);
    public native void feedInputData(long serviceId, byte[] inputData, int inputBatch, int inputChannel, int inputHeight, int inputWidth, int inputGraphId);
    public native void feedInputData(long serviceId, int[] inputData, int inputBatch, int inputChannel, int inputHeight, int inputWidth, int inputGraphId);
    public native void feedInputData(long serviceId, long[] inputData, int inputBatch, int inputChannel, int inputHeight, int inputWidth, int inputGraphId);
    
    // Signature: ()V
    public native void f();

    // Signature: (ID)I
    public native int f(int a, double b);

    // Signature: (Ljava/lang/Object;Ljava/lang/String;)V
    public native void f(Object a, String b);

    // Signature: ()V
    public native void g();
}
