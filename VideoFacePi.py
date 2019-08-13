#coding=utf-8 
import dlib
import cv2
import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # 设置端口号
GPIO.setup(11, GPIO.OUT)  # 设置电平输出
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

def initLight():
    GPIO.output(11, GPIO.LOW) # 输出电平
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    return

def lightBlue():
    initLight()
    GPIO.output(11, GPIO.HIGH)
    return

def lightRed():
    initLight()
    GPIO.output(12, GPIO.HIGH)
    return

def lightGreen():
    initLight()
    GPIO.output(13, GPIO.HIGH)
    return

# 计算两点距离
def calDistance(posA, posB):
    temp = pow(posA.x - posB.x, 2) + pow(posA.y - posB.y, 2)
    return math.sqrt(temp)

# 加载并初始化检测器
detector = dlib.get_frontal_face_detector()
# dlib的68点模型，使用训练好的特征预测器
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# 视频路径
#camera = cv2.VideoCapture('E:/study/13-FemaleGlasses.avi')
#camera = cv2.VideoCapture('E:/study/18-mytest2.avi')
camera = cv2.VideoCapture(0)
camera.set(3, 320)
camera.set(4, 240)
if not camera.isOpened():
    print("cannot open camear")
    exit(0)
biggestRight = 0
biggestLeft = 0
smallestRight = 100
smallestLeft = 100
frameCount = 0
tiredList = []
lastEye = 0
while True:
    # 读取帧
    ret, frame = camera.read()
    if not ret:
        break

    frameCount = frameCount + 1
    if frameCount % 2 != 0:
        continue
    frame_new = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 检测脸部
    dets = detector(frame_new, 1)
    # print("Number of faces detected: {}".format(len(dets)))
    if len(dets) > 0:
        lightGreen()
    else:
        initLight()

    # 查找脸部位置
    for i, face in enumerate(dets):
        # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} ".format(
        #    i, face.left(), face.top(), face.right(), face.bottom()))

        shape = predictor(frame, face)
        # 绘制脸部位置
        # cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 1)

        tempLeft = (calDistance(shape.part(37), shape.part(41)) + calDistance(shape.part(38), shape.part(40))) / \
                   (calDistance(shape.part(36), shape.part(39)))
        tempRight = (calDistance(shape.part(43), shape.part(47)) + calDistance(shape.part(44), shape.part(46))) / \
                    (calDistance(shape.part(42), shape.part(45)))

        faceInMid = calDistance(shape.part(0), shape.part(27)) / calDistance(shape.part(27), shape.part(16))
        if faceInMid > 0.4 and faceInMid < 2.5:  # 排除脸部旋转的情况
            if tempLeft > biggestLeft:
                biggestLeft = tempLeft

            if tempRight > biggestRight:
                biggestRight = tempRight

            if tempRight < smallestRight:
                smallestRight = tempRight

            if tempLeft < smallestLeft:
                smallestLeft = tempLeft


        if tempLeft-smallestLeft < (biggestLeft - smallestLeft) * 0.25 or tempRight - smallestRight < (biggestRight - smallestRight) * 0.25:
            #cv2.putText(frame, "closeEyes", (face.left(), face.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            #检查到闭眼
            #忽略前三十帧
            #cv2.putText(frame, "closeEyes", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            if lastEye == 1:
                tiredList.append(1)
                lightRed()
            lastEye = 1
        else:
            lastEye = 0
            tiredList.append(0)

        if len(tiredList) > 15:
            tiredList.pop(0)
            #if tiredList.count(1) > 5:
                #print("tired!!!!")

        mouthOpen = calDistance(shape.part(62), shape.part(66)) / calDistance(shape.part(60), shape.part(64))

        if mouthOpen > 0.50:
            #检测到打哈欠
            #cv2.putText(frame, "Yawning", (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            lightBlue()

    #cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
initLight()
