# MF1简易版串口协议图文说明
> 注：本文使用markdown格式编写，请使用任意markdown阅读器查看图文内容

## 串口协议格式
    帧头2B + 帧长2B + 校验2B + 命令码1B + 参数负载nB 
	帧头： @@/$$  @@表示使能校验，$$表示失能校验(便于手工调试协议)
	帧长：16位帧长，每帧最大64KB，是为了 BINCMD_FTRALL 导出全部特征值指令能一次性导出完特征值
	校验：CRC16格式
	命令码：单字节，最高位表示方向，主动发出bit7=0,回复bit7=1，即回复cmd|0x80

> 注意

0. 默认波特率为115200
1. 指令为单个阻塞式，在得到上个指令的回复前发送的指令会被丢弃。每次主循环会处理一次指令，处理周期约 100~150ms。
2. 使用 BINCMD_ABORT 指令可以中断某些长时间执行的指令，比如 BINCMD_RECORD。
3. 对于主机来说，本协议只需要256/512字节(127/255人)的串口缓冲区，适用于小容量的单片机。
4. 本协议支持每人最多8张人脸模板。
5. 改变波特率的指令的应答是使用原波特率应答。
6. person_id 为一字节，0xff占用为特殊用途，所以最多存储255人。


## 串口指令列表
|指令名|值|说明|
|--|--|--|
|BINCMD_PING    | 0x00|ping指令|
|BINCMD_ABORT   | 0x01|中断当前执行指令|
|BINCMD_INFO    | 0x02|查询板卡信息|
|BINCMD_BAUD    | 0x03|设置波特率|
|BINCMD_RECORD  | 0x04|开始录入人脸|
|BINCMD_CONFIRM | 0x05|确认录入人脸|
|BINCMD_DEL     | 0x06|删除指定ID人脸|
|BINCMD_FR_RUN  | 0x07|开始/停止运行人脸识别|
|BINCMD_FR_RES  | 0x08|模块返回的人脸识别结果|
|BINCMD_FR_GATE | 0x09|设置人脸识别门限|
|BINCMD_LED     | 0x0a|设置LED灯状态|
|BINCMD_RELAY   | 0x0b|设置继电器状态|
|BINCMD_RSTCFG  | 0x0c|复位板级配置到默认|
|BINCMD_IMPORT  | 0x10|导入人脸信息|
|BINCMD_FCNT    | 0x11|获取人脸库里的数量|
|BINCMD_FLIST   | 0x12|返回人脸列表|
|BINCMD_FTR     | 0x13|返回人脸特征值|
|BINCMD_FTRALL  | 0x14|导出所有人脸特征值|
|BINCMD_QRSCAN  | 0x15|开启二维码扫码|
|BINCMD_QRRES   | 0x16|二维码扫码结果|
|BINCMD_FACEPOS | 0x17|人脸坐标信息|
|BINCMD_PICADD  | 0x20|增加在画面显示的图片|
|BINCMD_STRADD  | 0x21|增加在画面显示的字符|
|BINCMD_DISDEL  | 0x22|清除界面上显示的图片|
|BINCMD_REBOOT  | 0x23|重启设备|
|BINCMD_SOFT_CFG| 0x24|板子配置|
|BINCMD_HARD_CFG| 0x25|板子硬件IO配置|
|BINCMD_PIC_CFG | 0x26|板子图传配置|
|BINCMD_INVALID | 0xff|非法指令|

## 串口错误码列表
~~~
typedef enum
{
	BINERR_NONE    = 0,
	BINERR_ERR     = 1,
	BINERR_ARG     = 2,
	BINERR_BAUD    = 3,
	BINERR_STOREDB = 4,
	BINERR_NOFACE  = 5,
	BINERR_FRTYPE  = 6,
	BINERR_NOMEM   = 7,
	BINERR_NOID    = 8,
	BINERR_RECOK   = 9,
	BINERR_RECTO   = 10, //timeout
	BINERR_RECFULL = 11, //flash full
    BINERR_RECID   = 12, //录入使用的ID错误
	BINCMD_QRTO    = 13, //扫码超时
    BINCM_POP_FAILE= 14,
}mfbin_err_t;
~~~

