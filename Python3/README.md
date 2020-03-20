1. **virtualenv**

   - `virtualenv --no-site-packages --python=/usr/bin/python3 venv3`

   - `source venv3/bin/activate`

   - `deactivate`

   - ```shell
     vim venv3/bin/activate
     Maybe you would change this:
     	VIRTUAL_ENV="/home/acui/Test/Tmp/venv3"
     to: 
     	VIRTUAL_ENV="$HOME/Test/Tmp/venv3"
     ```

   - ```shell
     pip --version
     pip 19.3.1 from /home/acui/Test/Tmp/venv3/lib/python3.5/site-packages/pip (python 3.5)
     pip is under the site-packages that indicates pip is a packages of python3.5  
     ```

2. python3 `str`  vs `bytes`

   Python 3最重要的新特性之一是对`字符串`和`二进制数据流`做了明确的区分。文本总是`Unicode`，由`str`类型表示，二进制数据则由`bytes`类型表示。

   注意的地方:

   ​    b = b'1234567'

   ​    s = str(b), 此时s为`"b'1234567'"`, 两边加了双引号

   ​	所以, s[2: -1]才是我们想要的实际的数据

   The disadvantage is that encoding the message using `Base64` increases its length. 

   在双方都知道数据的时候, 或许直接把读取的二进制流数据传给对方也是可以的(不考虑加密解密)

3. 

