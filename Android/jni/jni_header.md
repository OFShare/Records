# auto generate jni header

Program: **javah**

Arguments: **-classpath /home/acui/Android/Sdk/platforms/android-28/android.jar:$ModuleFileDir$/src/main/java -jni -d $ModuleFileDir$/src/main/cpp $FileClass$**

Working directory: None

**Notice**: -classpath you should change it to your own.

Finally you could go to the XXX.java file where difine native methods. **right click---->External Tools---->javah**



jdk-10.0.2发现，这个版本的jdk取消了javah,直接改用javac -h代替了

- `javac Tensor.java -h ./`