## 串口指令图文详解
### BINCMD_PING 0x00
ping检测指令，用于检测模块是否存在。  arg=NULL
在模块启动完毕后，模块也会主动向主机发送该指令表示启动完成。
串口信息示例（从串口助手拷贝出的记录，收表示主机收到模块的信息，发表示主机发往模块的信息）：
（以下示例是手工发送指令测试，所以发送方失能了校验）
~~~
[00:03:18.147]收←◆45 38 33 E8 B9 C5 13 
[00:03:18.228]收←◆59 FF 3A F5 
[00:03:18.243]收←◆17 4F 59 FF DB 3F 17 F2 B5 68 FC C8 74 65 C9 D2 B6 5D 3A 4D 01 09 09 C8 88 41 11 0F 40 0B A4 44 88 13 12 37 14 44 09 82 F0 80 25 5C B8 65 21 44 12 8A 50 38 69 90 08 00 30 44 44 96 40 9C F0 00 20 54 B8 B9 E0 21 22 41 88 CD 9A 16 5D BA 4D C6 D1 8A 86 C0 4B 01 0F 31 80 94 42 FB F0 08 02 40 12 F1 10 09 02 2B 70 88 03 00 5A C0 58 B0 83 2F 09 53 A3 20 AD 5A A4 4A CD 25 30 29 65 4A C9 29 62 DA 4B 09 09 25 49 51 1D 19 19 69 0B 05 0D 49 0B 09 09 90 0B 09 09 49 10 1A A0 
[00:03:18.259]收←◆5D FA 
/*这以上为开机的其余信息，忽略；以下为启动完成的信息*/
[00:03:18.515]收←◆40 40 07 00 78 F0 00   //开机完成后模块向主机发送ping指令, 主机可不回复
[00:03:19.467]发→◇24 24 07 00 FF FF 00   //主机向模块发送ping
[00:03:19.524]收←◆40 40 07 00 70 74 80   //模块回复pong，注意模块任何时候都会计算校验，主机可选校验
~~~

### BINCMD_ABORT 0x01
中断指令执行  arg=NULL
~~~
[00:09:07.053]发→◇24 24 07 00 FF FF 01 □
[00:09:07.092]收←◆40 40 08 00 53 9A 81 00 
~~~

### BINCMD_INFO 0x02
获取板卡信息，目前信息待定。  arg=NULL
~~~
[00:09:39.659]发→◇24 24 07 00 FF FF 02 □
[00:09:39.747]收←◆40 40 17 00 1A 21 82 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
~~~

### BINCMD_BAUD 0x03
设置波特率，注意，回复的信息是使用原波特率回复
arg=baud_rate[0,1,2,3] 小端顺序依次发送
~~~
[10:04:19.140]收←◆40 40 07 00 78 F0 00 
[10:05:34.574]发→◇24 24 0B 00 FF FF 03 80 25 00 00 □  //发送切换到9600指令
[10:05:34.706]收←◆40 40 08 00 E3 A9 83 00             //用原波特率正确回应
[10:05:37.231]发→◇24 24 0B 00 FF FF 03 80 25 00 00 □  //再尝试使用115200发送指令，会发现没有回复
[10:05:44.093]发→◇24 24 0B 00 FF FF 03 80 25 00 00 □  //串口助手切换到9600，发送指令
[10:05:44.194]收←◆40 40 08 00 E3 A9 83                //收到回复
[10:05:44.214]收←◆00 
[10:05:47.358]发→◇24 24 0B 00 FF FF 03 80 25 00 00 □
[10:05:47.490]收←◆40 40 08 00 E3 A9 83 
[10:05:47.506]收←◆00 
[10:06:01.214]发→◇24 24 0B 00 FF FF 03 00 C2 01 00 □  //重新切回115200
[10:06:01.314]收←◆40 40 08 00 E3 A9 83 00             //9600波特率回应成功
~~~

### BINCMD_RECORD 0x04
人脸录入指令
arg=person_id,face_idx,timeout_s,confirm_flag
person_id: 0~254
face_idx:  0~7. 注意不支持写入到已存在的person_id&face_idx,需要先删除，再添加
timeout_s: 0~255,单位秒
confirm_flag：录入后立即生效还是执行 BINCMD_CONFIRM 后生效
> 如果使能了confirm_flag, 则模块在收到 BINCMD_CONFIRM 之前，会把录入的人脸暂存到ram（最多8份）
> 直到收到 BINCMD_CONFIRM 后将暂存的人脸存入flash

录入成功时会返回当前用户的坐标信息,顺序为l_eye_x, l_eye_y, r_eye_x, r_eye_y, nose_x, nose_y, l_mouth_x, l_mouth_x, r_mouth_x, r_mouth_y, face_w, face_h,基本与`BINCMD_FACEPOS`相同


录入成功后屏幕上默认会有简易UI提示，用户可以定制修改。

~~~
[16:43:33.694]发→◇24 24 0B 00 FF FF 04 00 00 05 00 □  //录入人脸，5秒超时
[16:43:33.830]收←◆40 40 08 00 EB E4 84 00             //模块应答收到
[16:43:39.575]收←◆40 40 08 00 B1 4B 84 0A             //5秒未出现人脸，模块提示超时
[16:44:29.990]发→◇24 24 0B 00 FF FF 04 00 00 05 00 □  //再次录入
[16:44:30.082]收←◆40 40 08 00 EB E4 84 00             //应答
[16:44:31.603]收←◆40 40 08 00 2A 79 84 09             //录入成功响应
[16:44:42.374]发→◇24 24 0B 00 FF FF 04 00 00 05 00 □  //以相同ID再次录入
[16:44:42.544]收←◆40 40 08 00 EB E4 84 00             //应答
[16:44:42.927]收←◆40 40 08 00 87 2E 84 0C             //报ID已存在错误
~~~

