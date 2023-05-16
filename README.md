# Sichere Implementierungen auf Mikrocontrollern (WS 2022/2023)

## Installation and Setup

### Prerequisites

- VSCode
- VSCode Extensions: Python, Jupyter
- Git
- Python >=3.9

### Installation of ChipWhisperer

#### Windows

1. Download latest version of ChipWhisperer Setup from
   [https://github.com/newaetech/chipwhisperer/releases](https://github.com/newaetech/chipwhisperer/releases).
2. Install. Recommended Installation folder: `C:\cw`.
3. Update git repository

   ```batch
   cd C:\cw\cw\home\portable\chipwhisperer
   git pull
   ```

#### Unix like OS

1. Clone ChipWhisperer repository somewhere
   (In the following we will assume that the location is `~/work/chipwhisperer`):

   ```sh
   cd ~/work/
   git clone --branch develop https://github.com/newaetech/chipwhisperer.git
   cd chipwhisperer
   git submodule update --init jupyter
   ```

2. Install required packages. Here as example for a Debian based OS:

   ```sh
   sudo apt install libusb-dev make avr-libc gcc-avr gcc-arm-none-eabi
   ```

3. Adjust udev rules and allow user to access serial interfaces:

   ```sh
   sudo cp ~/work/chipwhisperer/hardware/50-newae.rules /etc/udev/rules.d/50-newae.rules
   sudo udevadm control --reload-rules
   sudo usermod -aG dialout $USER
   sudo usermod -aG plugdev $USER
   ```

### Installation of required Python packages

1. Clone this repository somewhere
   (In the following we will assume that the location is `~/work/ws2223/securec_ws2223`):

   ```sh
   cd ~/work/ws2223
   git clone https://github.com/hackenbergstefan/securec_ws2223.git
   ```

2. Create virtual environment:

   ```sh
   cd ~/work/ws2223
   python -m venv venv
   # On Unix like:
   . venv/bin/activate
   # On Windows:
   venv/Scripts/activate
   ```

3. Install packages:

   ```sh
   (venv)$ pip install -r requirements.txt
   # On Unix like:
   (venv)$ pip install -e ~/work/chipwhisperer
   # On Windows:
   (venv)$ pip install -e C:\cw\cw\home\portable\chipwhisperer
   ```

### Adjust environment variables

Create a file `.env` inside the repository with the following content:

Windows:

```env
# C:\work\ws2223\securec_ws2223\.env
PATH=C:\cw\cw\usr\bin;C:\cw\cw\home\portable\armgcc\bin;C:\cw\cw\home\portable\avrgcc\bin;$env["PATH"]
PYTHONPATH=C:\work\ws2223\securec_ws2223
FIRMWAREPATH=C:\cw\cw\home\portable\chipwhisperer\hardware\victims\firmware
```

Unix like (Assume your username is `stefan`):

```env
# /home/stefan/work/ws2223/securec_ws2223/.env
PATH=/home/stefan/work/chipwhisperer;$env["PATH"]
PYTHONPATH=/home/stefan/work/ws2223/securec_ws2223
FIRMWAREPATH=/home/stefan/work/chipwhisperer/hardware/victims/firmware
```

Reload VSCode (`Ctrl+Shift+P -> "Developer: Reload Window"`)

### Test setup

1. Open repository folder with VSCode
   VSCode should have recognized your virtual environment
2. Inside VSCode open [./lecture_0/test_setup.ipynb](./lecture_0/test_setup.ipynb)
3. Select kernel from virtual environment
4. Run cells step by step
