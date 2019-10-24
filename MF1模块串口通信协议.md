# 基于串口通信的人脸识别模块通信协议 `V2.0`

## **修改记录**

| 版本     | 时间         | 修改内容                                                            |
| -------- | ------------ | -------------------------------------------------------------------|
| `V1.0`   | `2019.05.31` | 新建协议                                                           |
| `V1.1`   | `2019.06.03` | `head_fix`改为`pkt_fix`<br/>添加串口 `IO` 说明                      |
| `V1.2`   | `2019.06.05` | 所有数据包增加`code`及`msg`                                         |
| `V1.3`   | `2019.06.13` | 增加翻转屏幕及摄像头接口                                             |
| `V1.4`   | `2019.06.14` | 增加使用特征值添加用户接口<br/>修复`bug`<br/>添加初始化添加版本信息     |
| `V1.5`   | `2019.06.17` | 增加在识别模式下输出特征值的选项                                      |
| `V1.5.1` | `2019.06.21` | 计算图片特征值，添加可选项进行人脸检测阈值设置                         |
| `V1.6`   | `2019.06.22` | 增加设置通信串口引脚指令<br/>修复`bug`                                |
| `V1.7`   | `2019.07.16` | 支持`112x112`图片输入计算特征值<br/>特征值进行了压缩                    |
| `V2.0`   | `2019.07.19` | 支持`MF1`模块，活体检测，部分功能不支持                                 |
| `V2.1`   | `2019.08.01` | 支持配置板子的`IO`                                                  |

## 硬件连接

| `K210`  |说明                                    |
| ------  |---------------------------------------|
| `IO5`   | 协议串口的`TX`,可设置，默认`5`,默认波特率为`115200` |
| `IO4`   | 协议串口的`RX`,可设置，默认`4` |
| `IO11`  | 调试串口的`RX`，可设置，默认`11`,默认波特率为`115200` |
| `IO10`  | 调试串口的`TX`，可设置，默认`10` |
| `IO24`  | 短按录入人脸，可设置，默认为`24`<br>（长按清空人脸特征值需烧录特殊固件） |
| `IO13`  | 继电器常高输出，可设置，默认为`13`     |
| `IO12`  | 继电器常低输出，可设置，默认为`12`     |

<div STYLE="page-break-after: always;"></div>

## `Json` 基本格式

```json
{"vesrion":$protocol_version,"type":"cmd_type","code":0,"msg":"msg","param":{"xx":"xx","xx":xx}}\r\n
```

#### 说明

- 当前 `protocol_version` 为 `1`

- 数据包结尾必须加 `\r\n`

- 数据包中间不允许有 `\r\n`

- 注意`\r\n`要转义为`0d0a`

### `cmd_type`

