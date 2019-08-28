# MF1 Module User Manual

- [1. Modify record](#1-Modify-record)
- [2. Hardware Resources Introduction](#2-Hardware-Resources-Introduction)
- [3. Function Introduction](#3-Function-Introduction)
    - [3.1 Module Features](#31-Module-Features)
    - [3.2 Instructions for use](#32-Instructions-for-use)
- [4. Application solution](#4-Application-solution)
    - [4.1 Serial Module](#41-Serial-Module)
    - [4.2 WeChat applet module](#42-WeChat-applet-module)
    - [4.3 Secondary development](#43-Secondary-development)
- [5. Q&A](#5-QA)


## 1. Modify record

|Version|Time|Modify content|
|-|-|-|
|1.0|2019.07.30|Initial Release|


<div STYLE="page-break-after: always;"></div>

## 2. Hardware Resources Introduction

<center class="half">
<img src="./assets/font_bottom.jpg" width = 60% />
</center>

* CPU : RISC-V dual core 64bit, built-in FPU, frequency 400Mhz-500Mhz
* Image recognition: live recognition
* Dual camera: infrared + visible light
* Infrared fill light: 3W infrared light-emitting diode
* Display: 1.33" TFT, resolution 240*320 display
* Other peripherals: capacitive touch button / support 3W speaker / MEMS microphone / SD NAND / RGB LED
* Wireless function (optional): Support 2.4G 802.11.b/g/n, SPI connection

* [Taobao purchase](https://item.taobao.com/item.htm?spm=a1z10.1-c.w4004-21231188695.25.27ba52b1bsusf7&id=599138281058)

<div STYLE="page-break-after: always;"></div>

## 3. Function Introduction

### 3.1 Module Features

|  |  |
|-|-|
|Core live face recognition module, face recognition through dual-spectrum camera, and determine whether it is alive,|  |
|Protected Screen Picture/Video Attack, Color/Black & White Laser/Inkjet Paper Attack |  |
|Suitable for indoor and semi-outdoor (no direct sunlight) environment, common for day/night (dark light environment automatically switches to infrared recognition |  |
|The default lens has a recognition distance of 40~80cm, and the customizable lens can be used for longer distance recognition|  |
| Boot time is about 0.2~0.3s , and the time from power-on to recognition of the first face is 0.4~0.5s | |
|Storing the number of face feature values up to about 10,000, optional SDNAND can store 4K face images |  |
|Face recognition accuracy rate 98% @ 0.001 FA|  |

### 3.2 Instructions for use

|||
|-|-|
|The upper spring of the MF1 module is a touch button, which is entered by the button to delete the record. |  |
| Entry method: The module is being entered into the face, the face is as full as possible on the screen, and when the face is seen by the red frame, press the button shortly, the screen will display the words “Enter Successfully” |  |
| Delete record: long press the button for more than 1s to delete all records |  |
|Identification: Within the recognition distance (40~80cm, basically within the wingspan), the face that has been entered can be quickly identified, and the recognition time of the living body is 0.2~0.3s|  |
|Dark light recognition: When the indoor environment is dark, or at night, the MF1 automatically switches to the infrared recognition mode, which is displayed as a near-infrared face image on the screen. |  |

|||
|-|-|
|The core module can be equipped with different sizes of screens, bottom plates, etc. For detailed configuration, see the selection table of the accessories |

## 4. Application solution

### 4.1 Serial Module

Based on Json's serial communication protocol, the analysis library is provided. For the specific protocol, see [Protocol Document] (MF1 module serial communication protocol.md)

The serial port module is simple to use, users can quickly integrate into their own system, but the degree of freedom is relatively small.

### 4.2 WeChat applet module

Connect to the 8285 via SPI for face entry and record viewing via our WeChat applet

### 4.3 Secondary development

Suitable for users with a good technical foundation, no need to connect to other MCUs, and have higher degrees of freedom for development.

Secondary development of [SDK] (https://github.com/sipeed/MF1_SDK) download link

For a brief description of the secondary development, please refer to [MF1 Module Secondary Development Instructions.md] (MF1 Module Secondary Development Instructions.md)

<div STYLE="page-break-after: always;"></div>

## 5. Q&A

* Q: How to update the firmware

  A: Please refer to [Update MaixPy Firmware](https://maixpy.sipeed.com/zh/get_started/upgrade_firmware.html), select `Sipeed Maix Bit With Mic` in the board selection, when two serial ports appear , select the first serial port

* Q: What should I pay attention to during use?

  A: Hold the USB plug after power-on (to prevent accidental touch of the touch button)

* Q: Power supply mode

  A: The module can be powered by USB5V, or the external backplane uses battery or power supply.
