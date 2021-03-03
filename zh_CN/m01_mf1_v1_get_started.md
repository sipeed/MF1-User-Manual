# `MF1`模块快速上手说明

- [`MF1` 模块快速上手说明](#MF1模块快速上手说明)
  - [安装驱动](#安装驱动)
  - [下载固件](#下载固件)
  - [人脸录入与删除](#人脸录入与删除)
  - [串口通信协议](#串口通信协议)

<div STYLE="page-break-after: always;"></div>

## 安装驱动

`MF1` 模块板载一颗 `CH552`，使用串口功能需要安装 `FT2232` 驱动

用户可在  [**FTDI官网**](https://www.ftdichip.com/Drivers/VCP.htm)  下载驱动，请选择对应自己电脑操作系统的安装包

具体的安装方法请参照  [**说明**](https://www.ftdichip.com/Support/Documents/InstallGuides.htm)，  在文档中清楚的写出了安装驱动的过程，请仔细阅读文档

部分系统安装之后，可能无法看到第二个串口

打开设备管理器，找到第二个串口，右键选择 `属性` ，选择使能`VCP`，重新拔插设备即可看到串口出现

<div STYLE="page-break-after: always;"></div>

## 下载固件

<center class="half">
<img src="../assets/kflash_gui.png" height = 50% width = 80% />
</center>

用户可以使用 [`kflash_gui` (https://github.com/sipeed/kflash_gui/releases)](https://github.com/sipeed/kflash_gui/releases) 来下载程序

具体流程为：

- ① 打开需要烧录的固件，如果是 `bin` 文件，请确保地址为 `0x00` ,是 `kfpkg` 文件时，不需要选择地址

- ② 选择开发板型号，`MF1` 模块请选择 `Sipeed MaixDuino`

- ③ 选择串口，`MF1` 模块，请选择第一个串口()

- ④ 点击 `下载`，开始下载

<div STYLE="page-break-after: always;"></div>

## 人脸录入与删除

<center class="half">
<img src="../assets/touch_key.png" height = 50% width = 80% />
</center>

板载了一个触摸按键，焊接有一根弹簧

请将人脸充满 `LCD` 的预览画面，在人脸框出红框之后，轻触弹簧按键，此时就可以录入人脸。

长按按键，即可删除所有存储的人脸信息，以及恢复默认的配置信息。

<div STYLE="page-break-after: always;"></div>

## 串口通信协议

[`MF1` V2 模块简明用户手册](../zh_CN/m02_mf1_v2_get_started.md)
