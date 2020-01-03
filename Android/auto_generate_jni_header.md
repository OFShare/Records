# auto generate jni header

Program: **javah**

Arguments: **-classpath /home/acui/Android/Sdk/platforms/android-28/android.jar:$ModuleFileDir$/src/main/java -jni -d $ModuleFileDir$/src/main/cpp $FileClass$**

Working directory: None

**Notice**: -classpath you should change it to your own.

Finally you could go to the XXX.java file where difine native methods. **right click---->External Tools---->javah**