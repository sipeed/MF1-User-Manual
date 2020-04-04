# 基于串口通信的人脸识别模块通信协议 `V2.0.1`

## **修改记录**

| 版本      | 时间         | 修改内容       |
| -------- | ------------ | ------------- |
| `0.1`   | `2019.09.05`  | 协议版本到`2`   |

## 硬件连接

| `K210`  |说明     |
| ------  |----------------------------- |
| `IO5`   | 协议串口的`TX`,可设置, 默认`5`,默认波特率为`115200`  |
| `IO4`   | 协议串口的`RX`,可设置, 默认`4`  |
| `IO11`  | 调试串口的`RX`, 可设置, 默认`11`,默认波特率为`115200`  |
| `IO10`  | 调试串口的`TX`, 可设置, 默认`10`  |
| `IO24`  | 短按录入人脸, 可设置, 默认为`24`<br>(长按清空人脸特征值需烧录特殊固件)  |
| `IO13`  | 继电器常高输出, 可设置, 默认为`13`  |
| `IO12`  | 继电器常低输出, 可设置, 默认为`12`  |

<div STYLE="page-break-after: always;"></div>

## `Json` 基本格式

```json
{"version":$protocol_version,"type":"cmd_type","code":0,"msg":"msg","param":{"xx":"xx","xx":xx}}\r\n
```

#### 说明

- 当前 `protocol_version` 为 `2`

- 数据包结尾必须加 `\r\n`

- 数据包中间不允许有 `\r\n`

> 注意`\r\n`要转义为**0x0D 0x0A**

### `cmd_type`

