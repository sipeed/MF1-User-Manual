# `MF` 人脸识别模块简明用户手册

[ [English](./README.md) | 中文]

- [`MF1` V1 模块简明用户手册](./zh_CN/m01_mf1_v1_get_started.md)
- [`MF1` V2 模块简明用户手册](./zh_CN/m02_mf1_v2_get_started.md)
- [`MF` 模块通用 HEX 协议](./zh_CN/p02_mf_protocol_manual_v2_hex_zh_CN.md)
- [`MF` 模块通用 JSON 协议](./zh_CN/p02_mf_protocol_manual_v2_json_zh_CN.md)
- [MF1 固件更新说明（与机器码 key 获取说明）](./zh_CN/k01_update_firmware_and_get_key.md)

## 关于 MF 人脸识别模组

- 现有 MF 人脸识别模组

| 模组/开发板 | 说明 |
| --- | --- |
| MF0 | 核心板 |
| MF1 | 1.3 寸 IPS 屏幕 |
| MF1_TO_MF2 | MF1 外接 2.4/2.8寸屏幕 |
| MF2 | 86 |
| MF4 | 定制版 |
| MF5 | 成品 |
| MF5-QT 版 | |

## MF 板型一览

<table border="3">
    <tr>
        <th colspan=4>MF1 V2 版</th>
    </tr>
    <tr>
        <td  width="100">描述</td>
        <td>正面视图</td>
        <td>背面视图（不带NAND）</td>
        <td>背面视图（带NAND）</td>
    </tr>
    <tr>
        <td width="100">MF1 1.3寸屏</td>
        <td>
            <img src="./assets/mf_module/mf1_front_v2.png" widt="600" alt="MF1 正面">
        </td>
        <td>
            <img src="./assets/mf_module/mf1_bottom_v2.png" widt="600" alt="MF1 背面视图">
        </td>
        <td>
            <img src="./assets/mf_module/mf1_bottom_v2(nand).png" widt="600" alt="MF1(NAND Flash) 背面视图">
        </td>
    </tr>
    <tr>
        <td>MF1 TO MF2 2.4/2.8寸屏</td>
        <td>
            <br> TODO: 图片为 MF1 1.3',待更新</br>
            <img src="./assets/mf_module/mf1_front_v2.png" widt="600" alt="MF1 正面">
        </td>
        <td>
            <br> TODO: 图片为 MF1 1.3',待更新</br>
            <img src="./assets/mf_module/mf1_bottom_v2.png" widt="600" alt="MF1 背面视图">
        </td>
        <td>
            <br> TODO: 图片为 MF1 1.3',待更新</br>
            <img src="./assets/mf_module/mf1_bottom_v2(nand).png" widt="600" alt="MF1(NAND Flash) 背面视图">
        </td>
    </tr>
</table>

- 烧录固件时注意 区分摄像头方向

| 描述 | 摄像头丝印 | 说明 |
| --- | --- | --- |
| 横向（H）| <img src="./assets/camera/camera_dual_h.png" widt="600" alt="横向双摄">| |
| 竖向（V）| <img src="./assets/camera/camera_dual_v.png" widt="600" alt="竖向双摄">| |

固件说明

> 烧录固件之前，一定要确认选择的固件和自己的**板型一致**，
烧录之后建议均擦除下**板级配置信息**

| 文件名 | 适用板型 | 说明 |
| --- | --- | --- |
|PROJ_MF1H_TO_MF2H_bin.bin   | MF1 转 2.4/2.8 寸, 摄像头方向: 横向(H)   | HEX 协议 |
|PROJ_MF1H_TO_MF2H_json.bin  | MF1 转 2.4/2.8 寸, 摄像头方向: 横向(H)   | JSON 协议 |
|   |   |   |
|PROJ_MF1H_bin.bin           | MF1 1.3 寸 IPS, 摄像头方向: 横向(H)      | HEX 协议 |
|PROJ_MF1H_json.bin          | MF1 1.3 寸 IPS, 摄像头方向: 横向(H)      | JSON 协议 |
|   |   |   |
|PROJ_MF1V_TO_MF2V_bin.bin   | MF1 转 2.4/2.8 寸, 摄像头方向: 竖向(V)   | HEX 协议 |
|PROJ_MF1V_TO_MF2V_json.bin  | MF1 转 2.4/2.8 寸, 摄像头方向: 竖向(V)   |JSON 协议 |
|   |   |   |
|PROJ_MF1V_bin.bin           | MF1 1.3 寸 IPS, 摄像头方向: 竖向(V)      | HEX 协议 |
|PROJ_MF1V_json.bin          | MF1 1.3 寸 IPS, 摄像头方向: 竖向(V)      | JSON 协议 |
|   |   |   |
|PROJ_MF2V_bin.bin           | MF2 2.4/2.8 寸, 摄像头方向: 竖向(V)      | HEX 协议 |
|PROJ_MF2V_json.bin          | MF2 2.4/2.8 寸, 摄像头方向: 竖向(V)      | JSON 协议 |
|   |   |   |
|protocol_bin.md             |                                         | BIN(HEX) 原始协议文件 |
|protocol_json.md            |                                         | JSON 原始协议文件 |
|release.md                  |                                         | 版本更新记录 |
+
