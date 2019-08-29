# FacePi

使用了Dlib的模型，来识别人脸的六十八个特征点，算法就根据特征点来计算眼睛变化程度，判断人的状态。并且加了直方图均衡法来进行光照处理，加强了黑暗场景的处理能力。

光照处理前 

![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/before.jpg)

光照处理后

![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/after.jpg)

光照处理前

![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/before2.png)

光照处理后

![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/after2.png)

# 树莓派移植
移植到了树莓派上，使用了一个RGB三色灯，来表示当前状态，识别不到人脸不亮灯，识别到人脸亮绿灯，识别到闭眼亮红灯，识别到打哈欠亮蓝灯

![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/notfound.png)
![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/normal.png)
![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/close.png)
![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/mouth.png)

# GIF
![Image text](https://raw.githubusercontent.com/Zsy3312/resource/master/ezgif.com-video-to-gif.gif)