| `cmd_type`    | 说明  |
| ---------- | ---------- |
| [`init`](#初始化完成) | 模块发送初始化完成消息    |
| [`pkt_prase_failed_ret`](#数据包解析出错信息) | 数据包解析出错信息    |
| [`face_info`](#输出人脸信息) | 识别到人脸后输出人脸信息 |
| [`face_recon`](#设置是否进行人脸识别) | 设置是否进行人脸识别 |
| [`face_recon_ret`](#设置是否进行人脸识别结果) | 设置是否进行人脸识别结果 |
| [`cal_pic_fea`](#计算图片人脸特征值) | 计算`Jpeg`图片中的人脸特征值 |
| [`cal_pic_fea_ret`](#计算图片人脸特征值结果) | 计算`Jpeg`图片中的人脸特征值结果 |
| [`add_user_spec_uid`](#添加用户指定UID) | 添加用户并指定`UID` |
| [`add_user_spec_uid_ret`](#添加用户指定UID结果) | 添加用户并指定`UID`结果 |
| [`add_user_by_fea`](#通过特征值添加用户) | 通过特征值添加用户 |
| [`add_user_by_fea_ret`](#通过特征值添加用户结果) |  通过特征值添加用户结果 |
| [`query_uid`](#查询UID是否存在) |  查询`UID`是否存在 |
| [`query_uid_ret`](#查询UID是否存在结果) |  查询`UID`是否存在结果 |
| [`del_user_by_uid`](#通过UID删除用户) |  通过`UID`删除用户 |
| [`del_user_by_uid_ret`](#通过UID删除用户结果) | 通过`UID`删除用户结果 |
| [`query_face`](#查询模块存储人脸信息) |  查询模块中存储的人脸信息 |
| [`query_face_ret`](#查询模块存储人脸信息结果) | 查询模块中存储的人脸信息结果 |
| [`set_lcd_display`](#设置屏幕显示) | 设置屏幕显示字符串或者图片 |
| [`set_lcd_display_ret`](#设置屏幕显示结果) | 设置屏幕显示字符串或者图片结果 |
| [`clr_lcd_display`](#删除屏幕显示) | 删除屏幕显示元素 |
| [`clr_lcd_display_ret`](#删除屏幕显示结果) | 删除屏幕显示元素结果 |
| [`brd_hard_cfg`](#设置模块硬件配置) | 设置模块硬件配置 |
| [`brd_hard_cfg_ret`](#设置模块硬件配置结果) |  设置模块硬件配置结果 |
| [`brd_soft_cfg`](#设置模块软件配置) | 设置模块软件配置  |
| [`brd_soft_cfg_ret`](#设置模块软件配置结果) | 设置模块软件配置结果 |
| [`qrscan`](#进行二维码扫码) | 模块进行二维码扫码  |
| [`qrscan_ret`](#二维码扫码结果) | 二维码扫码结果 |
| [`set_notify`](#设置通知陌生人) | 设置是否通知陌生人信息 |
| [`set_notify_ret`](#设置通知陌生人结果) | 设置是否通知陌生人信息结果 |

> 以上 `cmd` 可点击跳转

<div STYLE="page-break-after: always;"></div>

## **通信协议**

### **初始化完成**

```json
{
    "version": 2,
    "type": "init",
    "code": 0,
    "msg": "init done",
    "proto": "0.1"
}
```

#### 说明

模块启动完成

<br/>
<br/>

### **数据包解析出错信息**

```json
{
    "version": 2,
    "type": "pkt_prase_failed_ret",
    "msg": "json prase failed",
    "code": 1,
    "cmd": "unknown"
}
```

#### 说明

接受到错误的数据包之后返回, 并指出错误的地方, 主要用来协助排查错误

<br/>
<br/>

### **输出人脸信息**

```json
{"version":2,"type":"face_info","code":0,"msg":"have face","info":{"pic":"540A730200000000","total":1,"current":0,"x1":34,"y1":34,"x2":171,"y2":178,"score":0,"uid":"null","feature":"feature base64 encode or null"}}
```

#### 说明

`pic`: 当有多个人脸时用来判断是否属于同一张图片

`total`: 本次识别中人脸总数

`current`: 本次识别中第 `N` 张人脸(从`0`开始计数)

`x1`: 人脸坐标框左上角 `x`

`y1`: 人脸坐标框左上角 `y`

`x2`: 人脸坐标框右下角 `x`

`y2`: 人脸坐标框右下角 `y`

`score`: 人脸匹配值(直接输出特征值时为 0)

`uid`: 人脸对应的 `UID`(直接输出特征值时为 `null`)

`feature`: 人脸特征值, 可配置是否输出(不输出时为 `null`)

<br/>
<br/>

### **设置是否进行人脸识别**
```json
{"version":2,"type":"face_recon","query_stat":0,"set_stat":1}
```

#### 说明

`query_stat`:查询当前人脸识别的状态, `0`禁用,`1`使能

`set_stat`: 设置是否进行人脸识别

### **设置是否进行人脸识别结果**
```json
{"version":2,"type":"face_recon_ret","code":0,"msg":"set_stat success","stat":1}
```

#### 说明

`msg`: 执行结果

`stat`: 当前是否进行人脸识别的状态

`code`: 状态码

- 状态码

  `0`: 成功

  `1`: 解析失败


### **计算图片人脸特征值**

```json
{"version": 2,"type": "cal_pic_fea","img": {"size": 10152,"auto_add":0,"sha256": "E65083CFEEEA8F377094C2297E8D3691C23AA8BAD33A82B5E4E4981914FFAC74","uid":"0A6F4FB4000000000000000000000000"}}
```

#### 说明

`threshold`: 人脸检测阈值, 可选,默认为`70`

`size`: Jpeg 图片的大小, **注意, 最大支持 30K 的图片**

`auto_add`: 识别成功后自动添加用户到模块(默认不添加, 那么返回的`UID`全为`0`)

`sha256`: `Jpeg` 图片的 `sha256` 校验值 (`7zip` 以及 `haozip` 都支持计算)

`uid`: 如果选择自动添加到模块, 将使用这个指定的`uid`

收到以下返回内容(`code` 为 1)就可以开始发送图片, 必须在`10s`内发送完毕。超时退出接受`jpeg`状态

```json
{"version":2,"type":"cal_pic_fea_ret","code":1,"msg":"please start send jpeg image","info":{"uid":"null","feature":"null"}}
```

> 当 `info` 中的 `code`为 `1` 表示可以开始发送 `Jpeg` 图片

可使用 `XCOM` 或者其他串口助手的发送文件功能, 载入 `Jpeg` 文件, 选择发送即可

<br/>
<br/>

### **计算图片人脸特征值结果**

```json
{"version":2,"type":"cal_pic_fea_ret","code":0,"msg":"get feature success","info":{"face_prob":0.90,"uid":"0A6F4FB4000000000000000000000000","feature":"feature base64 encode"}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`uid`: 人脸在模块中存储的 `UID`, 如果需要删除相应人脸需要此 `UID`

`feature`: 人脸计算得出的特征值(`base64 encode`)

`face_prob`: 人脸检测分数, 正常值为小于`1`的浮点数

> 在[计算图片人脸特征值](#计算图片人脸特征值)数据包中可选择是否自动添加用户到模块中

- 状态码

  `0`: 计算特征值成功

  `1`: 可以开始发送 `Jpeg` 图片

  `2`: 解析 `Json` 出错, `msg` 中会指出出错地方

  `3`: 模块存储已满

  `4`: 图片中有多张人脸

  `5`: 图片中没有人脸(可能是方向不对, 或者是人脸太小)

  `6`: `Jpeg` 解码失败(或者图片不是 `320x240` 分辨率)

  `7`: `Jpeg` 文件 `sha256` 校验失败, 或者等待接受图片超时

<br/>
<br/>

### **添加用户指定UID**

```json
{"version":2,"type":"add_user_spec_uid","user":{"uid":"EDE6E800A20000000000000000000000","time_s":5}}
```

#### 说明

> 相当于按键录入用户, 可以指定`uid`,会检测用户是否正脸

`uid`: 用户指定新添加用户的`uid`

`time_s`: 添加用户超时时间, 默认`5`s,最大值`100`

<br/>
<br/>

### **添加用户指定UID结果**

```json
{"version":2,"type":"add_user_spec_uid_ret","user":{"uid":"EDE6E800A20000000000000000000000"}}
```

#### 说明

`msg`: 执行结果

`code`: 状态码

- 状态码

  `0`: 成功

  `1`: 失败

  `2`： 等待添加

<br/>
<br/>

### **通过特征值添加用户**

```json
{"version":2,"type":"add_user_by_fea","user":{"uid":"EDE6E800A20000000000000000000000","fea":"feature base64 encode"}}
```

#### 说明

`uid`: 用户的`uid`

`fea`: 用户人脸特征值

### **通过特征值添加用户结果**

```json
{"version":2,"type":"add_user_by_fea_ret","code":0,"msg":"add user success","uid":"EDE6E800A20000000000000000000000"}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`uid`: 添加成功的`uid`,如果失败全为`0`

- 状态码

  `0`: 添加成功

  `1`: `Json` 解析出错

  `2`: 保存到`flash`失败

  `3`: `uid`已存在

<br/>
<br/>

### **查询UID是否存在**
```json
{"version":2,"type":"query_uid","uid":"0E3D6BA9000000000000000000000000"}
```

#### 说明
`uid`: 需要查询的 uid

### **查询UID是否存在结果**
```json
{"version":2,"type":"query_uid_ret","code":0,"msg":"uid exist","uid_id":1}
```

#### 说明

`msg`: 执行结果

`uid_id`: `UID`存储的`id`, 这个可以配合查询用户信息使用

`code`: 状态码

- 状态码
  `0`: `UID`存在

  `1`: `UID`不存在

  `2`: 解析错误

### **通过UID删除用户**

```json
{"version": 2,"type": "del_user_by_uid","uid":"1BC6EB528C0000000000000000000000"}
```

#### 说明

`uid`: 需要删除的用户 uid

> 当 `uid` 为 `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF` (32 个`F`)时删除所有的用户

如果失败在返回结果有具体说明

<br/>
<br/>

### **通过UID删除用户结果**

```json
{"version":2,"type":"del_user_by_uid_ret","code":3,"msg":"can not find user by uid"}
```

#### 说明

`msg`: 执行结果

`code`: 状态码

- 状态码

  `0`: 删除成功

  `1`: `Json` 解析出错, 缺少关键字

  `2`: `flash` 操作失败

  `3`: 未能查找到对应 `uid` 的用户

<br/>
<br/>

### **查询模块存储人脸信息**

```json
{"version":2,"type":"query_face","query":{"total":1,"start":0,"end":10,"out_feature":0}}
```

#### 说明

`total`: 为 `1` 查询一共存储多少人脸信息,  `start` 和 `end` 以及 `out_feature` 没有意义,  为 `0` 表示查询 从 `start` 到 `end` 区间的人脸 UID

`out_feature`： 人脸信息是否输出对应特征值, 默认不输出(输出特征值的话一次只能查一个)

`start`: 查询区间起始值

`end`: 查询区间结束值

<br/>
<br/>

### **查询模块存储人脸信息结果**

```json
{"version":2,"type":"query_face_ret","code":0,"msg":"query uid ands feature success","face":{"total":2,"start":0,"end":1,"info":[{"order":0,"uid":"22BCD239290000000000000000000000","feature":"feature bease64 encode"}...]}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`face`:

- `total`: 当前模块中人脸总数

- `start`: 本次查询结果区间起始值(从`0`开始计数)

- `end`: 本次查询结果区间结束值

- `info`:

  - `order`: 当前人脸的顺序

  - `uid`: 当前人脸的 `UID`

  - `feature`: 当前人脸的特征值

- 状态码

  `0`: 查询成功

  `1`: `Json` 解析出错

  `2`: 当查询包中设置 `total` 为 `1` 时返回当前模块中存储的人脸数量

  `3`: 从 `flash` 中读取保存的数据时出错

<br/>
<br/>

### **设置屏幕显示**

```json
{"version":2,"type":"set_lcd_display","cfg":{"cfg_type":"str","zhCN":0,"id":0,"x":0,"y":0,"size":16,"str":"abcd","color":1,"bg_color":1}}
```

```json
{"version":2,"type":"set_lcd_display","cfg":{"cfg_type":"pic","id":0,"x":0,"y":0,"w":320,"h":240,"addr":123456,"alpha":50}}
```

#### 说明

`cfg_type`: `str`或者`pic`,设置叠加图片或者字符串

字符串显示配置：

  - `id`: 字符串的`id`, 删除时使用

  - `x`: 字符串显示位置的`x`坐标,**注意,`MF1 1.3inch`,`0`需要转换成`40`**

  - `y`: 字符串显示位置的`y`坐标

  - `size`: 目前支持`16`和`32`

  - `str`: 需要显示的字符串

  - `color`: 字符串的颜色, 数字类型, `RGB565`编码,`63488`表示红色

  - `bg_color`: 字符串底色, 数字类型, 等于`1`的时候不设置背景色

  - `zhCN`: 字符串是否为中文,<br>如果字符串是中文, 需要对`str`进行`base64`编码, <br>目前支持`GB2312`编码的中文显示,`ye7b2s75y9m/xry8`表示`深圳矽速科技`

图片显示配置：

  - `id`: 图片的`id`, 删除时使用

  - `x`: 图片显示原点`x`,**注意,`MF1 1.3inch`,`0`需要转换成`40`**

  - `y`: 图片显示原点`y`

  - `w`: 图片的宽

  - `h`: 图片的高

  - `addr`: 图片在flash中保存的地址

  - `alpha`: 图片与摄像头图像叠加透明度

<br/>
<br/>

### **设置屏幕显示结果**

```json
{"version":2,"type":"set_lcd_display_ret","msg":"set lcd display success","code":0,"id":0}
```

#### 说明

`id`: 屏幕显示内容的`id`

`msg`: 消息

`code`: 代码

  - `0`： 成功

  - `1`： 失败

<br/>
<br/>

### **删除屏幕显示**

```json
{"version":2,"type":"clr_lcd_display","id":0}
```

#### 说明

`id`: 屏幕显示内容的`id`, 当`id`为1024时删除所有的内容

<br/>
<br/>

### **删除屏幕显示结果**

```json
{"version":2,"type":"clr_lcd_display_ret","msg":"clr lcd display success","code":0,"id":0}
```

#### 说明

`id`: 屏幕显示内容的`id`

`msg`: 消息

`code`: 代码

  - `0`： 成功

  - `1`： 失败

<br/>
<br/>

### **设置模块硬件配置**

```json
{"version":2,"type":"brd_hard_cfg","cfg":{"get_cfg":0,"cfg_type":"lcd_cam","lcd_flip":0,"lcd_mirror":0,"cam_flip":0,"cam_mirror":0}}
```

```json
{"version":2,"type":"brd_hard_cfg","cfg":{"get_cfg":0,"cfg_type":"uart_relay","port_tx":10,"port_rx":11,"log_tx":5,"log_rx":4,"relay_low": 12,"relay_high": 13,"key":24,"key_dir":1}}
```

#### 说明

`get_cfg`: 读取当前配置

<br/>

当 `cfg_type` 为 `lcd_cam` 时, 查询或者设置模块的屏幕及摄像头的旋转

`lcd_flip`: `lcd`显示进行垂直镜像

`lcd_mirror`: `lcd`显示进行水平镜像

`cam_flip`: `camera` 进行垂直镜像

`cam_mirror`:`camera` 进行水平镜像

<br/>

当 `cfg_type` 为 `uart_relay` 时, 查询或者设置模块的串口及继电器的配置

`port_tx`: 本模块与其他模块通信`TX`引脚, 默认为`10`

`port_rx`: 本模块与其他模块通信`RX`引脚, 默认为`11`

`log_tx`: 本模块输出日志`TX`引脚, 默认为`5`

`log_rx`: 本模块输出日志`RX`引脚, 默认为`4`

`relay_low`: 继电器输出**常低**引脚, 默认为`12`

`relay_high`: 继电器输出**常高**引脚, 默认为`13`

`key`: 按键, 默认为`24`

`key_dir`: 按键按下电平, 默认为`1`

> 注意, 模块不会检测设置的`IO`是否相同, 请自己保证参数的正确<br>重启生效设置

<br/>
<br/>

### **设置模块硬件配置结果**

```json
{"version":2,"type":"brd_hard_cfg_ret","code":1,"msg":"get cfg success","cfg":{}}
```

#### 说明

`msg`: 消息

`code`: 代码

  - `0`： 成功

  - `1`： 失败

`cfg`: 参考上边的[设置模块硬件配置](#设置模块硬件配置)指令

<br/>
<br/>

### **设置模块软件配置**

```json
{"version":2,"type":"brd_soft_cfg","cfg":{"get_cfg":0,"out_fea":0,"auto_out_fea":0,"out_interval_ms":100,"out_threshold":88.0,"pkt_fix":0,"relay_open_s":2,"port_baud":115200}}
```

#### 说明

> `0`为关闭, `1`为打开

`get_cfg`: 读取当前配置

`out_fea`: 识别成功是否输出特征值, 默认为`0`

`auto_out_fea`: 不与存储的人脸库进行对比, 识别到人脸就输出, 默认为`0`

`out_interval_ms`: 两次输出结果的间隔, 单位为`ms`, 默认为`100`, 最大为`1000`

`out_threshold`: 人脸比对输出阈值(浮点数, 最大100), 默认为`77.0`

`pkt_fix`: 通信协议是否加头尾以及 `CRC16` 校验, 默认为 `0`

`relay_open_s`: 继电器打开时间, 单位为`s`, 默认为`2`, 最大为`100`

`port_baud`: 通信串口波特率, 默认为`115200`

`out_fea` 取值说明

  - `0`： 不输出特征值

  - `1`： 输出特征值(`flash`存储的特征值)

  - `2`： 输出实时特征值

`auto_out_fea` 为`1`时, 输出的人脸信息中, `uid`为`null`, `score`为`0`

> 重启使设置生效

##### 开启 `pkt_fix` 的通信格式

```C
0xAA 0x55 HI(LEN) LO(LEN) HI(CRC16) LO(CRC16) ...(data)... 0x55 0xAA
```

可使用 [http://www.ip33.com/crc.html](http://www.ip33.com/crc.html) 选择 `CRC-16/X25 x16+x12+x5+1`

<br/>
<br/>

### **设置模块软件配置结果**

```json
{"version":2,"type":"brd_soft_cfg_ret","code":1,"msg":"get cfg success","cfg":{}}
```

#### 说明

`msg`: 消息

`code`: 代码

  - `0`： 成功

  - `1`： 失败

`cfg`: 参考上边的[设置模块软件配置](#设置模块软件配置)指令

<br/>
<br/>


## 以下属于扩展功能

### **进行二维码扫码**
```json
{"version":2,"type":"qrscan","time_out_s":20}
```

#### 说明

`time_out_s`: 二维码扫码超时时间

### **二维码扫码结果**
```json
{"version":2,"type":"qrscan_ret","code":0,"msg":"success","qrcode":"xxxxxx"}
```

#### 说明

> 建议使用`L`纠错等级的二维码, 并且二维码版本最好小于`7`

`qrcode`:扫码结果

`msg`: 执行结果

`code`: 代码

  - `0`： 成功

  - `1`： 解析指令失败

  - `2`: 扫码超时

  - `3`： 未知错误

### **设置通知陌生人**
```json
{"version":2,"type":"set_notify","query":0,"en":1,"out_fea":0}
```

#### 说明

> 这个指令默认不开启, 需要自行编译固件

`query`: 查询当前状态

`en`: `1`使能, `0`禁用

`out_fea`:`1`输出陌生人的特征值,`0`不输出


### **设置通知陌生人结果**
```json
{"version":2,"type":"set_notify_ret","code":0,"msg":"save cfg success","en":0,"out_fea":0}
```

#### 说明

`msg`: 执行结果

`code`: 代码

  - `0`： 成功

  - `1`： 解析指令失败

  - `2`： 未知错误