### BINCMD_CONFIRM 0x05
确认人脸录入指令，arg=0/1  
0,抛弃之前录入的人脸；1,之前录入的人脸正式入库生效;
~~~
[22:16:16.349]发→◇24 24 0B 00 FF FF 04 00 00 05 01 □ //录入person00,face0,待确认
[22:16:16.428]收←◆40 40 08 00 EB E4 84 00 
[22:16:17.819]收←◆40 40 08 00 2A 79 84 09 
[22:16:19.128]发→◇24 24 0B 00 FF FF 04 00 01 05 01 □ //录入person00,face1,待确认
[22:16:19.227]收←◆40 40 08 00 EB E4 84 00 
[22:16:20.460]收←◆40 40 08 00 2A 79 84 09 
[22:16:21.789]发→◇24 24 0B 00 FF FF 04 00 02 05 01 □ //录入person00,face2,待确认
[22:16:21.867]收←◆40 40 08 00 EB E4 84 00 
[22:16:22.636]收←◆40 40 08 00 2A 79 84 09 
[22:16:25.424]发→◇24 24 08 00 FF FF 05 01 □ //确认之前的录入
[22:16:25.835]收←◆40 40 08 00 33 FD 85 00 
[22:16:40.166]发→◇24 24 07 00 FF FF 11 □    //
[22:16:40.204]收←◆40 40 0A 00 FA C9 91 06 00 01 
[22:16:41.063]发→◇24 24 07 00 FF FF 12 □
[22:16:41.131]收←◆40 40 14 00 3C AE 92 00 00 02 00 01 00 00 00 02 00 01 00 00 
~~~


### BINCMD_DEL 0x06
删除人脸指令，arg=person_id,face_idx	
person_id设为0xff，则删除所有人
face_id设为0xff，则删除该人的所有face
~~~
[18:43:06.065]发→◇24 24 07 00 FF FF 11 □        //查询人数
[18:43:06.171]收←◆40 40 0A 00 E8 EA 91 06 00 03 //3人，6张图片
[18:43:08.169]发→◇24 24 07 00 FF FF 12 □        //打印所有人信息
[18:43:08.187]收←◆40 40 14 00 0D 0F 92 00 00 00 00 01 00 02 01 00 01 01 02 00 
[18:43:17.661]发→◇24 24 09 00 FF FF 06 00 02 □  //删除person00的 02号图
[18:43:17.886]收←◆40 40 08 00 5B D7 86 00       //成功
[18:43:29.887]发→◇24 24 07 00 FF FF 11 □        //查询人数
[18:43:29.948]收←◆40 40 0A 00 8C 05 91 05 00 03 //成功减为3人，5张图
[18:43:31.614]发→◇24 24 07 00 FF FF 12 □        //打印详情
[18:43:31.659]收←◆40 40 12 00 54 37 92 00 00 00 00 01 01 00 01 01 02 00 
[18:43:33.733]发→◇24 24 09 00 FF FF 06 00 FF □  //删除person00的所有图片
[18:43:33.899]收←◆40 40 08 00 5B D7 86 00       //成功
[18:43:35.797]发→◇24 24 07 00 FF FF 11 □        //查询人数
[18:43:35.851]收←◆40 40 0A 00 DC C2 91 03 00 02 //成功变为2人，3张图
[18:43:37.797]发→◇24 24 07 00 FF FF 12 □        //打印详情
[18:43:37.868]收←◆40 40 0E 00 7A 69 92 00 01 00 01 01 02 00 
~~~

