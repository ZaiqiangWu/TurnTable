## How to use

### Step 0

Install Anaconda if it is not installed on your machine.

```
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
```

### Step 1
Run the following command to create the environment.
```
conda create -n turntable python=3.8
conda activate turntable
pip install git+https://github.com/ROBOTIS-GIT/DynamixelSDK.git#subdirectory=python

```


### Step 2

Connect the turntable to your PC. Get the serial port name of the motor. For Linux, the device name is under `/dev/`, and it probably looks like `/dev/ttyUSB0`. Then you need to change the `DEVICE_NAME` in line 5 of file `turntable_test.py`.

Then run this command:
```
sudo chmod a+rw /dev/ttyUSB0
```

### Step 3

```
python turntable_test.py
```