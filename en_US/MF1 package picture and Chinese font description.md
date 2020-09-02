# MF1 package picture and Chinese font description

- [1. Packing pictures] (#1. Packing pictures)
- [2. Packing Chinese Fonts] (#2. Packing Chinese Fonts)

## 1. Packing pictures

```shell
./gen_imgbin.sh

Or

./gen_imgbin.sh 1 #All images merge into one file
```

- Use [`tools/pic/gen_imgbin.sh`](./tools/pic/gen_imgbin.sh) to package the image. It is recommended to merge all the images into one large file.

- Requires the picture to be `*.BMP` (the script will convert `*.BMP` to `*.bin`).<br>The width cannot exceed the width of the screen, and the height can be less than the height of the screen.

- Modify [`tools/pic/flash-list.json`](./tools/pic/flash-list.json) to specify the address corresponding to the image

- The address of the picture needs to be decimal, and it is better to use `4K` bytes for it. If you want to burn separately, you need to ensure that the address is `64K` bytes.

- The space currently allocated to the user to store the picture is `12-16MBytes`, no other space can be used.

## 2. Packing Chinese fonts

- There are currently Chinese fonts for `GB2312` and `GBK`. `16x16` and `32x32`<br> are recommended to use the font of `GB2312`, which is small in size and supports commonly used Chinese characters.

- Directly burn [`GB2312_16_32.kfpkg`] (./tools/zhCN_font/GB2312/GB2312_16_32.kfpkg)