### BINCMD_FR_RUN 0x07
开始/停止人脸识别，arg=output_type (0 stop, 1 output only id, 2 output id&ftr)
~~~
[22:52:36.525]发→◇24 24 08 00 FF FF 07 01 □  //开启人脸识别，设置仅上报id，可以观察到红外灯亮起
[22:52:36.639]收←◆40 40 08 00 83 CE 87 00 
[22:52:38.958]收←◆40 40 0B 00 22 F0 08 01 01 00 02  //识别到录入的人脸，上报，总共一个脸，当前第一个，person00,face02
[22:52:39.166]收←◆40 40 0B 00 22 F0 08 01 01 00 02  //第二帧上报，时差约0.2s，其中有0.1s是停顿在UI显示，可调整
[22:52:39.422]收←◆40 40 0B 00 22 F0 08 01 01 00 02  //第三帧
[22:52:41.598]收←◆40 40 0B 00 22 F0 08 01 01 00 02  
[23:06:44.488]收←◆40 40 0B 00 88 23 08 01 01 FF FF  //FF FF 表示陌生人
[23:06:44.648]收←◆40 40 0B 00 88 23 08 01 01 FF FF 
[22:52:49.471]发→◇24 24 08 00 FF FF 07 02 □         //设置上报id及特征值
[22:52:49.534]收←◆40 40 08 00 83 CE 87 00           //下面回复了当前图像中脸的特征值(196B,也可设置为192/128精简版)
[22:52:50.782]收←◆40 40 CF 00 BE F5 08 01 01 00 00 20 03 0D 1D 24 B9 DD 00 D2 D4 DA E7 E2 51 09 2C E9 15 24 07 E3 32 DF D4 FA 1F EF 0C 3B 45 C6 DD E8 D0 05 EB 13 FB D2 F0 25 F9 FD EF D2 B7 EB 46 22 FF E7 2C E6 C0 04 26 1B 1A 47 CF BC 01 57 00 FA 13 13 19 1D 24 15 38 14 1A 01 13 1C EF 00 F3 F9 FB C4 FF DA F3 26 BE F9 05 F8 F1 D3 E1 BE D8 1F AF 3A BA F9 1B 06 0B FD 23 0B 2E 07 01 0F DD 4D 44 57 F3 FD 1B F8 FB 0C 15 DD BD EB 21 3C 00 09 B7 E4 D5 14 E3 18 21 00 E3 FF ED B9 DC 00 00 3C C8 02 39 0B E5 13 FF 0F 14 FF 17 EF FB CF 15 F3 34 FA 19 ED E2 32 FA E3 3C C6 C6 DA D2 DC 14 ED 27 DC 06 19 27 09 F6 1B F8 FB DA 24 02 FD AF E4 F5 05 0F 
[22:52:57.997]发→◇24 24 08 00 FF FF 07 00 □  //停止人脸识别，可以观察到红外灯关闭
[22:52:58.127]收←◆40 40 08 00 83 CE 87 00 
~~~

### BINCMD_FR_RES 0x08
模块上报的识别结果，每次一个，多人多次返回
arg=i,n,person_id,face_idx,[ftr]
i, 当前画面中的第i张脸（i从1开始）
n，当前画面总共有多少张脸
person_id, face_idx: 人员及人脸ID，0xff表示陌生人
ftr：可选输出特征值

输出示例见上一节
							
### BINCMD_FR_GATE 0x09
设置人脸识别的参数，比对阈值(0~100,建议80~90)，活体阈值(0~100，建议60~80)，是否需要正视(0/1),[可选]红外识别阈值
arg=compare_gate,live_gate,front_gate,[fe_gate_ir]

~~~
[23:17:37.924]发→◇24 24 0A 00 FF FF 09 5A 50 00 □
[23:17:37.983]收←◆40 40 08 00 93 54 89 00 
~~~


### BINCMD_LED 0x0a
LED操作，注意在开启FR_RUN时，会受内部逻辑控制
arg=wled_duty wled有效值为0~255
~~~
[23:27:57.141]发→◇24 24 08 00 FF FF 0A 80 □ //设置白光亮度为一半亮度
[23:27:57.270]收←◆40 40 08 00 FB 7E 8A 00   //回应ok
~~~

### BINCMD_RELAY 0x0b
设置继电器开启一段时间
arg=time,polarity 继电器IO的脉冲时间，单位为0.1s
~~~
[23:33:18.343]发→◇24 24 08 00 FF FF 0B 0A □        //继电器开启1s
[23:33:18.415]收←◆45 38 33 40 40 08 00 23 67 8B 00 //回应ok
~~~

### BINCMD_RSTCFG 0x0c
复位板卡配置到默认状态
发送后需要重启板卡生效
~~~
[18:17:56.489]发→◇24 24 07 00 FF FF 0C □
[18:17:56.565]收←◆40 40 08 00 F5 5E 8C 00 
~~~


### BINCMD_IMPORT 0x10
导入人脸特征值
arg=person_id,face_idx,face_ftr(196B default)
~~~
[01:39:02.487]发→◇24 24 CD 00 FF FF 10 00 00 19 F1 26 3E 2A BA FD 0F CB DE D0 F7 15 4B 14 0F 00 FB 32 18 CC 2B 00 D0 CB 0C F6 1F 37 41 E1 F1 01 B4 07 DB 20 01 D5 D9 28 D3 0F 0C FC D0 E3 56 02 05 E5 31 D8 AF EA 14 2D 0E 23 C4 A9 0E 44 11 D8 0D 28 0D 18 1F 17 1B 1E 19 03 0A 25 EA 00 05 06 10 CF 03 E0 F1 23 A9 02 1C 09 07 DF D6 D5 D1 1C DB 25 C9 E7 1C EA 17 F8 F9 FD 3A 18 05 0F F4 57 57 5A F5 F1 2D F8 11 2B 02 E0 D1 00 1C 35 00 00 C7 E9 EC 0E E4 1B 16 EE C2 12 07 C6 EF F8 07 45 CA EF 25 07 F4 20 E2 0A 04 2A 1F E7 FF D8 1C EC 19 F9 0B FE 0A 38 25 05 2A BC B0 E3 BD CB 11 17 12 D9 FC 19 17 F8 F7 18 02 11 FA 16 11 00 B2 E9 EE EE 0C □  //导入一张图片
[01:39:02.613]收←◆40 40 08 00 1A 16 90 00    //返回成功
[01:39:11.741]发→◇24 24 08 00 FF FF 07 01 □  //测试识别
[01:39:11.781]收←◆40 40 08 00 83 CE 87 00 
[01:39:13.446]收←◆40 40 0B 00 30 D3 08 01 01 00 00   //成功使用导入的特征值识别
[01:39:13.654]收←◆40 40 0B 00 30 D3 08 01 01 00 00 
~~~

