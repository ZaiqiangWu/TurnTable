## How to use

### Step 0

Install Anaconda if it is not installed on your machine.

```
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
```

### Step 1
Make sure that you are under the `./PerGarmentVITON`, then run the following command to create the environment.
```
conda create -n turntable python=3.8
conda activate turntable
pip install git+https://github.com/ROBOTIS-GIT/DynamixelSDK.git#subdirectory=DynamixelSDK/python

```


## Install

1. Download the `DynamixelSDK` and install it
    ```bash
    git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
    cd DynamixelSDK/python
    python setup.py install
    ```
    After that, you can check whether it has installed in python:
    ```python
    from dynamixel_sdk import *
    ```

2. Get the serial port name of the motor. For Linux, the device name is under `/dev/`, and it probably looks like `/dev/tty.USB0`. Then you need to change the `DEVICE_NAME` in line 22 of file `XM540.py`.

3. Setup the IPCam's url in line 8 of `test.py`. Then define the data folder in line 25 (You need to create one first otherwise the cv2.imwrite won't recognize the path).

4. Run the `test.py`. 
    - Firstly, you may need to reset the turntable by typing in a single character `R` and then `enter`.
    - Then, you may typing in `O` to start recording.
    
5. If you need to mount the camera and access the storage, you need to
   ```
   ps aux | grep gphoto
   # kill the processes
   
   mkdir /home/toby/camera
   gphotofs /home/toby/camera
   ```

### Kinect Feed 
```bash
 curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add | sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt-get install libk4a1.4 libk4a1.4-dev k4a-tools
 cp Capturing/turntable/99-k4a.rules /etc/udev/rules.d/
 pip install pyk4a
 ```

### RealSense
 ```bash 
 sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE 
 sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u 
+
 sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev librealsense2-dbg 
 ``` 