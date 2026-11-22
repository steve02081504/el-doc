# desktop-automation/vision.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/vision {#api-ce81ac1cdd26910feb1b}

源码：`src/stdlib/desktop-automation/vision.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/vision.el#L1)

在 RGBA 图像上读取像素、裁剪、比较颜色和搜索模板图像；返回坐标相对于输入图像左上角。
模板搜索按行优先扫描；图像资源由调用方提供，访问像素时借用其缓冲区。

## imagePixel {#api-4cfd93a25ea49815c4a5}

源码：`src/stdlib/desktop-automation/vision.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/vision.el#L167)

读取图像中指定整数坐标的 RGBA 像素；越界或非整数坐标会因范围校验失败。

```el-signature
export fn imagePixel(image: RgbaImage, x: Number, y: Number): ScreenPixel
```

**返回类型**：[`ScreenPixel`](../../types.md#api-f5326652bd97bfe22d03)

**参数**：image 要读取的 RGBA 图像。

**参数**：x 从左侧起算的像素列，范围为 `0..image.width-1`。

**参数**：y 从顶部起算的像素行，范围为 `0..image.height-1`。

**返回值**：包含 0..255 通道值的 `ScreenPixel`。

### 示例：读取图像左上角像素

```el
let pixel = imagePixel(image, 0, 0)
```