### BINCMD_FCNT 0x11
查询人脸库数量指令
模块返回参数：arg=all_cnt(2B), person_cnt(1B)
~~~
[18:43:06.065]发→◇24 24 07 00 FF FF 11 □        //查询人数
[18:43:06.171]收←◆40 40 0A 00 E8 EA 91 06 00 03 //3人，6张图片
~~~

### BINCMD_FLIST 0x12
打印人脸库所有的person_id和face_idx
模块返回格式：errcode+[person_id,face_idx]*N  
~~~
[18:43:08.169]发→◇24 24 07 00 FF FF 12 □        //打印所有人信息
[18:43:08.187]收←◆40 40 14 00 0D 0F 92 00 00 00 00 01 00 02 01 00 01 01 02 00 
~~~

### BINCMD_FTR 0x13
查询对应人脸的特征值
in arg  = person_id, face_idx
out arg = err_code,  person_id, face_idx, face_ftr 
~~~
[23:36:30.901]发→◇24 24 09 00 FF FF 13 00 00 □ //以下返回：err=0, person00,face00, faceftr(196B)
[23:36:30.919]收←◆40 40 CE 00 67 6E 92 00 00 00 19 F1 26 3E 2A BA FD 0F CB DE D0 F7 15 4B 14 0F 00 FB 32 18 CC 2B 00 D0 CB 0C F6 1F 37 41 E1 F1 01 B4 07 DB 20 01 D5 D9 28 D3 0F 0C FC D0 E3 56 02 05 E5 31 D8 AF EA 14 2D 0E 23 C4 A9 0E 44 11 D8 0D 28 0D 18 1F 17 1B 1E 19 03 0A 25 EA 00 05 06 10 CF 03 E0 F1 23 A9 02 1C 09 07 DF D6 D5 D1 1C DB 25 C9 E7 1C EA 17 F8 F9 FD 3A 18 05 0F F4 57 57 5A F5 F1 2D F8 11 2B 02 E0 D1 00 1C 35 00 00 C7 E9 EC 0E E4 1B 16 EE C2 12 07 C6 EF F8 07 45 CA EF 25 07 F4 20 E2 0A 04 2A 1F E7 FF D8 1C EC 19 F9 0B FE 0A 38 25 05 2A BC B0 E3 BD CB 11 17 12 D9 FC 19 17 F8 F7 18 02 11 FA 16 11 00 B2 E9 EE EE 0C 
~~~

### BINCMD_FTRALL 0x14
导出所有人脸信息，一般用于上位机的导出所有信息，然后导到其他机器。
arg=errcode,[person_id,face_idx,face_ftr]*N

