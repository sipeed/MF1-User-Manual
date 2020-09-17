# MF1 打包图片及中文字体说明

！！！ 旧版文档 待更新

-------

## 打包图片

```shell
./gen_imgbin.sh

or

./gen_imgbin.sh 1  #所有图片合并成一个文件
```

- 使用[`tools/pic/gen_imgbin.sh`](./tools/pic/gen_imgbin.sh)来打包图片, 建议将所有图片合并成一个大文件

- 要求图片为 `*.BMP`(脚本会将`*.BMP`转为`*.bin`) <br>宽度不可以超过屏幕的宽度, 高度可以小于屏幕的高度

- 修改[`tools/pic/flash-list.json`](./tools/pic/flash-list.json), 指定图片对应的地址

- 图片的地址需要为 10 进制, 而且最好是 `4K` 字节对其<br>如果要分开烧录, 需要保证地址是 `64K` 字节对其

- 目前分配给用户用来存储图片的空间为 `12-16MBytes` ,不可使用其他空间

## 打包中文字体

- 目前有 `GB2312` 及 `GBK` 的中文字库, `16x16` 和 `32x32` <br>建议使用 `GB2312` 的字库, 体积小, 支持常用的汉字, 非生僻字

- 直接烧录[`GB2312_16_32.kfpkg`](./tools/zhCN_font/GB2312/GB2312_16_32.kfpkg)即可