| `cmd_type`                                          | 说明                            |
| --------------------------------------------------- | ------------------------------- |
| [`init`](#初始化完成)                               | 模块发送初始化完成消息          |
| [`pkt_prase_failed_ret`](#数据包解析出错信息)       | 数据包解析出错信息              |
| [`set_cfg`](#设置模块参数)                          | 设置模块参数                    |
| [`set_cfg_ret`](#设置模块参数结果)                  | 设置模块参数结果                |
| [`get_cfg`](#获取模块参数)                          | 获取模块参数                    |
| [`get_cfg_ret`](#获取模块参数结果)                  | 获取模块参数结果                |
| [`cal_pic_fea`](#计算图片人脸特征值)                | 计算图片人脸特征值              |
| [`cal_pic_fea_ret`](#计算图片人脸特征值结果)        | `JPEG` 图片特征值计算结果       |
| [`del_user_by_uid`](#删除用户)                      | 使用 `UID` 进行用户删除         |
| [`del_user_by_uid_ret`](#删除用户结果)              | 使用 `UID` 进行用户删除结果     |
| [`face_info`](#输出人脸信息)                        | 识别人脸后输出信息              |
| [`query_face`](#查询当前模块存储人脸信息)           | 查询当前模块存储人脸信息        |
| [`query_face_ret`](#查询当前模块存储人脸信息结果)   | 查询当前模块存储人脸信息结果    |
| [`lcd_cam_roate`](#屏幕及摄像头旋转)                | 设置`LCD`及`CAMERA`进行旋转(`MF1`不支持)|
| [`lcd_cam_roate_ret`](#屏幕及摄像头旋转结果)        | 设置`LCD`及`CAMERA`进行旋转结果(`MF1`不支持)|
| [`add_uer_by_fea`](#通过特征值添加用户)             | 通过特征值添加用户              |
| [`add_uer_by_fea_ret`](#通过特征值添加用户结果)     | 通过特征值添加用户结果          |
| [`set_brd_pin_cfg`](#设置模块引脚分配)         | 设置模块引脚分配            |
| [`set_brd_pin_cfg_ret`](#设置模块引脚分配结果) | 设置模块引脚分配结果        |

> 以上 `cmd` 可点击跳转

<div STYLE="page-break-after: always;"></div>

## **通信协议**

### **初始化完成**

```json
{ "version": 1, "type": "init", "code":0,"msg": "init done","version":"v2.0" }
```

#### 说明

模块启动完成之后发送，之后才可进行操作

<br/>
<br/>

### **数据包解析出错信息**

```json
{"version": 1,"type": "pkt_prase_failed_ret","msg": "json prase failed","code": 1,"cmd": "unknown"}
```

#### 说明

接受到错误的数据包之后返回，并指出错误的地方，主要用来协助排查错误

<br/>
<br/>

### **设置模块参数**

```json
{"version":1,"type":"set_cfg","cfg":{"uart_baud":115200,"out_feature":0,"open_delay":1,"pkt_fix":0,"auto_out_feature":0,"out_interval_in_ms":500,"fea_gate":70}}
```

#### 说明

`uart_baud`: 模块通信串口波特率，默认为 `115200`

`out_feature`: 识别到人脸之后输出信息是否附带人脸的特征值，默认为 `0`

`open_delay`: 输出 `IO` 打开（翻转）时间，默认为 `1`

`pkt_fix`: 通信协议是否加头尾以及 `CRC16` 校验，默认为 `0`，不开启将直接传输数据

`auto_out_feature`: 是否进行人脸比对

`out_interval_in_ms`: 输出特征值间隔时间 `ms`,默认 `500`，设置为 `0` 不限制，最小限制为 `500`

`fea_gate`: 人脸比对阈值

- `auto_out_feature` 取值说明

  - `0`: 需要进行比对，输出添加人脸时的特征值

  - `1`: 不需要进行比对，输出实时的特征值，此时`uid`为`null`，`score`为`0`

  - `2`: 需要进行比对，输出人脸实时的特征值

##### 开启 `pkt_fix` 的通信格式

```C
0xAA 0x55 HI(LEN) LO(LEN) HI(CRC16) LO(CRC16) ...(data)... 0x55 0xAA
```

可使用 [http://www.ip33.com/crc.html](http://www.ip33.com/crc.html) 选择 `CRC-16/X25 x16+x12+x5+1`

<br/>
<br/>

### **设置模块参数结果**

```json
{"version":1,"type":"set_cfg_ret","msg":"save cfg success","code":0}
```

#### 说明

`msg`: 返回信息

`code`: 返回状态码

- 状态码

  `0`: 设置模块参数成功

  `1`: 解析 `Json` 失败，`msg` 中会指出错误地方

  `2`: 保存模块参数失败

> 如果更改了 `uart_baud` 以及 `pkt_fix` 模块会自动重启使更改生效

<br/>
<br/>

### **获取模块参数**

```json
{ "version": 1, "type": "get_cfg" }
```

#### 说明

获取模块当前配置

<br/>
<br/>

### **获取模块参数结果**

```json
{"version":1,"type":"get_cfg_ret","code":0,"msg":"get cfg success","cfg":{"uart_baud":115200,"out_feature":0,"open_delay":1,"pkt_fix":0,"auto_out_feature":0,"out_interval_in_ms":500,"fea_gate":70}}
```

#### 说明

与 `set_cfg` 参数一致，只是 `type` 不同

<br/>
<br/>

### **计算图片人脸特征值**

```json
{"version": 1,"type": "cal_pic_fea","img": {"size": 10152,"auto_add":0,"sha256": "E65083CFEEEA8F377094C2297E8D3691C23AA8BAD33A82B5E4E4981914FFAC74"}}
```

### 说明

`gate`: 人脸检测阈值，可选项，不写使用默认值

`size`: Jpeg 图片的大小, **注意，最大支持 30K 的图片**

`auto_add`: 识别成功后自动添加用户到模块（默认不添加，那么返回的`UID`全为`0`）

`sha256`: `Jpeg` 图片的 `sha256` 校验值 （`7zip` 以及 `haozip` 都支持计算）

收到以下返回内容（`code` 为 1）就可以开始发送图片，必须在`10s`内发送完毕。超时退出接受`jpeg`状态

```json
{"version":1,"type":"cal_pic_fea_ret","code":1,"msg":"please start send jpeg image","info":{"uid":"null","feature":"null"}}
```

> 当 `info` 中的 `code`为 `1` 表示可以开始发送 `Jpeg` 图片

可使用 `XCOM` 或者其他串口助手的发送文件功能，载入 `Jpeg` 文件，选择发送即可

<br/>
<br/>

### **计算图片人脸特征值结果**

- 正确返回

```json
{"version":1,"type":"cal_pic_fea_ret","code":0,"msg":"get feature success","info":{"face_prob":0.90,"uid":"0A6F4FB4000000000000000000000000","feature":"feature base64 encode"}}
```

- 错误返回(举例)

```json
{"version":1,"type":"cal_pic_fea_ret","code":2,"msg":"can not find img.sha256","info":{"face_prob":0,"uid":"null","feature":"null"}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`uid`: 人脸在模块中存储的 `UID`，如果需要删除相应人脸需要此 `UID`

`feature`: 人脸计算得出的特征值（`base64 encode`）

`face_prob`: 人脸检测分数，正常值为小于`1`的浮点数

> 在[计算图片人脸特征值](#计算图片人脸特征值)数据包中可选择是否自动添加用户到模块中

- 状态码

  `0`: 计算特征值成功

  `1`: 可以开始发送 `Jpeg` 图片

  `2`: 解析 `Json` 出错，`msg` 中会指出出错地方

  `3`: 模块存储已满

  `4`: 图片中有多张人脸

  `5`: 图片中没有人脸（可能是方向不对，或者是人脸太小）

  `6`: `Jpeg` 解码失败（或者图片不是 `320x240` 分辨率）

  `7`: `Jpeg` 文件 `sha256` 校验失败，或者等待接受图片超时

<br/>
<br/>

### **删除用户**

```json
{"version": 1,"type": "del_user_by_uid","uid":"1BC6EB528C0000000000000000000000"}
```

#### 说明

`uid`: 需要删除的用户 uid

> 当 `uid` 为 `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF` （32 个`F`）时删除所有的用户

如果失败在返回结果有具体说明

<br/>
<br/>

### **删除用户结果**

```json
{"version":1,"type":"del_user_by_uid_ret","code":3,"msg":"can not find user by uid"}
```

#### 说明

`msg`: 执行结果

`code`: 状态码

- 状态码

  `0`: 删除成功

  `1`: `Json` 解析出错，缺少关键字

  `2`: `flash` 操作失败

  `3`: 未能查找到对应 `uid` 的用户

<br/>
<br/>

### **输出人脸信息**

```json
{"version":1,"type":"face_info","code":0,"msg":"have face","info":{"pic":"540A730200000000","total":1,"current":0,"x1":34,"y1":34,"x2":171,"y2":178,"score":0,"uid":"null","feature":"feature base64 encode or null"}}
```

#### 说明

`pic`: 当有多个人脸时用来判断是否属于同一张图片

`total`: 本次识别中人脸总数

`current`: 本次识别中第 `N` 张人脸（从`0`开始计数）

`x1`: 人脸坐标框左上角 `x`

`y1`: 人脸坐标框左上角 `y`

`x2`: 人脸坐标框右下角 `x`

`y2`: 人脸坐标框右下角 `y`

`score`: 人脸匹配值（直接输出特征值时为 0）

`uid`: 人脸对应的 `UID`（直接输出特征值时为 `null`）

`feature`: 人脸特征值，可配置是否输出（不输出时为 `null`）

<br/>
<br/>

### **查询当前模块存储人脸信息**

```json
{"version":1,"type":"query_face","query":{"total":1,"start":0,"end":10,"out_feature":0}}
```

#### 说明

`total`: 为 `1` 查询一共存储多少人脸信息， `start` 和 `end` 以及 `out_feature` 没有意义， 为 `0` 表示查询 从 `start` 到 `end` 区间的人脸 UID

`out_feature`： 人脸信息是否输出对应特征值，默认不输出（输出特征值的话一次只能查一个）

`start`: 查询区间起始值

`end`: 查询区间结束值

<br/>
<br/>

### **查询当前模块存储人脸信息结果**

```json
{"version":1,"type":"query_face_ret","code":0,"msg":"query uid ands feature success","face":{"total":2,"start":0,"end":1,"info":[{"order":0,"uid":"22BCD239290000000000000000000000","feature":"feature bease64 encode"}...]}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`face`:

- `total`: 当前模块中人脸总数

- `start`: 本次查询结果区间起始值（从`0`开始计数）

- `end`: 本次查询结果区间结束值

- `info`:

  - `order`: 当前人脸的顺序

  - `uid`: 当前人脸的 `UID`

  - `feature`: 当前人脸的特征值

* 状态码

  `0`: 查询成功

  `1`: `Json` 解析出错

  `2`: 当查询包中设置 `total` 为 `1` 时返回当前模块中存储的人脸数量

  `3`: 从 `flash` 中读取保存的数据时出错

### **屏幕及摄像头旋转**

```json
{"version":1,"type":"lcd_cam_roate","cfg":{"get_cfg":0,"lcd_flip":0,"lcd_mirror":0,"cam_flip":0,"cam_mirror":0}}
```

#### 说明

`get_cfg`: 获取当前模块的 `LCD` 及 `CMA` 参数

`lcd_flip`: `lcd`显示进行垂直镜像

`lcd_mirror`: `lcd`显示进行水平镜像

`cam_flip`: `camera` 进行垂直镜像

`cam_mirror`:`camera` 进行水平镜像

> `MF1`模块不支持此指令

### **屏幕及摄像头旋转结果**

```json
{"version":1,"type":"lcd_cam_roate_ret","code":0,"msg":"set lcd and cam success","cfg":{"lcd_flip":0,"lcd_mirror":0,"cam_flip":0,"cam_mirror":0}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

- 状态码

  `0`: 设置成功

  `1`: `Json` 解析出错

  `2`: 保存配置出错

  `3`: 获取配置成功

  `4`: `MF1`模块不支持设置

### **通过特征值添加用户**

```json
{"version":1,"type":"add_uer_by_fea","user":{"uid":"EDE6E800A20000000000000000000000","fea":"feature base64 encode"}}
```

#### 说明

`uid`: 用户的`uid`

`fea`: 用户人脸特征值

### **通过特征值添加用户结果**

```json
{"version":1,"type":"add_uer_by_fea_ret","code":0,"msg":"add user success","uid":"EDE6E800A20000000000000000000000"}
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

### **设置模块引脚分配**

```json
{"version": 1,"type": "set_brd_pin_cfg","cfg":{"get_cfg":0,"port_tx":10,"port_rx":11,"log_tx":5,"log_rx":4,"relay_low": 12,"relay_high": 13,"key":24,"key_dir":1}}
```

#### 说明

`get_cfg`: 获取当前模块的配置

`port_tx`: 本模块与其他模块通信`TX`引脚，默认为`10`

`port_rx`: 本模块与其他模块通信`RX`引脚，默认为`11`

`log_tx`: 本模块输出日志`TX`引脚，默认为`5`

`log_tx`: 本模块输出日志`RX`引脚，默认为`4`

`relay_low`: 继电器输出**常低**引脚，默认为`12`

`relay_high`: 继电器输出**常高**引脚，默认为`13`

`key`: 按键，默认为`24`

`key_dir`: 按键按下电平，默认为`1`

> 注意，模块不会检测设置的`IO`是否相同，请自己保证参数的正确

### **设置模块引脚分配结果**

```json
{"version":1,"type":"set_brd_pin_cfg_ret","code":0,"msg":"get uart_pin cfg success","cfg":{"port_tx":10,"port_rx":11,"log_tx":5,"log_rx":4,"relay_low":12,"relay_high":13,"key":24,"key_dir":1}}
```

#### 说明

`code`: 状态码

`msg`: 返回信息

`cfg`： 模块当前配置，与[设置指令一样](#设置模块引脚分配)

- 状态码

  `0`: 设置成功

  `1`: `Json` 解析出错

  `2`: 设置参数有误，在`msg`中指出

  `3`: 保存参数失败
