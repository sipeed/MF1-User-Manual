# MF1 binary serial port protocol Manual (Json) `V2.0.1`

## **Change log**

| Version | | Revision datedescription |
| -------- | ------------ | ------------- |
| `0.2` | `2020.06.01` | |
| `0.1` | `2019.09.05` | |



## 1. Serial communication convention

| Parameter description | Default value |
| --------------------- | ------------- |
| Baud rate | 115200 |
| Data bits | 8 |
| Parity bit | None |
| Stop bit | 1 |
| Data Flow Control | None |

## Hardware connection

| MF1 Module | Description |
| ------ |----------------------------- |
| `IO5` | he `TX` of the protocol serial port, can be set, the default is `5`, and the default baud rate is `115200` |
| `IO4` | `RX` of protocol serial port, can be set, default `4` |
| `IO11` | he `TX` of the debug serial port, can be set, the default is `5`, and the default baud rate is `115200` |
| `IO10` | `RX` of debug serial port, can be set, default `4` |
| `IO24` | Short press to enter the face, which can be set, the default is `24`<br/>(long press to clear the facial feature value requires burning special firmware) |
| `IO13` | Relay normally high output, can be set, default is `13` |
| `IO12` | Relay normally low output, can be set, default is `12` |

## `Json` Protocol Format

```json
{"version":$protocol_version,"type":"cmd_type","code":0,"msg":"msg","param":{"xx":"xx","xx":xx}} \r\n
```

#### Description

-current `protocol_version` is `2`

-The end of the packet must be added `\r\n`

-`\r\n` is not allowed in the middle of the packet

> Note that `\r\n` should be escaped as **0x0D 0x0A**

### Command: `cmd_type`