~~~
[23:40:42.566]发→◇24 24 07 00 FF FF 14 □
[23:40:42.646]收←◆40 40 AC 04 9E AD 92 00   //以下返回了存储的6个脸，分属于3个人
00 00 19 F1 26 3E 2A BA FD 0F CB DE D0 F7 15 4B 14 0F 00 FB 32 18 CC 2B 00 D0 CB 0C F6 1F 37 41 E1 F1 01 B4 07 DB 20 01 D5 D9 28 D3 0F 0C FC D0 E3 56 02 05 E5 31 D8 AF EA 14 2D 0E 23 C4 A9 0E 44 11 D8 0D 28 0D 18 1F 17 1B 1E 19 03 0A 25 EA 00 05 06 10 CF 03 E0 F1 23 A9 02 1C 09 07 DF D6 D5 D1 1C DB 25 C9 E7 1C EA 17 F8 F9 FD 3A 18 05 0F F4 57 57 5A F5 F1 2D F8 11 2B 02 E0 D1 00 1C 35 00 00 C7 E9 EC 0E E4 1B 16 EE C2 12 07 C6 EF F8 07 45 CA EF 25 07 F4 20 E2 0A 04 2A 1F E7 FF D8 1C EC 19 F9 0B FE 0A 38 25 05 2A BC B0 E3 BD CB 11 17 12 D9 FC 19 17 F8 F7 18 02 11 FA 16 11 00 B2 E9 EE EE 0C 
00 01 1B E9 26 39 20 B4 EF 0A DA E0 C7 EB 00 45 15 12 00 FB 33 15 DE 26 00 DC D5 12 F7 13 3F 3E C6 DE F5 C1 11 F3 28 01 D0 E5 27 CA 1B 13 01 C7 F6 51 00 FB E8 1C D6 B4 E3 17 2A 25 2C C8 B4 00 43 0D E9 0F 30 14 23 30 15 27 23 28 07 14 26 EF 02 0A 20 18 D9 09 E6 ED 23 A7 10 08 08 05 D8 D8 C6 C8 21 D8 1B CE 00 1A F3 11 F1 04 ED 3C 0F 00 FC E3 54 46 5E FA DE 1C ED 10 33 0D D9 D8 FE 23 46 01 FC B7 E9 F8 06 F3 23 10 F8 C4 12 F6 CD F8 FD 01 3C C7 F1 2B 0D ED 15 F6 02 09 2B 26 F2 18 E0 16 E2 1E E9 FC FB F7 34 15 EF 2B B9 C5 EF B0 CF 0B 0D 21 D9 FF 23 20 F5 FA 18 0B FB E2 17 1D FA B2 EB 04 F7 18 
00 02 1F F8 1D 2B 33 B6 ED 06 D2 E8 C9 F2 12 54 0E 28 F0 0C 30 20 E5 2E FB DB D8 05 F2 10 3F 3B E0 F5 F8 B0 0C E0 0E FE D8 E5 24 DB 12 09 E2 C0 E9 46 F9 0A E8 2D E6 B6 E9 16 2C 0C 33 C3 A9 0C 4D 13 DB 11 2E 1E 0D 1A 0E 31 11 2D 04 FD 1C E8 FE 04 06 0B D0 FA E8 EF 20 AA 0C 18 02 07 E2 E2 CF C9 23 D7 20 C6 ED 0E F7 14 FD 00 03 32 09 01 0E F2 46 56 5D F1 EF 30 02 10 2E 0E CF D6 FB 29 47 04 02 C7 E3 E2 09 E3 28 1E EB CD FC 03 D4 E7 F9 11 51 BF 00 25 06 ED 11 E0 09 03 20 28 E5 08 DA 1F EA 1A F0 03 FD 08 29 16 F1 3B BE B7 F9 AA DB 22 0A 22 E4 00 09 25 03 ED 1A 04 09 F8 0F 13 09 B5 D0 01 F4 09 
01 00 12 EB 1E 3B 2C B6 FE 0A D2 E3 CC F3 02 4D 1B 0B 01 F3 37 1A D9 20 05 DE CF 16 FB 25 44 3C DC E6 FB C4 0D F0 27 02 D4 E7 28 D0 0E 16 0B CE E9 5C FB 0D E8 28 D5 C0 E3 0A 1F 10 2B CD AB 0D 42 16 D9 0A 2B 0E 25 38 0A 15 1D 1A 08 15 23 F3 F9 03 0B 15 D5 06 E2 E6 20 A7 0D 0D 0C FF DD D3 D1 C8 22 E4 28 C8 E6 17 E8 20 F2 08 FB 39 1F FE 08 E3 53 48 56 E9 E8 20 F2 12 30 0F DF CA FE 26 45 05 02 B8 E7 E3 04 F2 2C 1C F4 CD 09 FF C2 00 07 FB 38 CA EB 28 06 F0 26 E2 08 02 24 20 EA 0E D6 2E E3 1A EF 0E 04 00 38 18 FA 21 BD B4 E4 BA D0 09 0D 14 DD FE 20 28 F4 FC 1D 0B 09 F3 20 0D FE AF EC 09 EE 0A 
01 01 2E F7 26 3F 26 B1 FE FC E1 D8 D1 EC 07 44 17 07 FC 0C 41 18 C7 27 03 EA C3 07 EF 12 46 2E D7 E8 00 BC 03 F6 20 0C CC E3 24 DA 0D 06 09 D1 F6 5C EE 07 EB 3E C6 A9 E6 14 3A 22 2F C4 AB 1D 41 26 DE 1A 22 14 1B 29 07 15 18 15 07 17 20 E5 F9 07 0F 07 D9 F8 F1 EE 20 B0 0C 0C 0B 02 DD E4 D0 CC 26 D5 1D C5 E9 10 E3 1D 00 0A E8 35 0D FE 09 ED 4D 45 4F FD F2 29 F2 0F 32 10 E2 CE F4 1F 3A 0C 07 D2 D8 F6 0A DC 2C 1B E4 C6 14 FB CD FC F9 04 3A D7 F7 13 05 EF 1B E1 FE 0E 45 24 DE 0F CD 19 E4 1D F1 09 F3 FD 31 24 FD 32 C4 B6 EB B3 CD 1F 1A 1A D5 FF 04 15 F9 F8 1A FC 09 F3 15 18 F5 BE E3 FC F6 11 
02 00 0D EC 27 24 34 C3 E3 02 EE E1 CE 02 F6 2F 14 28 08 00 19 23 DB 18 0B CF E1 04 E6 1A 3F 42 DB F3 FE C8 0E EC 25 EE EC ED 1D CC 19 08 F2 C6 D8 4F FF 0C F5 29 D7 A9 E3 1F 20 28 2E DE A5 EE 52 0E D2 25 1F 22 15 22 10 17 28 37 11 0B 19 EC F7 0F 22 19 CF FE E9 E0 27 A5 05 02 14 FA EB D1 D0 E6 0F C9 13 BC 15 14 EC 0B FE 05 F7 4E 18 14 02 EC 4B 38 62 ED F1 1D F2 0B 3D 00 D7 DA 00 29 34 F6 02 AD EF E3 0F EB 23 0F 09 C5 F8 FB BE DB 16 15 31 D1 F4 2A 09 E9 26 F4 0C 02 2E 22 0D 14 E6 0B E2 17 E2 FD FE F8 27 14 F5 3A B6 B8 02 A6 E6 06 0E 45 E5 0A 14 1E 11 E5 23 00 14 F3 1A 14 FE BD DE 09 F9 0B 
~~~

