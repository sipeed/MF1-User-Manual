# MF1模块二次开发说明

### 如果有任何的需求或者BUG,请发邮件至 **<support@sipeed.com>**

### `SDK`中只包含固件代码，模型文件需要另外生成（出厂已烧录），具体请邮件联系我们

## 目录


## 工程目录说明

[**SDK**](https://github.com/sipeed/MF1_SDK) 下载连接，**工具链** [下载链接](https://github.com/kendryte/kendryte-gnu-toolchain/releases)


```
assets                             图片文件
components                         SDK组件
├── boards                         不同板子配置
├── drivers
│   ├── camera                     摄像头驱动
│   ├── lcd                        屏幕驱动
│   ├── mem_macro
│   └── sd_card                    SD卡驱动
├── kendryte_sdk
│   └── kendryte-standalone-sdk    K210SDK
├── third_party
│   └── oofatfs                    文件系统
└── utils
    ├── base64                     base64编解码
    ├── cJSON                      cJSON
    ├── cQueue                     队列
    ├── image_op                   图像操作
    ├── jpeg_decode                jpeg解码
    ├── jpeg_encode                jpeg编码
    └── list                       链表
projects                           工程目录
├── hello_world                    helloword
└── MF1
    ├── build                      编译生成的固件在这个目录
    ├── compile                    工程编译配置
    ├── main                       工程目录
        ├── audio                  语音播放
        ├── blur_detect            模糊检测
        ├── face_lib               人脸识别库
        ├── network                网络驱动，ESP8285及W5500
        ├── src                    主函数
        ├── uart_recv              串口驱动
        └── ui                     图片
tools                              SDK编译相关的工具
```

## 工程编译

> 建议使用`Ubuntu`或其他`Linux`发行版进行编译，本工程并未在`Kendryte-IDE`中验证过

参考工程目录下的README进行编译

## 下载固件

<center class="half">
<img src="assets/kflash_gui.jpg" height = 50% width = 80% />
</center>

用户可以使用 `kflash_gui` 来下载程序

具体流程为：

- ① 打开需要烧录的固件，

  如果是`bin`文件，请确保地址为`0x00`,

  是`kfpkg`文件时，不需要选择地址

- ② 选择开发板型号，`MF1`模块请选择`Sipeed Maix Bit With Mic`

- ③ 选择串口，`MF1`模块，请选择第一个串口

- ④ 点击`下载`，开始下载

## 升级 `ESP8285` 固件

现在(2019.08.14之前) `esp8285` 出厂默认烧录的是 `AT` 固件，在 `MF1` 中使用的是 `SPI` 与模块进行通信，所以需要更新一下固件。

**更新 `esp8285` 固件，需要将使能引脚打开，烧录[预编译好的固件](http://dl.sipeed.com/MAIX/HDK/factory_firmware/Ai_Module_MF1_lib_wifi_on.bin)来使能`wifi`**

<center class="half">
<img src="assets/update_esp8285.jpg" height = 50% width = 50% />
</center>

①：短接这个触点到`GND`然后上电

②：使用这个串口进行`esp82825`的固件更新

`esp8285 SPI`固件[下载地址](http://dl.sipeed.com/MAIX/HDK/factory_firmware/esp8266/WiFiSPIESP.ino.esp8285_40M_freq_1M_DOUT.bin)

`flash_download_tools`[下载地址](https://www.espressif.com/zh-hans/support/download/other-tools)

`flash_download_tools`下载选项

<center class="half">
<img src="assets/flash_download_tools.png" height = 50% width = 60% />
</center>

〇：注意选择`ESP8285`下载，**千万不要**选择`ESP8266`

①：选择之前下载的固件，地址为`0`

②：选择晶振频率为`40M`

③：选择`flash`频率为`40M`

④：选择`flash`大小为`8Mbit`

⑤：选择对应的串口，**波特率建议选择为115200**

⑥：点击开始下载

## 代码解释

有问题请发邮件到`support@sipeed.com`
