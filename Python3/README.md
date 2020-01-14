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

2. 

