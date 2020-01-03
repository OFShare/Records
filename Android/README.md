# setup envorinment for Android on Ubuntu

1. if you wanna build from a clean envorinment,you can whole remove the envorinment about Java and Android studio.

    `rm ~/.AndroidStudio`
    
    `rm ~/.android`

    for more details,please reference to these links:

    [How to completely uninstall Java?](https://askubuntu.com/questions/84483/how-to-completely-uninstall-java)

    [Uninstall Android Studio completely](https://askubuntu.com/questions/546723/uninstall-android-studio-completely)
    
2. install Java

    `sudo apt-get install openjdk-8-jre `
    
    `sudo apt-get install openjdk-8-jdk `
    
    for more details,please reference to this link:
    
    [How do I install Java?](https://askubuntu.com/questions/48468/how-do-i-install-java)
    
3. install Android Studio

    you can go to Official website to [download](https://developer.android.com/studio/) this,you better have a good network speed.
    
4. install sdk for Android

    you can through  [SDK Manager](https://developer.android.com/studio/intro/update.html#sdk-manager) to download it
    
5. install opencv-sdk for Android(not necessary)

    you can go to github of opencv [releases](https://github.com/opencv/opencv/releases) to download it

others:

    1.you do not need set JAVA_HOME,JAVA_SDK.
    
    2.what about sdk? like android sdk,opencv sdk and so on. In my opinion,just like cpp's stl,it have already wrote some useful functions that you can easily handle.
    
    3.ndk-bundle you better use version of 16 instead of the latest version of 18.
    
    4.Android-Sdk's cmake you better use version of 3.6.* instead of the latest version of 3.10.*

# adb command

1. `cd Android\Sdk\platform-tools`

2. `.\adb.exe devices`(show devices that what you have connected)

3. `.\adb.exe -s 420B2Q4QHO install -r  C:\Users\xxx\Desktop\appmain-release.apk`

4. `sudo adb kill-server`

5. `sudo adb start-server`

    

