# `MF1` 模块简明用户手册

本文目录：

- [**MF1(V2)** 模块快速上手说明](#MF1_V2\ 模块快速上手说明)
  - [驱动,调试工具下载](#下载&&安装必备软件)
  - [安装 USB 驱动](#下载&&安装必备软件)
- [检查版本固件并更新](#检查版本固件并更新)
- [串口通讯协议](#串口通讯协议)
  - [人脸录入与识别](#人脸录入与识别)

MF1(V2) 人脸识别模块外观一览

<table border="3">
    <tr>
        <th colspan=3>MF1 V2 版</th>
    </tr>
    <tr>
        <td  width="100">描述</td>
        <td>正面视图</td>
        <td>背面视图</td>
    </tr>
    <tr>
        <td  width="100">MF1 1.3寸屏,不带 NAND FLASH</td>
        <td rowspan=2>
            <img src="../assets/mf_module/mf1_front_v2.png" width="600" alt="MF1 正面">
        </td>
        <td>
            <img src="../assets/mf_module/mf1_bottom_v2.png" width="600" alt="MF1 背面视图">
        </td>
    </tr>
    <tr>
        <td>MF1 1.3寸屏,带 NAND FLASH</td>
        <td>
            <img src="../assets/mf_module/mf1_bottom_v2(nand).png" width="600" alt="MF1(NAND Flash) 背面视图">
        </td>
    </tr>
</table>

## 安装驱动

`MF` 模块板载一颗 `CH552`，使用串口功能需要安装 `FT2232` 驱动

用户可在  [**FTDI官网**](https://www.ftdichip.com/Drivers/VCP.htm)  下载驱动，请选择对应自己电脑操作系统的安装包

- USB 驱动: **FT2232** ->[[下载链接点这里](https://dl.sipeed.com/MAIX/tools/ftdi_vcp_driver)](https://dl.sipeed.com/MAIX/tools/ftdi_vcp_driver)

1. 确认设备是否插入，及驱动是否安装

<img src="../assets/get_started/win_drives_1.png" height="500" alt="打开设备管理器">

2. 打开上一节的的链接下载驱动文件
<img src="../assets/get_started/win_drives_2.png" alt="打开设备管理器">

3. 点击安装
<img src="../assets/get_started/win_drives_3.png" alt="安装 FT2232 驱动">

4. 安装完成之后,可以在设备管理器看到已经识别到两个串口设备了(其中只有一个串口可用)

<img src="../assets/get_started/win_drives_4.png" alt="安装 FT2232 驱动">

部分系统安装之后，可能无法看到第二个串口, 打开设备管理器，找到第二个串口，右键选择 `属性` ，选择使能`VCP`，重新拔插设备即可看到串口出现

> FT2232 官方驱动方法，请参照 [**说明**](https://www.ftdichip.com/Support/Documents/InstallGuides.htm)， 在文档中清楚的写出了安装驱动的过程，请仔细阅读文档


## 人脸录入与删除

<center class="half">
<img src="../assets/touch_key.png" height = 50% width = 80% />
</center>

板载了一个触摸按键，焊接有一根弹簧

请将人脸充满 `LCD` 的预览画面，在人脸框出红框之后，轻触弹簧按键，此时就可以录入人脸。

长按按键，即可删除所有存储的人脸信息，以及恢复默认的配置信息。

<div STYLE="page-break-after: always;"></div>