| Command: `cmd_type` | Description |
| ---------- | ---------- |
| [`init`](#Initialization complete) | Module sends initialization complete message |
| [`pkt_prase_failed_ret`](#Packet parsing error message) | Packet parsing error message |
| [`ping`](#Check module) | Check if the module exists |
| [`pong`](#Check module result) | Check whether the module has a result |
| [`face_info`](#Output face information) | Output face information after face recognition |
| [`face_pos`](#Detected face) | Detected face (stranger) coordinate information |
| [`cal_pic_fea`](#Calculate the face feature value of the picture) | Calculate the face feature value of the `Jpeg` picture |
| [`cal_pic_fea_ret`](#Calculate the facial feature value result of the picture) | Calculate the facial feature value result of the `Jpeg` picture |
| [`add_user_by_fea`](#Add user by feature value) | Add user by feature value |
| [`add_user_by_fea_ret`](#Add user results by feature value) | Add user results by feature value |
| [`add_user_spec_uid`](#Add user specified UID) | Add user and specify `UID` |
| [`add_user_spec_uid_ret`](#Add user specified UID result) | Add user and specify `UID` result |
| [`del_user_by_uid`](#Delete user by UID) | Delete user by `UID` |
| [`del_user_by_uid_ret`](#Delete user result by UID) | Delete user result by `UID` |
| [`query_face`](#Query module to store face information) | Query the face information stored in the module |
| [`query_face_ret`](#Query module to store face information results) | Query module to store face information results |
| [`set_lcd_display`](#Set screen display) | Set screen display string or picture |
| [`set_lcd_display_ret`](#Set screen display result) | Set screen display string or picture result |
| [`clr_lcd_display`](#Delete screen display) | Delete screen display elements |
| [`clr_lcd_display_ret`](#Delete screen display result) | Delete screen display element result |
| [`brd_hard_cfg`](#Set module hardware configuration) | Set module hardware configuration |
| [`brd_hard_cfg_ret`](#Set the module hardware configuration result) | Set the module hardware configuration result |
| [`brd_soft_cfg`](#Set module software configuration) | Set module software configuration |
| [`brd_soft_cfg_ret`](#Set module software configuration result) | Set module software configuration result |
| [`set_notify`](#Set to notify strangers) | Set whether to notify strangers |
| [`set_notify_ret`](#Set notification results to strangers) | Set whether to notify strangers of information results |
| [`query_uid`](#Query whether the UID exists) | Query whether the specified UID exists |
| [`query_uid_ret`](#Query whether the UID has a result) | Query whether the specified UID has a result |
| [`face_recon`](#Set whether to perform face recognition) | Set whether to perform face recognition |
| [`face_recon_ret`](#Set whether to perform face recognition results) | Set whether to perform face recognition results |
| [`qrscan`](#Scan QR code) | Module scan QR code |
| [`qrscan_ret`](#QR code scanning result) | QR code scanning result |
| [`restore`](#Restore factory settings) | Restore factory settings |
| [`restore_ret`](#Restore factory settings result) | Restore factory settings result |
| [`reset`](#Control device restart) | Control device restart |
| [`reset_ret`](#Control device restart result) | Control device restart result |
| [`pic_stream_cfg`](#Picture transmission serial port configuration) | Picture transmission serial port configuration |
| [`pic_stream_cfg_ret`](#Picture transmission serial port configuration result) | Picture transmission serial port configuration result |

> Above `cmd` can click to jump

<div STYLE="page-break-after: always;"></div>

## **letter of agreement**

### **loading finished**

```json
{
    "version": 2,
    "type": "init",
    "code": 0,
    "msg": "init done",
    "proto": "0.1"
}
```

#### Description

Module startup completed

<br/>
<br/>

### **Data packet parsing error message**

```json
{
    "version": 2,
    "type": "pkt_prase_failed_ret",
    "msg": "json prase failed",
    "code": 1,
    "cmd": "unknown"
}
```

#### Description

Return after receiving the wrong data packet and point out the wrong place, mainly used to assist in troubleshooting

> There is a spelling error here, but for compatibility, it will not be corrected

<br/>
<br/>

### **Check Module**
```json
{
    "version": 2,
    "type": "ping"
}
```

#### Description

The host initiates a ping command to check whether the module is online

### **Check module results**
```json
{
    "version": 2,
    "type": "pong",
    "msg": "i am here",
    "code": 0
}
```

#### Description

Reply to fixed content

### **Output face information**

```json
{
    "version": 2,
    "type": "face_info",
    "code": 0,
    "msg": "have face",
    "info": {
        "pic": "540A730200000000",
        "total": 1,
        "current": 0,
        "x1": 34,
        "y1": 34,
        "x2": 171,
        "y2": 178,
        "score": 0,
        "uid": "null",
        "feature": "feature base64 encode or null"
    }
}
```

#### Description

`pic`: Used to determine whether there are multiple faces in the same picture

`total`: The total number of faces in this recognition

`current`: The `N` face in this recognition (counting from `0`)

`x1`: the upper left corner of the face coordinate frame `x`

`y1`: the upper left corner of the face coordinate frame `y`

`x2`: the lower right corner of the face coordinate box `x`

`y2`: the lower right corner of the face coordinate frame `y`

`score`: face matching value (0 when directly outputting feature values)

 `uid`: `UID` corresponding to the face (`null` when directly outputting the feature value)

`feature`: face feature value, configurable whether to output (null when not output)

<br/>
<br/>

### **Face Detected**

```json
{"version":2,"type":"face_pos","code":0,"msg":"face position","x1":31,"y1":0,"x2":138,"y2 ":139,"lex":42,"ley":54,"rex":107,"rey":46,"nx":82,"ny":82,"lmx":60,"lmy": 119,"rmx":110,"rmy":115,"index":2,"total":1}
```

#### Description

`total`: The total number of faces in this recognition

`index`: The `N` face in this recognition (counting from `0`)

`x1`: the upper left corner of the face coordinate frame `x`

`y1`: the upper left corner of the face coordinate frame `y`

`x2`: the lower right corner of the face coordinate box `x`

`y2`: the lower right corner of the face coordinate frame `y`

`lex`: Five key points, left eye coordinate `x`
`ley`: Five key points, left eye coordinate `y`

`rex`: Five key points, right eye coordinate `x`
`rey`: Five key points, right eye coordinate `y`

`nx`: Five key points, mouth coordinates `x`
`ny`: Five key points, mouth coordinates `y`

`lmx`: Five key points, coordinates of the left mouth corner `x`
`lmy`: Five key points, the coordinates of the left mouth corner `y`

`rmx`: Five key points, the coordinates of the right mouth corner `x`
`rmy`: Five key points, the coordinates of the right mouth corner `y`

> If `total` conflicts with `index`, the index shall prevail

### **Calculate the facial feature value of the picture**

```json
{
    "version": 2,
    "type": "cal_pic_fea",
    "img": {
        "size": 10152,
        "auto_add":0,
        "sha256": "E65083CFEEEA8F377094C2297E8D3691C23AA8BAD33A82B5E4E4981914FFAC74",
        "uid":"0A6F4FB4000000000000000000000000"
    }
}
```

#### Description

`threshold`: face detection threshold, optional, default is `70`

`size`: The size of the Jpeg picture, **note, the maximum support for 30K pictures**

`auto_add`: automatically add the user to the module after the recognition is successful (the default is not added, then the returned `UID` is all `0`)

`sha256`: `sha256` checksum of `Jpeg` image (both `7zip` and `haozip` support calculation)

 `uid`: If you choose to automatically add to the module, the specified `uid` will be used

You can start sending the picture after receiving the following return content (`code` is 1), and it must be sent within `10s`. Exit and accept `jpeg` status after timeout

```json
{"version":2,"type":"cal_pic_fea_ret","code":1,"msg":"please start send jpeg image","info":{"uid":"null","feature": "null"}}
```

> When the `code` in `info` is `1`, it means you can start sending `Jpeg` pictures

You can use `XCOM` or other serial port assistant's file sending function to load `Jpeg` file, and then select send

-NOTE: To obtain the file `sha256`, use the following command

>
> Windows cmd: certutil -hashfile `filename` SHA256
>
> Linux: sha256sum `filename`


<br/>
<br/>

### **Result of calculating facial feature value of picture**

```json
{
    "version":2,
    "type":"cal_pic_fea_ret",
    "code":0,
    "msg":"get feature success",
    "info":{
        "face_prob":0.90,
        "uid":"0A6F4FB4000000000000000000000000",
        "feature":"feature base64 encode"
    }
}
```

#### Description

`code`: status code

`msg`: return information

 `uid`: The `UID` of the face stored in the module, if you need to delete the corresponding face, you need this `UID`

`feature`: Feature value calculated by face (`base64 encode`)

`face_prob`: face detection score, normal value is a floating point number less than `1`

> In the [Calculate picture face feature value](#Calculate picture face feature value) data package, you can choose whether to automatically add users to the module

- status code

  `0`: Successful calculation of eigenvalues

  `1`: You can start sending `Jpeg` pictures

  `2`: Error parsing `Json`, the error will be pointed out in `msg`

  `3`: Module storage is full

  `4`: There are multiple faces in the picture

  `5`: There is no face in the picture (may be the direction is wrong, or the face is too small)

  `6`: `Jpeg` decoding failed (or the image is not `320x240` resolution)

  `7`: `sha256` verification of `Jpeg` file failed, or timeout waiting to receive the image

<br/>
<br/>

### **Add users by feature value**

```json
{
    "version":2,
    "type":"add_user_by_fea",
    "user":{
        "name":"B2E2CAD4",
        "uid":"EDE6E800A20000000000000000000000",
        "fea":"feature base64 encode"
    }
}
```

#### Description

`name`: Optional, name, support Chinese, no more than 4 Chinese characters, GB2312 code(Hex format)

`uid`: the user's `uid`

`fea`: user's facial feature value

### **Add user results by feature value**

```json
{
    "version":2,
    "type":"add_user_by_fea_ret",
    "code":0,
    "msg":"add user success",
    "uid":"EDE6E800A20000000000000000000000"
}
```

#### Description

`code`: status code

`msg`: return information

 `uid`: add the successful `uid`, if it fails, all are `0`

- status code

  `0`: added successfully

  `1`: `Json` parsing error

  `2`: Failed to save to `flash`

  `3`: `uid` already exists

<br/>
<br/>

### **Add user specified UID**

```json
{
    "version":2,
    "type":"add_user_spec_uid",
    "user":{
        "name":"B2E2CAD4",
        "uid":"EDE6E800A20000000000000000000000",
        "time_s":5,
    }
}
```

#### Description

> It is equivalent to entering a user by pressing a button, you can specify uid, and it will detect whether the user is positive

`name`: Optional, name, support Chinese, no more than 4 Chinese characters, GB2312 code

`uid`: The user specifies the `uid` of the newly added user

`time_s`: add user timeout time, default is `5`s, maximum is `100`

<br/>
<br/>

### **Add user specified UID result**

```json
{
    "version":2,
    "type":"add_user_spec_uid_ret",
    "user":{
        "uid":"EDE6E800A20000000000000000000000"
    }
}
```

#### Description

`msg`: execution result

`code`: status code

- status code

  `0`: success

  `1`: failure

  `2`: waiting to be added

<br/>
<br/>


### **Delete user by UID**

```json
{
    "version": 2,
    "type": "del_user_by_uid",
    "uid":"1BC6EB528C0000000000000000000000"
}
```

#### Description

 `uid`: the user uid that needs to be deleted

> Delete all users when `uid` is `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF` (32 `F`)

If it fails, there are specific instructions in the return result

<br/>
<br/>

### **Delete user result by UID**

```json
{
    "version":2,
    "type":"del_user_by_uid_ret",
    "code":3,
    "msg":"can not find user by uid"
}
```

#### Description

`msg`: execution result

`code`: status code

- status code

  `0`: Delete successfully

  `1`: `Json` parsing error, missing keywords

  `2`: `flash` operation failed

  `3`: Failed to find the user corresponding to `uid`

<br/>
<br/>

### **Query module to store face information**

```json
{
    "version":2,
    "type":"query_face",
    "query":{
        "total":1,
        "start":0,
        "end":10,
        "out_feature":0
    }
}
```

#### Description

`total`: Query how much face information is stored for `1`, `start`, `end` and `out_feature` have no meaning, `0` means to query the face UID from `start` to `end`

`out_feature`: Whether to output the corresponding feature value of the face information, it is not output by default (you can only check one at a time if you output the feature value)

`start`: start value of query interval

`end`: Query the end value of the interval

<br/>
<br/>

### **Query module to store face information results**

```json
{"version":2,"type":"query_face_ret","code":0,"msg":"query uid ands feature success","face":{"total":2,"start":0, "end":1,"info":[{"order":0,"uid":"22BCD239290000000000000000000000","feature":"feature bease64 encode"}...]}}
```

#### Description

`code`: status code

`msg`: return information

`face`:

-`total`: The total number of faces in the current module

-`start`: The starting value of the query result interval (counting from `0`)

-`end`: the end value of the query result interval

-`info`:

  -`order`: the order of the current face

  -`uid`: the `UID` of the current face

  -`feature`: the feature value of the current face

- status code

  `0`: query successful

  `1`: `Json` parsing error

  `2`: Return the number of faces stored in the current module when `total` is set to `1` in the query package

  `3`: Error reading the saved data from `flash`

<br/>
<br/>

### **Setting the screen display**

```json
{
    "version":2,
    "type":"set_lcd_display",
    "cfg":{
        "cfg_type":"str",
        "zhCN":0,
        "id":0,
        "x":0,
        "y":0,
        "size":16,
        "str":"abcd",
        "color":1,
        "bg_color":1
    }
}
```

```json
{
    "version":2,
    "type":"set_lcd_display",
    "cfg":{
        "cfg_type":"pic",
        "id":0,
        "x":0,
        "y":0,
        "w":320,
        "h":240,
        "addr":123456,
        "alpha":50,
        "resize":1
    }
}
```

#### Description

`cfg_type`: `str` or `pic`, set the superimposed picture or string

String display configuration:

  -`id`: `id` of the string, used when deleting, range [0-31]

  -`x`: The `x` coordinate of the display position of the string, **note that `MF1 1.3inch`, `0` need to be converted to `40`**

  -`y`: `y` coordinate of the string display position

  -`size`: currently supports `16` and `32`

  -`str`: The string to be displayed

  -`color`: string color, number type, `RGB565` encoding, `63488` means red

  -`bg_color`: String background color, number type, do not set background color when equal to `1`

  -`zhCN`: Whether the string is Chinese, <br>If the string is Chinese, `str` needs to be encoded with `base64`, <br>Currently, it supports the display of Chinese with `GB2312` encoding, and `ye7b2s75y9m/xry8` means `Shenzhen Silicon Speed ​​Technology`

Picture display configuration:

  -`id`: the `id` of the picture, used when deleting, range [0-31]

  -`x`: The picture shows the origin `x`, **note, `MF1 1.3inch`, `0` needs to be converted to `40`**

  -`y`: The picture shows the origin `y`

  -`w`: the width of the picture

  -`h`: The height of the picture

  -`addr`: The address where the image is saved in flash

  -`alpha`: Transparency of superimposed image and camera image

  -`resize`: Enlarge the picture 2x2, optional parameters

<br/>
<br/>

### **Set the screen display result**

```json
{
    "version":2,
    "type":"set_lcd_display_ret",
    "msg":"set lcd display success",
    "code":0,
    "id":0
}
```

#### Description

`id`: `id` of the content displayed on the screen

`msg`: message

`code`: code

  -`0`: success

  -`1`: failed

<br/>
<br/>

### **Delete screen display**

```json
{
    "version":2,
    "type":"clr_lcd_display",
    "id":0
}
```

#### Description

`id`: The `id` of the content displayed on the screen, delete all the content when the `id` is 1024

<br/>
<br/>

### **Delete screen display results**

```json
{
    "version":2,
    "type":"clr_lcd_display_ret",
    "msg":"clr lcd display success",
    "code":0,
    "id":0
}
```

#### Description

`id`: `id` of the content displayed on the screen

`msg`: message

`code`: code

  -`0`: success

  -`1`: failed

<br/>
<br/>

### **Set module hardware configuration**

```json
{
    "version":2,
    "type":"brd_hard_cfg",
    "cfg":{
        "get_cfg":0,
        "cfg_type":"lcd_cam",
        "lcd_flip":0,
        "lcd_mirror":0,
        "cam_flip":0,
        "cam_mirror":0
    }
}
```

```json
{
    "version":2,
    "type":"brd_hard_cfg",
    "cfg":{
        "get_cfg":0,
        "cfg_type":"uart_relay",
        "port_tx":10,
        "port_rx":11,
        "log_tx":5,
        "log_rx":4,
        "relay": 12,
        "relay_pol": 13,
        "key":24,
        "key_dir":1
    }
}
```

#### Description

`get_cfg`: read current configuration

<br/>

When `cfg_type` is `lcd_cam`, query or set the rotation of the module's screen and camera

`lcd_flip`: `lcd` display for vertical mirroring

`lcd_mirror`: `lcd` display for horizontal mirroring

`cam_flip`: `camera` for vertical mirroring

`cam_mirror`: `camera` for horizontal mirroring

<br/>

When `cfg_type` is `uart_relay`, query or set the module's serial port and relay configuration

`port_tx`: This module communicates with other modules `TX` pin, the default is `10`

`port_rx`: This module communicates with other modules `RX` pin, the default is `11`

`log_tx`: This module outputs log `TX` pin, the default is `5`

`log_rx`: This module outputs log `RX` pin, default is `4`

`relay`: Relay output pin

`relay_high`: Relay output effective level

`key`: key, default is `24`

`key_dir`: key press level, default is `1`

> Note that the module will not detect whether the set `IO` is the same, please ensure that the parameters are correct.<br>Restart to take effect

<br/>
<br/>

### **Set the module hardware configuration results**

```json
{
    "version":2,
    "type":"brd_hard_cfg_ret",
    "code":1,
    "msg":"get cfg success",
    "cfg":{
    }
}
```

#### Description

`msg`: message

`code`: code

  -`0`: success

  -`1`: failed

`cfg`: Refer to the [Set Module Hardware Configuration](#Set Module Hardware Configuration) command above

<br/>
<br/>

### **Set module software configuration**

```json
{
    "version":2,
    "type":"brd_soft_cfg",
    "cfg":{
        "get_cfg":0,
        "out_fea":0,
        "auto_out_fea":0,
        "pkt_fix":0,
        "out_interval_ms":100,
        "out_threshold":88.0,
        "out_threshold_ir": 58.0,
        "living_threshold": 70.0,
        "relay_open_s":2,
        "port_baud":115200
    }
}
```

#### Description

> `0` is off, `1` is on

`get_cfg`: read current configuration

`out_fea`: Whether to output the feature value if the recognition is successful, the default is `0`

`auto_out_fea`: Do not compare with the stored face library, and output when the face is recognized, the default is `0`

`out_interval_ms`: The interval between two output results, the unit is `ms`, the default is `100`, the maximum is `1000`

`out_threshold`: Face comparison output threshold (floating point number, max 100), default is `77.0`

`out_threshold_ir`: [Optional] Infrared face comparison output threshold (floating point number, max 100), default is `88.0`

`living_threshold`: Living body comparison threshold (floating point number), the default is `70.0`

`pkt_fix`: Whether to add headers and tails to the communication protocol and `CRC16` check, the default is `0`

`relay_open_s`: Relay open time, the unit is `s`, the default is `2`, the maximum is `100`

`port_baud`: communication serial port baud rate, default is `115200`

`out_fea` value description

  -`0`: Do not output characteristic values

  -`1`: Output characteristic value (the characteristic value stored in `flash`)

  -`2`: Output real-time characteristic value

When `auto_out_fea` is `1`, in the output face information, `uid` is `null` and `score` is `0`

> Restart to make the settings take effect

##### Open the communication format of `pkt_fix`

```C
0xAA 0x55 HI(LEN) LO(LEN) HI(CRC16) LO(CRC16)...(data)... 0x55 0xAA
```

You can use [http://www.ip33.com/crc.html](http://www.ip33.com/crc.html) to select `CRC-16/X25 x16+x12+x5+1`

<br/>
<br/>

### **Set module software configuration results**

```json
{
    "version":2,
    "type":"brd_soft_cfg_ret",
    "code":1,
    "msg":"get cfg success",
    "cfg":{
    }
}
```

#### Description

`msg`: message

`code`: code

  -`0`: success

  -`1`: failed

`cfg`: Refer to the [Setup Module Software Configuration](#Setup Module Software Configuration) command above

<br/>
<br/>

### **Set notification to strangers**

```json
{"version":2,"type":"set_notify","query":0,"en":1,"out_fea":0}
```

Description

> This command is not enabled by default, you need to compile the firmware yourself

`query`: Query current status1

`en`: `1` enable, `0 disable

`out_fea`:`1`Output the eigenvalues ​​of strangers,`0 `No output

### **Set up notification to strangers of results**

```json
{"version":2,"type":"set_notify_ret","code":0,"msg":"save cfg success","en":0,"out_fea":0}
```

#### Description

`msg`: execution result

`code`: code

  -`0`: success

  -`1`: Failed to parse the command

  -`2`: Unknown error


### **Query whether UID exists**
```json
{"version":2,"type":"query_uid","uid":"0E3D6BA9000000000000000000000000"}
```

#### Description
 `uid`: the uid to be queried

### **Check if UID exists or not**
```json
{"version":2,"type":"query_uid_ret","code":0,"msg":"uid exist","uid_id":1}
```

#### Description

`msg`: execution result

`uid_id`: `id` stored by `UID`, this can be used to query user information

`code`: status code

- status code
  `0`: `UID` exists

  `1`: `UID` does not exist

  `2`: Parsing error

### **Set whether to perform face recognition**
```json
{"version":2,"type":"face_recon","query_stat":0,"set_stat":1, "set_block":1}
```

#### Description

`query_stat`: Query the current status of face recognition, `0` disable, `1` enable

`set_stat`: Set whether to perform face recognition

`set_block`: Set whether to receive images

> Block priority is higher than stat, if block is 1, stat is 0, no recognition is performed, but the camera image will be displayed

### **Set whether to perform face recognition results**

```json
{"version":2,"type":"face_recon_ret","code":0,"msg":"set_stat success","stat":1, "block":1}
```

#### Description

`msg`: execution result

`stat`: Whether the current status of face recognition

`code`: status code

- status code

  `0`: success

  `1`: parse failed

### **Scan QR code**
```json
{
    "version":2,
    "type":"qrscan",
    "time_out_s":20
}
```

#### Description

`time_out_s`: QR code scan timeout time

### **QR code scan result**
```json
{"version":2,"type":"qrscan_ret","code":0,"msg":"success","qrcode":"xxxxxx"}
```

#### Description

> It is recommended to use the QR code with error correction level `L`, and the QR code version should be less than `7`

`qrcode`: scan code result

`msg`: execution result

`code`: code

  -`0`: success

  -`1`: Failed to parse the command

  -`2`: Scan code timed out

  -`3`: Unknown error

### **reset**
```json
{
    "version":2,
    "type":"restore",
    "key":"erotser"
}
```

#### Description

no

### **Restore factory settings result**
```json
{
    "version":2,
    "type":"restore_ret",
    "code":0,
    "msg":"restore board success",
}
```

#### Description

no


### **Control device restart**
```json
{"version":2,"type":"reset","key":"teser"}
```

#### Description

no

### **Control device restart result**
```json
{
    "version":2,
    "type":"restore_ret",
    "code":0,
    "msg":"restore board success"
}
```

#### Description

no

### **Image transmission serial port configuration**

```json
{
    "version":2,
    "type":"pic_stream_cfg",
    "query":0,
    "tx":30,
    "baud":921600
}
```

##### Description

`query`: 0, set; 1, query

`baud`: The baud rate used for the output image

`tx`: output image pin, set to `255` to disable image transmission function

### **Image transmission serial port configuration results**

```json
{
    "version":2,
    "type":"pic_stream_cfg_ret",
    "code":0,
    "msg":"config pic stream success",
    "tx":30,
    "baud":921600
}
```

##### Description

`msg`: Results

`code`:

  -`0`: success

  -`1`: Failed to update configuration

  -`2`: Command did not update configuration
