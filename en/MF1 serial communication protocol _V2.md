# Face recognition module communication protocol based on serial communication V2.0.1

- [1. Modifying the record](#1. Modifying the record) 
- [2. Hardware connection](#2. Hardware connection)
- [3. Json Basic Format](#3. Json Basic Format)
    - [3.1 cmd_type](#3.1 cmd_type)
- [4. Communication Protocol](#4. Communication Protocol)
    - [4.1 Initialization completed](#4.1 Initialization completed)
    - [4.2 Packet Parsing Error Message](#4.2 Packet Parsing Error Message)
    - [4.3 Output Face Information](#4.3 Output Face Information)
    - [4.4 Calculating Picture Face Feature Values](#4.4 Calculating Picture Face Feature Values)
    - [4.5 Calculate picture face feature value result](#4.5 Calculate picture face feature value result)
    - [4.6 Add User-Specified UID](#4.6 Add User-Specified UID)
    - [4.7 Add User-Specified UID Result](#4.7 Add User-Specified UID Result)
    - [4.8 Add User by Feature Value](#4.8 Add User by Feature Value)
    - [4.9 Add User Results by Feature Values](#4.9 Add User Results by Feature Values)
    - [4.10 Delete User by UID](#4.10 Delete User by UID)
    - [4.11 Deleting User Results by UID](#4.11 Deleting User Results by UID)
    - [4.12 Query Module Stores Face Information](#4.12 Query Module Stores Face Information)
    - [4.13 Query Module Stores Face Information Results](#4.13 Query Module Stores Face Information Results)
    - [4.14 Setting Screen Display](#4.14 Setting Screen Display)
    - [4.15 Setting Screen Display Results](#4.15 Setting Screen Display Results)
    - [4.16 Delete Screen Display](#4.16 Delete Screen Display)
    - [4.17 Delete screen display result](#4.17 Delete screen display result)
    - [4.18 Setting Module Hardware Configuration](#4.18 Setting Module Hardware Configuration)
    - [4.19 Setting Module Hardware Configuration Results](#4.19 Setting Module Hardware Configuration Results)
    - [4.20 Setting Module Software Configuration](#4.20 Setting Module Software Configuration)
    - [4.21 Setting Module Software Configuration Results](#4.21 Setting Module Software Configuration Results)

## 1. Modify the record

| Version | Time | Modify content |
| -------- | ------------ | ------------- |
| `0.1` | `2019.09.05` | Protocol version to `2` |

## 2. Hardware connection

| `K210` | Description |
| ------ |----------------------------- |
| `IO5` | Protocol serial port `TX`, can be set, default `5` |
| `IO4` | Protocol serial port `RX`, can be set, default `4` |
| `IO11` | Debugging the serial port `RX`, can be set, the default `11` |
| `1010` | Debugging the serial port `TX`, can be set, the default `10` |
| `IO24` | Short press to enter the face, can be set, the default is `24`<br> (long press to clear the face feature value to burn special firmware) |
| `IO13` | Relay constant high output, can be set, default is `13` |
| `IO12` | Relay low output, can be set, default is `12` |

<div STYLE="page-break-after: always;"></div>
## 3. Json basic format

```json
{"version":$protocol_version,"type":"cmd_type","code":0,"msg":"msg","param":{"xx":"xx","xx":xx}} \r\n
```

<h4>Description</h4>
- The current `protocol_version` is `2`

- The end of the packet must be added `\r\n`

- `\r\n` is not allowed in the middle of the packet.

> Note that `\r\n` is to be escaped as `0d0a`

### 3.1 cmd_type

| `cmd_type` | Description |
| ---------- | ---------- |
| [`init`](#Initialization Completed) | Module Send Initialization Complete Message |
| [`pkt_prase_failed_ret`](#Packet Parsing Error Message) | Packet Parsing Error Message |
| [`face_info`](#output face information) | Output face information after recognizing faces |
| [`cal_pic_fea`](#Calculate image face feature values) | Calculate face feature values in `Jpeg` images |
| [`cal_pic_fea_ret`](#Calculate picture face eigenvalue results) | Calculate face eigenvalue results in `Jpeg` picture |
| [`add_user_spec_uid`](#Add User-Specified UID) | Add User and Specify `UID` |
| [`add_user_spec_uid_ret`](#Add User-Specified UID Results) | Add User and Specify `UID` Result |
| [`add_user_by_fea`](#Add User by Feature Value) | Add User by Feature Value |
| [`add_user_by_fea_ret`](#Add User Results by Feature Values) | Add User Results by Feature Values  |
| [`del_user_by_uid`](#Delete User by UID) | Delete User by `UID`|
| [`del_user_by_uid_ret`](#Delete User Results by UID) | Delete User Results by `UID` |
| [`query_face`](#Query Module Stores Face Information) | Face Information Stored in Query Module |
|[`query_face_ret`](#Query Module Stores Face Information Results) | Face Information Results Stored in Query Module  |
| [`set_lcd_display`](#Setup Screen Display) | Set Screen Display String or Picture |
| [`set_lcd_display_ret`](#Setting Screen Display Results) | Setting Screen Display String or Picture Results |
| [`clr_lcd_display`](#Delete Screen Display) | Delete Screen Display Elements |
| [`clr_lcd_display_ret`](#Delete Screen Display Results) | Delete Screen Display Element Results |
| [`brd_hard_cfg`](#Setup Module Hardware Configuration) | Setting Module Hardware Configuration |
| [`brd_hard_cfg_ret`](#Set Module Hardware Configuration Results) | Set Module Hardware Configuration Results |
| [`brd_soft_cfg`](#Setup Module Software Configuration) | Setting Module Software Configuration |
| [`brd_soft_cfg_ret`](#Setup Module Software Configuration Results) | Set Module Software Configuration Results |


> above `cmd` can click to jump

<div STYLE="page-break-after: always;"></div>
## **4. Communication Protocol**

### 4.1 Initialization completed

```json
{ "version": 2, "type": "init", "code":0,"msg": "init done","proto":"0.1" }
```

<h4>Description</h4>
Module startup completed



### 4.2 Packet parsing error message

```json
{"version": 2,"type": "pkt_prase_failed_ret","msg": "json prase failed","code": 1,"cmd": "unknown"}
```

<h4>Description</h4>
Return after receiving the wrong packet, and indicate the error, mainly used to help troubleshoot



### 4.3 Output face information

```json
{"version":2,"type":"face_info","code":0,"msg":"have face","info":{"pic":"540A730200000000","total":1," Current":0,"x1":34,"y1":34,"x2":171,"y2":178,"score":0,"uid":"null","feature":"feature base64 Encode or null"}}
```

<h4>Description</h4>
`pic`: Used to judge whether it belongs to the same picture when there are multiple faces

`total`: Total number of faces in this recognition

`current`: The #N` face in this recognition (starting from `0`)

`x1`: The upper left corner of the face coordinate box `x`

`y1`: The upper left corner of the face coordinate box `y`

`x2`: The lower right corner of the face coordinate box `x`

`y2`: The lower right corner of the face coordinate box `y`

`score`: face matching value (0 when directly outputting the feature value)

`uid`: `UID` corresponding to the face (`null` when outputting the feature value directly)

`feature`: face feature value, configurable whether to output (not to be `null` when output)



### 4.4 Calculating picture face feature values

```json
{"version": 2,"type": "cal_pic_fea","img": {"size": 10152,"auto_add":0,"sha256": "E65083CFEEEA8F377094C2297E8D3691C23AA8BAD33A82B5E4E4981914FFAC74","uid":"0A6F4FB4000000000000000000000000"}}
```

<h4>Description</h4>
`threshold`: Face detection threshold, optional, default is `70`

`size`: Jpeg image size, **Note, maximum support for 30K images**

`auto_add`: Automatically add users to the module after successful recognition (the default is not added, then the returned `UID` is all `0`)

`sha256`: `j256` checksum of `Jpeg` image (`7zip` and `haozip` both support calculation)

`uid`: If you choose to add to the module automatically, the specified `uid` will be used.

You can start sending the image after receiving the following return (`code` is 1), and it must be sent within `10s`. Timeout to accept the `jpeg` status

```json
{"version":2,"type":"cal_pic_fea_ret","code":1,"msg":"please start send jpeg image","info":{"uid":"null","feature": "null"}}
```

> When `code` in `info` is `1`, it can start sending `Jpeg` pictures

You can use the `XCOM` or other serial port assistant's send file function to load the `Jpeg` file and select Send.

### 4.5 Calculating picture face feature value results

```json
{"version":2,"type":"cal_pic_fea_ret","code":0,"msg":"get feature success","info":{"face_prob":0.90,"uid":"0A6F4FB4000000000000000000000000", "feature":"feature base64 encode"}}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

`uid`: The `UID` stored by the face in the module. If you need to delete the corresponding face, you need this `UID`.

`feature`: The eigenvalue calculated by the face (`base64 encode`)

`face_prob`: face detection score, normal value is less than `1` floating point number

> In the [Calculate Picture Face Feature Value] (#Calculate Picture Face Feature Value) packet, you can choose whether to automatically add the user to the module.

- status code

  `0`: Calculate the eigenvalue successfully

  `1`: can start sending `Jpeg` pictures

  `2`: Parsing `Json` error, `msg` will indicate the error place

  `3`: Module storage is full

  `4`: There are many faces in the picture

  `5`: There are no faces in the picture (maybe the direction is wrong, or the face is too small)

  `6`: `Jpeg` decoding failed (or the picture is not `320x240` resolution)

  `7`: `Jpeg` file `sha256` verification failed, or waiting to accept image timeout



### 4.6 Add User-Specified UID

```json
{"version":2,"type":"add_user_spec_uid","user":{"uid":"EDE6E800A20000000000000000000000","time_s":5}}
```

<h4>Description</h4>
> Equivalent to key input user, you can specify `uid`, it will detect whether the user is facing the face

`uid`: The user specifies the `uid` of the newly added user.

`time_s`: Add user timeout, default `5`s, maximum `100`



### 4.7 Add User-Specified UID Results

```json
{"version":2,"type":"add_user_spec_uid_ret","user":{"uid":"EDE6E800A20000000000000000000000"}}
```

<h4>Description</h4>
`msg`: execution result

`code`: status code

- status code

  `0`: success

  `1`: failed

  `2`: waiting to be added



### 4.8 Adding users by feature values

```json
{"version":2,"type":"add_user_by_fea","user":{"uid":"EDE6E800A20000000000000000000000","fea":"feature base64 encode"}}
```

<h4>Description</h4>
`uid`: User's `uid`

`fea`: user face feature value

### 4.9 Adding User Results by Feature Values

```json
{"version":2,"type":"add_user_by_fea_ret","code":0,"msg":"add user success","uid":"EDE6E800A20000000000000000000000"}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

`uid`: Add a successful `uid`, if the failure is all `0`

- status code

  `0`: added successfully

  `1`: `Json` parsing error

  `2`: Save to `flash` failed

  `3`: `uid` already exists



### 4.10 Deleting users by UID

```json
{"version": 2,"type": "del_user_by_uid","uid":"1BC6EB528C0000000000000000000000"}
```

<h4>Description</h4>
`uid`: User uid to be deleted

> Delete all users when `uid` is `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF` (32 `F`)

If the failure is specified in the returned result



### 4.11 Deleting User Results by UID

```json
{"version":2,"type":"del_user_by_uid_ret","code":3,"msg":"can not find user by uid"}
```

<h4>Description</h4>
`msg`: execution result

`code`: status code

- status code

  `0`: deleted successfully

  `1`: `Json` parsing error, missing keyword

  `2`: `flash` operation failed

  `3`: Failed to find the user corresponding to `uid`



### 4.12 Query module stores face information

```json
{"version":2,"type":"query_face","query":{"total":1,"start":0,"end":10,"out_feature":0}}
```

<h4>Description</h4>
`total`: How many face information is stored for `1`, `start` and `end` and `out_feature` have no meaning, and `0` means query face UID from `start` to `end`

`out_feature`: Whether the face information outputs the corresponding feature value, the default is not output (only one can be checked at a time if the feature value is output)

`start`: query interval start value

`end`: Query interval end value



### 4.13 Query Module Stores Face Information Results

```json
{"version":2,"type":"query_face_ret","code":0,"msg":"query uid ands feature success","face":{"total":2,"start":0, "end":1,"info":[{"order":0,"uid":"22BCD239290000000000000000000000","feature":"feature bease64 encode"}...]}}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

`face`:

- `total`: total number of faces in the current module

- `start`: The starting value of the result interval of this query (counting from `0`)

- `end`: the end of the query result interval

- `info`:

  - `order`: the order of the current face

  - `uid`: `UID` of the current face

  - `feature`: the eigenvalue of the current face

- status code

  `0`: The query is successful

  `1`: `Json` parsing error

  `2`: Returns the number of faces stored in the current module when `total` is `1` in the query package.

  `3`: Error reading saved data from `flash`




### 4.14 Setting the screen display

```json
{"version":2,"type":"set_lcd_display","cfg":{"cfg_type":"str","zhCN":0,"id":0,"x":0,"y": 0,"size":16,"str":"abcd","color":1,"bg_color":1}}
```

```json
{"version":2,"type":"set_lcd_display","cfg":{"cfg_type":"pic","id":0,"x":0,"y":0,"w": 320, "h": 240, "addr": 123456, "alpha": 50}}
```

<h4>Description</h4>
`cfg_type`: `str` or `pic`, set the overlay image or string

String display configuration:
- `id`: `id` of the string, used when deleting
- `x`: string displays the `x` coordinates of the location
- `y`: string shows the position of the `y` coordinate
- `size`: Currently supports `16` and `32`
- `str`: the string to be displayed
- `color`: the color of the string, the type of the number, the `RGB565` code, the `63488` indicates the red
- `bg_color`: string background color, number type, equal to `1` when background color is not set
- `zhCN`: Whether the string is Chinese, <br> If the string is Chinese, you need to `base64` the `str`, <br> currently supports the Chinese display of `GB2312` encoding, `ye7b2s75y9m/xry8` `深圳矽速科技"

Picture display configuration:
  - `id`: `id` of the picture, used when deleting
  - `x`: The picture shows the origin `x`
  - `y`: The picture shows the origin `y`
  - `w`: the width of the picture
  - `h`: the height of the picture
  - `addr`: the address where the image is saved in flash
  - `alpha`: Image and camera image overlay transparency

### 4.15 Setting the screen to display the result

```json
{"version":2,"type":"set_lcd_display_ret","msg":"set lcd display success","code":0,"id":0}
```

<h4>Description</h4>
`id`: The `id` of the screen display content

`msg`: message

`code`: code

  - `0`: success

  - `1`: failed



### 4.16 Delete screen display

```json
{"version":2,"type":"clr_lcd_display","id":0}
```

<h4>Description</h4>
`id`: The screen displays the `id` of the content. When the `id` is 1024, all the contents are deleted.



### 4.17 Delete screen display results

```json
{"version":2,"type":"clr_lcd_display_ret","msg":"clr lcd display success","code":0,"id":0}
```

<h4>Description</h4>
`id`: The `id` of the screen display content

`msg`: message

`code`: code

  - `0`: success

  - `1`: failed



### 4.18 Setting module hardware configuration

```json
{"version":2,"type":"brd_hard_cfg","cfg":{"get_cfg":0,"cfg_type":"lcd_cam","cfg":{"lcd_flip":0,"lcd_mirror":0 ,"cam_flip":0,"cam_mirror":0}}
```

```json
{"version":2,"type":"brd_hard_cfg","cfg":{"get_cfg":0,"cfg_type":"uart_relay","port_tx":10,"port_rx":11,"log_tx": 5, "log_rx": 4, "relay_low": 12, "relay_high": 13, "key": 24, "key_dir": 1}}
```

<h4>Description</h4>
`get_cfg`: read the current configuration



Query or set the module's screen and camera rotation when `cfg_type` is `lcd_cam`

`lcd_flip`: `lcd` shows vertical mirroring

`lcd_mirror`: `lcd` shows horizontal mirroring

`cam_flip`: `camera` for vertical mirroring

`cam_mirror`:`camera` for horizontal mirroring



Query or set the module's serial port and relay configuration when `cfg_type` is `uart_relay`

`port_tx`: This module communicates with other modules with the `TX` pin. The default is `10`.

`port_rx`: This module communicates with other modules with the `RX` pin. The default is `11`.

`log_tx`: This module outputs the log `TX` pin, the default is `5`

`log_rx`: This module outputs the log `RX` pin, which defaults to `4`.

`relay_low`: Relay output ** often low ** pin, default is `12`

`relay_high`: Relay output** constant high** pin, default is `13`

`key`: button, the default is `24`

`key_dir`: Press the button level, the default is `1`

> Note that the module will not detect if the set 'IO` is the same, please ensure that the parameters are correct.



### 4.19 Setting module hardware configuration results

```json
{"version":2,"type":"brd_hard_cfg_ret","code":1,"msg":"get cfg success","cfg":{}}
```

<h4>Description</h4>
`msg`: message

`code`: code

  - `0`: success

  - `1`: failed

`cfg`: Refer to the [Setup Module Hardware Configuration] (#Set Module Hardware Configuration) command above.



### 4.20 Setting module software configuration

```json
{"version":2,"type":"brd_soft_cfg","cfg":{"get_cfg":0,"out_fea":0,"auto_out_fea":0,"out_interval_ms":100,"out_threshold":88.0, "pkt_fix": 0, "relay_open_s": 2, "port_baud": 115200}}
```

<h4>Description</h4>
> `0` is off, `1` is on

`get_cfg`: read the current configuration

`out_fea`: Identifies whether the feature value is output successfully. The default is `0`.

`auto_out_fea`: Does not compare with the stored face database, it recognizes the face output, the default is `0`

`out_interval_ms`: The interval between two output results, the unit is `ms`, the default is `100`, and the maximum is `1000`

`out_threshold`: Face comparison output threshold (floating point, maximum 100), default is `88.0`

`pkt_fix`: Whether the communication protocol adds header and tail and `CRC16` checksum, the default is `0`

`relay_open_s`: Relay open time, the unit is `s`, the default is `2`, the maximum is `100`

`port_baud`: Communication serial port baud rate, default is `115200`

`out_fea` value description

  - `0`: does not output eigenvalues

  - `1`: Output feature value (characteristic value stored in `flash`)

  - `2`: Output real-time eigenvalues

When `auto_out_fea` is `1`, the output face information, `uid` is `null`, `score` is `0`

> Restart to make the settings take effect

<h5>Open the communication format of pkt_fix</h5>

```C
0xAA 0x55 HI(LEN) LO(LEN) HI(CRC16) LO(CRC16) ...(data)... 0x55 0xAA
```

You can use [http://www.ip33.com/crc.html](http://www.ip33.com/crc.html) to select `CRC-16/X25 x16+x12+x5+1`



### 4.21 Setting module software configuration results

```json
{"version":2,"type":"brd_soft_cfg_ret","code":1,"msg":"get cfg success","cfg":{}}
```

<h4>Description</h4>
`msg`: message

`code`: code

  - `0`: success

  - `1`: failed

`cfg`: Refer to the [Setup Module Software Configuration] (#Setup Module Software Configuration) command above.