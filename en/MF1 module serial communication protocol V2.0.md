# MF1 module serial communication protocol V2.0

- [1. Modify record](#1. Modify record)        
- [2. Hardware connection](#2. Hardware connection)        
- [3. Json Basic format](#3. Json Basic format)        
    - [3.1 cmd_type](#3.1 cmd_type)        
- [4. Letter of agreement](#4. Letter of agreement)        
    - [4.1 Loading finished](#4.1 Loading finished)        
    - [4.2 Packet parsing error message](#4.2 Packet parsing error message)            
    - [4.3 Set module parameters](#4.3 Set module parameters)        
    - [4.4 Set module parameter results](#4.4 Set module parameter results)        
    - [4.5 Get module parameters](#4.5 Get module parameters)        
    - [4.6 Get module parameter results](#4.6 Get module parameter results)
    - [4.7 Calculating picture face feature values](#4.7 Calculating picture face feature values)
    - [4.8 Calculating picture face feature value results](#4.8 Calculating picture face feature value results) 
    - [4.9 Delete users](#4.9 Delete users) 
    - [4.10 Delete user results](#4.10 Delete user results) 
    - [4.11 Output face information](#4.11 Output face information) 
    - [4.12 Query the current module to store face information](#4.12 Query the current module to store face information) 
    - [4.13 Query the current module to store face information results](#4.13 Query the current module to store face information results) 
    - [4.14 Screen and camera rotation](#4.14 Screen and camera rotation) 
    - [4.14 Screen and camera rotation](#4.14 Screen and camera rotation) 
    - [4.15 Screen and camera rotation results](#4.15 Screen and camera rotation results) 
    - [4.16 Add users by feature value](#4.16 Add users by feature value) 
    - [4.17 Add user results by feature value](#4.17 Add user results by feature value) 
    - [4.18 Setup Module Pin Assignment](#4.18 Setup Module Pin Assignment) 
    - [4.19 Set Module Pin Assignment Results](#4.19 Set Module Pin Assignment Results) 
## **1. Modify record**

| Version | Time | Modify content |
| -------- | ------------ | --------------------------- ----------------------------------------|
| `V1.0` | `2019.05.31` | New Agreement |
| `V1.1` | `2019.06.03` | `head_fix` to `pkt_fix`<br/>Add serial port `IO` Description |
| `V1.2` | `2019.06.05` | Add `code` and `msg` to all packets |
| `V1.3` | `2019.06.13` | Add flip screen and camera interface |
| `V1.4` | `2019.06.14` | Adding a user interface using feature values<br/>fixing `bug`<br/>adding initialization to add version information |
| `V1.5` | `2019.06.17` | Add options for outputting feature values ​​in recognition mode |
| `V1.5.1` | `2019.06.21` | Calculate picture feature values, add options for face detection threshold settings |
| `V1.6` | `2019.06.22` | Add settings communication serial port pin command <br/>fix `bug` |
| `V1.7` | `2019.07.16` | Support `112x112` picture input calculation feature value<br/>feature value is compressed |
| `V2.0` | `2019.07.19` | Support `MF1` module, live detection, some features are not supported |
| `V2.1` | `2019.08.01` | Supporting the board's `IO` |

## 2. Hardware connection

| `K210` | `NAME` | Description |
| ------ | ---------------- | ------------------------- -------------|
| `IO11` | `uart_rx` | `K210` Communication Serial Port `RX`, can be set, default `11` |
| `1010` | `uart_tx` | `K210` Communication Serial Port `TX`, can be set, default `10` |
| `IO5` | `log_tx` | `k210` Print the `TX` of the log, can be set, the default `5` |
| `IO4` | `log_rx` | `k210` Print log `RX`, can be set, default `4` |
| `IO24` | `record key` | `short press record` `long press to clear stored face and board cfg`<br> can be set, default is `24` |
| `IO13` | `relay_act_low` | `relay output`, can be set, default is `13` |
| `IO12` | `relay_act_high` | `relay output`, can be set, default is `12` |

<div STYLE="page-break-after: always;"></div>
## 3. Json Basic format

```json
{"vesrion":$protocol_version,"type":"cmd_type","code":0,"msg":"msg","param":{"xx":"xx","xx":xx}} \r\n
```

<h3>Description</h3>
- The current `protocol_version` is `1`

- The end of the packet must be added `\r\n`

- `\r\n` is not allowed in the middle of the packet.

- Note that `\r\n` is to be escaped to `0d0a`.

### 3.1 cmd_type

| `cmd_type`                                          | Description                            |
| --------------------------------------------------- | ------------------------------- |
| [`init`](#Initialization Completed) | Module Send Initialization Complete Message |
| [`pkt_prase_failed_ret`](#Packet Parsing Error Message) | Packet Parsing Error Message |
| [`set_cfg`](#Set Module Parameters) | Setting Module Parameters |
| [`set_cfg_ret`](#Set Module Parameter Results) | Set Module Parameter Results |
| [`get_cfg`](#Get Module Parameters) | Get Module Parameters |
| [`get_cfg_ret`](#Get Module Parameter Results) | Get Module Parameter Results |
| [`cal_pic_fea`](#Calculate picture face feature values) | Calculate picture face feature values |
| [`cal_pic_fea_ret`](#Calculate image face feature value results) | `JPEG` Image feature value calculation result |
| [`del_user_by_uid`](#Delete User) | User Delete with `UID` |
| [`del_user_by_uid_ret`](#Delete User Results) | Use `UID` for User Delete Results |
| [`face_info`](#output face information) | Output information after recognizing faces |
| [`query_face`](#Query current module storage face information) | Query current module storage face information |
| [`query_face_ret`](#Query current module storage face information result) |  Query current module storage face information result   |
| [`lcd_cam_roate`](#Screen and Camera Rotation) | Set `LCD` and `CAMERA` to rotate (`MF1` not supported)  |
| [`lcd_cam_roate_ret`](#Screen and camera rotation results) | Set `LCD` and `CAMERA` to rotate results (`MF1` not supported)  |
| [`add_uer_by_fea`](#Add User by Feature Value) | Add User by Feature Value  |
| [`add_uer_by_fea_ret`](#Add User Results by Feature Values) | Add User Results by Feature Values  |
| [`set_brd_pin_cfg`](#Setting Module Pin Assignment) | Setting Module Pin Assignment  |
| [`set_brd_pin_cfg_ret`](#Set Module Pin Assignment Result) | Set Module Pin Assignment Results  |

> above `cmd` can click to jump

<div STYLE="page-break-after: always;"></div>
## **4. Letter of agreement**

### **4.1 Loading finished**

```json
{ "version": 1, "type": "init", "code":0,"msg": "init done","version":"v2.0" }
```

<h4>Description</h4>
After the module is started, it will be sent before it can be operated.

<br/>
<br/>

### 4.2 Packet parsing error message

```json
{"version": 1,"type": "pkt_prase_failed_ret","msg": "json prase failed","code": 1,"cmd": "unknown"}
```

<h4>Description</h4>
Return after receiving the wrong packet, and indicate the error, mainly used to help troubleshoot
<br/>
<br/>

### **4.3 Set module parameters**

```json
{"version":1,"type":"set_cfg","cfg":{"uart_baud":115200,"out_feature":0,"open_delay":1,"pkt_fix":0,"auto_out_feature":0, "out_interval_in_ms":500,"fea_gate":70}}
```

<h4>Description</h4>
`uart_baud`: module communication serial port baud rate, default is `115200`

`out_feature`: Whether the output information of the face is attached to the face after the face is recognized, the default is `0`

`open_delay`: Output `IO` open (flip) time, default is `1`

`pkt_fix`: Whether the communication protocol adds header and tail and `CRC16` checksum, the default is `0`. If it is not enabled, the data will be transmitted directly.

`auto_out_feature`: Whether to perform face matching

`out_interval_in_ms`: Output feature value interval time `ms`, default `500`, set to `0` no limit, minimum limit is `500`

`fea_gate`: face comparison threshold

- `auto_out_feature` value description

  - 0: Need to compare, output the feature value when adding a face

  - 1: No need to compare, output real-time eigenvalues, at this time `uid` is `null`, `score` is `0`

  - 2: Need to compare, output real-time eigenvalues ​​of faces

<h4>  Open the communication format of pkt_fix</h4>
```C
0xAA 0x55 HI(LEN) LO(LEN) HI(CRC16) LO(CRC16) ...(data)... 0x55 0xAA
```

You can use [http://www.ip33.com/crc.html](http://www.ip33.com/crc.html) to select `CRC-16/X25 x16+x12+x5+1`

<br/>
<br/>

### **4.4 Set module parameter results**

```json
{"version":1,"type":"set_cfg_ret","msg":"save cfg success","code":0}
```

<h4>Description</h4>
`msg`: return information

`code`: return status code

- status code
  0: Set module parameters successfully
  1: Parsing `Json` fails, `msg` will indicate the wrong place
  2: Failed to save module parameters

> If the `uart_baud` and `pkt_fix` modules are changed, they will automatically restart for the changes to take effect

<br/>
<br/>

### **4.5 Get module parameters**

```json
{ "version": 1, "type": "get_cfg" }
```

<h4>Description</h4>
Get the current configuration of the module.

<br/>
<br/>

### **4.6 Get module parameter results**

```json
{"version":1,"type":"get_cfg_ret","code":0,"msg":"get cfg success","cfg":{"uart_baud":115200,"out_feature":0,"open_delay ":1,"pkt_fix":0,"auto_out_feature":0,"out_interval_in_ms":500,"fea_gate":70}}
```

<h4>Description</h4>
Consistent with the `set_cfg` parameter, just `type` is different.

<br/>
<br/>

### **4.7 Calculating picture face feature values**

```json
{"version": 1,"type": "cal_pic_fea","img": {"size": 10152,"auto_add":0,"sha256": "E65083CFEEEA8F377094C2297E8D3691C23AA8BAD33A82B5E4E4981914FFAC74"}}
```

<h4>Description</h4>
`gate`: face detection threshold, optional, not written with default values.

`size`: Jpeg image size, **Note, maximum support for 30K images.**

`auto_add`: Automatically add users to the module after successful recognition (the default is not added, then the returned `UID` is all `0`).

`sha256`: `j256` checksum of `Jpeg` image (`7zip` and `haozip` both support calculation).

You can start sending the image after receiving the following return (`code` is 1), and it must be sent within `10s`. Timeout to accept the `jpeg` status.

```json
{"version":1,"type":"cal_pic_fea_ret","code":1,"msg":"please start send jpeg image","info":{"uid":"null","feature": "null"}}
```

> When `code` in `info` is `1`, it can start sending `Jpeg` pictures.

You can use the `XCOM` or other serial port assistant's send file function to load the `Jpeg` file and select Send.

<br/>
<br/>

### **4.8 Calculating picture face feature value results**

- Return correctly

```json
{"version":1,"type":"cal_pic_fea_ret","code":0,"msg":"get feature success","info":{"face_prob":0.90,"uid":"0A6F4FB4000000000000000000000000", "feature":"feature base64 encode"}}
```

- Error return (example)

```json
{"version":1,"type":"cal_pic_fea_ret","code":2,"msg":"can not find img.sha256","info":{"face_prob":0,"uid":" Null","feature":"null"}}
```

<h4>Description</h4>
`code`: status code.

`msg`: return information.

`uid`: The `UID` stored by the face in the module. If you need to delete the corresponding face, you need this `UID`.

`feature`: The eigenvalue calculated by the face (`base64 encode`).

`face_prob`: face detection score, normal value is less than `1` floating point number.

> In the [Calculate Picture Face Feature Value] (#Calculate Picture Face Feature Value) packet, you can choose whether to automatically add the user to the module.

- status code
  0: Calculate the eigenvalue successfully

  1: can start sending `Jpeg` pictures

  2: Parsing `Json` error, `msg` will indicate the error place

  3: Module storage is full

  4: There are many faces in the picture

  5: There are no faces in the picture (maybe the direction is wrong, or the face is too small)

  6: `Jpeg` decoding failed (or the picture is not `320x240` resolution)

  7: `Jpeg` file `sha256` verification failed, or waiting to accept image timeout

<br/>
<br/>

### **4.9 Delete users**

```json
{"version": 1, "type": "del_user_by_uid","uid":"1BC6EB528C0000000000000000000000"}
```

<h4>Description</h4>
`uid`: User uid to be deleted

> Delete all users when `uid` is `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF` (32 `F`)

If the failure is specified in the returned result.

<br/>
<br/>

### **4.10 Delete user results**

```json
{"version":1,"type":"del_user_by_uid_ret","code":3,"msg":"can not find user by uid"}
```

<h4>Description</h4>
`msg`: execution result

`code`: status code

- status code

  0: deleted successfully

  1: `Json` parsing error, missing keyword

  2: `flash` operation failed

  3: Failed to find the user corresponding to `uid`

<br/>
<br/>

### **4.11 Output face information**

```json
{"version":1,"type":"face_info","code":0,"msg":"have face","info":{"pic":"540A730200000000","total":1," Current":0,"x1":34,"y1":34,"x2":171,"y2":178,"score":0,"uid":"null","feature":"feature base64 Encode or null"}}
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

<br/>
<br/>

### **4.12 Query the current module to store face information**

```json
{"version":1,"type":"query_face","query":{"total":1,"start":0,"end":10,"out_feature":0}}
```

<h4>Description</h4>
`total`: How many face information is stored for `1`, `start` and `end` and `out_feature` have no meaning, and `0` means query face UID from `start` to `end`

`out_feature`: Whether the face information outputs the corresponding feature value, the default is not output (only one can be checked at a time if the feature value is output)

`start`: query interval start value

`end`: Query interval end value

<br/>
<br/>

### **4.13 Query the current module to store face information results**

```json
{"version":1,"type":"query_face_ret","code":0,"msg":"query uid ands feature success","face":{"total":2,"start":0, "end":1,"info":[{"order":0,"uid":"22BCD239290000000000000000000000","feature":"feature bease64 encode"}...]}}
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

* status code

  0: The query is successful

  1: `Json` parsing error

  2: Returns the number of faces stored in the current module when `total` is `1` in the query package.

  3: Error reading saved data from `flash`

### **4.14 Screen and camera rotation**

```json
{"version":1,"type":"lcd_cam_roate","cfg":{"get_cfg":0,"lcd_flip":0,"lcd_mirror":0,"cam_flip":0,"cam_mirror":0} }
```

<h4>Description</h4>
`get_cfg`: Get the `LCD` and `CMA` parameters of the current module

`lcd_flip`: `lcd` shows vertical mirroring

`lcd_mirror`: `lcd` shows horizontal mirroring

`cam_flip`: `camera` for vertical mirroring

`cam_mirror`:`camera` for horizontal mirroring

> `MF1` module does not support this command

### **4.15 Screen and camera rotation results**

```json
{"version":1,"type":"lcd_cam_roate_ret","code":0,"msg":"set lcd and cam success","cfg":{"lcd_flip":0,"lcd_mirror":0, "cam_flip": 0, "cam_mirror": 0}}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

- status code

  0: set successfully

  1: `Json` parsing error

  2: Error saving configuration

  3: Get the configuration successfully

  4: `MF1` module does not support setting

### **4.16 Add users by feature value**

```json
{"version":1,"type":"add_uer_by_fea","user":{"uid":"EDE6E800A20000000000000000000000","fea":"feature base64 encode"}}
```

<h4>Description</h4>
`uid`: User's `uid`

`fea`: user face feature value

### **4.17 Add user results by feature value**

```json
{"version":1,"type":"add_uer_by_fea_ret","code":0,"msg":"add user success","uid":"EDE6E800A20000000000000000000000"}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

`uid`: Add a successful `uid`, if the failure is all `0`

- status code

  0: added successfully

  1: `Json` parsing error

  2: Save to `flash` failed

  3: `uid` already exists

### **4.18 Setup Module Pin Assignment**

```json
{"version": 1, "type": "set_brd_pin_cfg", "cfg":{"get_cfg":0,"port_tx":10,"port_rx":11,"log_tx":5,"log_rx":4, "relay_low": 12,"relay_high": 13,"key":24,"key_dir":1}}
```

<h4>Description</h4>
`get_cfg`: Get the configuration of the current module

`port_tx`: This module communicates with other modules with the `TX` pin. The default is `10`.

`port_rx`: This module communicates with other modules with the `RX` pin. The default is `11`.

`log_tx`: This module outputs the log `TX` pin, the default is `5`

`log_tx`: This module outputs the log `RX` pin, which defaults to `4`.

`relay_low`: Relay output ** often low ** pin, default is `12`

`relay_high`: Relay output** constant high** pin, default is `13`

`key`: button, the default is `24`

`key_dir`: Press the button level, the default is `1`

> Note that the module will not detect if the set 'IO` is the same, please ensure that the parameters are correct.

### **4.19 Set Module Pin Assignment Results**

```json
{"version":1,"type":"set_brd_pin_cfg_ret","code":0,"msg":"get uart_pin cfg success","cfg":{"port_tx":10,"port_rx":11," Log_tx":5,"log_rx":4,"relay_low":12,"relay_high":13,"key":24,"key_dir":1}}
```

<h4>Description</h4>
`code`: status code

`msg`: return information

`cfg`: The current configuration of the module, same as [set instruction] (#Set module pin assignment)

- status code
  0: set successfully

  1: `Json` parsing error

  2: The setting parameters are incorrect and are indicated in `msg`

  3: Failed to save parameters