### BINCMD_QRSCAN 0x15
开启扫描二维码，arg=timeout_s

~~~
24 24 08 00 FF FF 15 0A
~~~

### BINCMD_QRRES 0x16
二维码返回结果,qrcode以00结尾
arg=err_code+[qrcode]

### BINCMD_FACEPOS 0x17
模块上报人脸坐标信息，每次一人，多人多次返回
arg=i,n,l_eye_x, l_eye_y, r_eye_x, r_eye_y, nose_x, nose_y, l_mouth_x, l_mouth_x, r_mouth_x, r_mouth_y, face_w, face_h

i, 当前画面中的第i张脸（i从1开始）

n，当前画面总共有多少张脸

person_id, face_idx: 人员及人脸ID，0xff表示陌生人

坐标原点是人脸框左上角


### BINCMD_PICADD 0x20
在屏幕上显示图片，需要预先在flash中写入图片资源。用户指定ID，后面使用对应ID来删除
arg=id(1B),alpha(1B),,resize(1B)addr(4B),w(2B),h(2B),x(2B),y(2B)
所有参数为小端存储。
id为用户设置的图片资源id号，0~254。注意如果id重复，会被新设置的图片取代。
alpha=0 不透明; =255 全透明
resize=1 图片2x2缩放

> 注意:MF1，横屏的x需要加40偏移，竖屏的y需要加40偏移

~~~
[23:49:56.446]发→◇24 24 15 00 FF FF 20 00 80 00 0C C7 00 F0 00 F0 00 00 00 24 00 □
[23:49:56.518]收←◆40 40 08 00 B8 A0 A0 00  //可见屏幕上半透明叠加了一张图片
[00:45:25.453]发→◇24 24 15 00 FF FF 20 01 80 00 00 C0 00 10 00 10 00 00 00 29 00 □
[00:45:25.509]收←◆40 40 08 00 B8 A0 A0 00  //不透明地叠加图片

~~~

### BINCMD_STRADD 0x21
在屏幕上显示字符串
arg=id(1B),x(2B),y(2B),size(16/32),color(RGB565),bg_color(RGB565),zhCN(1B),String(nB)
id：表示资源id，与图片公用0~254的id号空间。
zhCN表示字符串中是否包含中文字符，如果包含中文字符，需要GB2312编码。
String本身的长度信息包含在帧头的长度中，但也需要以 00 结尾

> 矽     速     科     技        @      你     好     世     界
> CE F9 CB D9 BF C6 BC BC 20 40 20 C4 E3 BA C3 CA C0 BD E7  

~~~
[01:24:37.853]发→◇24 24 18 00 FF FF 21 02 00 00 40 00 10 FF FF 00 00 00 31 32 33 34 35 00 □ //黑底白字显示'12345'
[01:24:37.974]收←◆40 40 08 00 60 B9 A1 00 
[01:24:46.389]发→◇24 24 26 00 FF FF 21 03 00 00 80 00 10 00 F8 FF FF 01 CE F9 CB D9 BF C6 BC BC 20 40 20 C4 E3 BA C3 CA C0 BD E7 00 □  //白底红字显示'矽速科技 @ 你好世界'
[01:24:46.501]收←◆40 40 08 00 60 B9 A1 00 
~~~


### BINCMD_DISDEL 0x22
删除指定id图片  
arg=id;	255表示删除所有图片。
~~~
[00:46:55.708]发→◇24 24 08 00 FF FF 22 FF □  //接上节内容执行，可见屏幕上所有内容被清空
[00:46:55.766]收←◆40 40 08 00 08 93 A2 00 
~~~

### BINCMD_REBOOT 0x23
重启设备
arg=key; 固定为0xD9
```
发-> 24 24 08 00 FF FF 23 D9
收-> 40 40 08 00 2D 48 A3 00
```

### BINCMD_SOFT_CFG 0x24
读取/设置软件配置
arg=get_cfg,cam_flip,cam_mirror,lcd_flip,lcd_mirro,uartp_out_fea,resv,resv,resv,uartp_out_interval_ms

