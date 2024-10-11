# KouSuanOCR 网络包加密了，研究解密并不是长久之计。MITM不再维护。

**udp tcp ws没看到对面进度的包，很奇怪啊，就是一个本地生成的假的PK。**

适用于1920x1080安卓模拟器的小猿口算自动刷分&自动比赛脚本

OCR识别适用于刷题刷分，~MITM适用于比赛~。需要注意的是：**当你的速度超过其他与你同样使用脚本的人时，或者连赢和平局时，系统会安排机器人给你。具体为：id没变，名字一样，每次显示对面的胜利数量都是随机的，对面速度也是随机的。**

**~增加KouSuanMITMCheat，具体查看脚本内注释。~**

推荐的库&思路：<br>
<https://github.com/wyp010428/xiaoyuankousuan><br>
<https://github.com/cr4n5/XiaoYuanKouSuan><br>
`本脚本不会教你安装什么库，自己去百度找相关资料进行安装。`


>template_image = cv2.imread('QQ20241008-195310.png', 0) <br>
>template_image2 = cv2.imread('QQ20241008-201026.png', 0) <br>
>template_image3 = cv2.imread('continue.png', 0) <br>
>template_image4 = cv2.imread('continuepk.png', 0) <br>


这两个图片是用来进行自动点击识别元素的，以及脚本默认适配横屏1920x1080分辨率模拟器，并且你需要提前手动连接上你的虚拟机adb远程端口。


~KouSuanMITM&KouSuanMITMCheat~的部署难度比KouSuanOCR低许多，我们这里只讲MITM如何配置，请确保你能够执行基本的pip install操作 以及能够自行增加镜像源。

~KouSuanMITM~的需要的库：
> mitmproxy<br>
> numpy<br>
> opencv-python<br>
> Pillow<br>


使用前请确保你已经连接上了ADB设备。如果是虚拟机则将代理设置为手动并且IP地址为你的PC地址，端口为8080。这里以MUMU模拟器为例。<br>

如何获取MUMU模拟器的ADB端口:<https://mumu.163.com/help/20230214/35047_1073151.html><br>

pip换源教程:<https://zhuanlan.zhihu.com/p/345161094><br>

<img src="https://github.com/extrant/IMGSave/blob/main/mitm%E6%95%99%E7%A8%8B.png?raw=true">

之后运行抓包.bat就可以，会打开一个浏览器窗口。如果你的虚拟机能够正常加载小猿口算的图片那么恭喜你已经成功了！