当get_cfg=0x01时表示读取当前配置,模块回复的顺序与设置的参数一致,get_cfg为0xD9

当get_cfg!=0x01时表示进行设置,模块回复设置结果,0x00表示成功,其他值为失败

```
发-> 24 24 11 00 FF FF 24 01 00 00 00 00 00 00 00 00 00 
收-> 40 40 11 00 20 92 A4 D9 01 00 00 00 00 00 00 00 64 
```

### BINCMD_HARD_CFG 0x25
读取/设置硬件配置
arg=get_cfg,port_tx,port_rx,log_tx,log_rx,relay_pin,relay_pol,relay_opent,key_pin,key_pol

当get_cfg=0x01时表示读取当前配置,模块回复的顺序与设置的参数一致,get_cfg为0xD9

当get_cfg!=0x01时表示进行设置,模块回复设置结果,0x00表示成功,其他值为失败

```
发-> 24 24 11 00 FF FF 25 01 00 00 00 00 00 00 00 00 00 
收-> 40 40 11 00 B3 97 A5 D9 05 04 0A 0B 0D 01 14 18 01 
```

### BINCMD_PIC_CFG 0x26
设置串口图传功能
arg=get_cfg(1B),tx(1B),baud(4B)

当get_cfg=0x01时表示读取当前配置,模块回复的顺序与设置的参数一致,get_cfg为0xD9

当get_cfg!=0x01时表示进行设置,模块回复设置结果,0x00表示成功,其他值为失败

tx 为`255`禁用图传功能

baud 限制最大值为3M

```
发-> 24 24 0D 00 FF FF 26 01 00 00 00 00 00 //读取配置
收-> 40 40 0D 00 AA B7 A6 00 1E 00 0E 10 00 

发-> 24 24 0D 00 FF FF 26 00 1E 00 0E 10 00 //设置IO30,Baud 921600
收-> 24 24 0D 00 FF FF 26 00 1E 00 0E 10 00
```

## 附录
### CRC16代码参考
~~~
uint16_t crc16_xmodem(const uint8_t *buffer, uint32_t buffer_length)
{
    uint8_t c, treat, bcrc;
    uint16_t wcrc = 0;

    for(uint32_t i = 0; i < buffer_length; i++)
    {
        c = buffer[i];
        for(uint8_t j = 0; j < 8; j++)
        {
            treat = c & 0x80;
            c <<= 1;
            bcrc = (wcrc >> 8) & 0x80;
            wcrc <<= 1;
            if(treat != bcrc)
                wcrc ^= 0x1021;
        }
    }
    return wcrc;
}
~~~

### MF模块 内置默认图片资源地址
~~~
#define PIC_ICON_WIFI_ADDR	(0xc00000)
#define PIC_ICON_WIFI_SIZE	(16 * 16 * 2)

#define PIC_ICON_ETH_ADDR	(0xc00200)
#define PIC_ICON_ETH_SIZE	(16 * 16 * 2)

#define PIC_LOGO_RECORD_ADDR	(0xc00400)
#define PIC_LOGO_RECORD_SIZE	(240 * 240 * 2)

#define PIC_LOGO_CONNING_ADDR	(0xc1c600)
#define PIC_LOGO_CONNING_SIZE	(240 * 240 * 2)

#define PIC_LOGO_CONN_FAIL_ADDR	(0xc38800)
#define PIC_LOGO_CONN_FAIL_SIZE	(240 * 240 * 2)

#define PIC_LOGO_CONN_OK_ADDR	(0xc54a00)
#define PIC_LOGO_CONN_OK_SIZE	(240 * 240 * 2)

#define PIC_LOGO_QR_SHOW_ADDR	(0xc70c00)
#define PIC_LOGO_QR_SHOW_SIZE	(240 * 240 * 2)

#define PIC_LOGO_QR_ERR_ADDR	(0xc8ce00)
#define PIC_LOGO_QR_ERR_SIZE	(240 * 240 * 2)

#define PIC_LOGO_QR_TO_ADDR	(0xca9000)
#define PIC_LOGO_QR_TO_SIZE	(240 * 240 * 2)

#define PIC_LOGO_PASS_ADDR	(0xcc5200)
#define PIC_LOGO_PASS_SIZE	(240 * 286 * 2)

#define PIC_BAR_480214_ADDR	(0xce6a40)
#define PIC_BAR_480214_SIZE	(480 * 214 * 2)

#define PIC_BAR_24080_ADDR	(0xd18cc0)
#define PIC_BAR_24080_SIZE	(240 * 80 * 2)

#define PIC_BAR_360160_ADDR	(0xd222c0)
#define PIC_BAR_360160_SIZE	(360 * 160 * 2)

#define PIC_BAR_160480_ADDR	(0xd3e4c0)
#define PIC_BAR_160480_SIZE	(160 * 480 * 2)

#define PIC_BAR_480160_ADDR	(0xd63cc0)
#define PIC_BAR_480160_SIZE	(480 * 160 * 2)
~~~
	
