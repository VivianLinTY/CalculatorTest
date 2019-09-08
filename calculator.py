import uiautomator2 as u2
import traceback
import datetime
import cv2
import numpy as np

pkgName = "com.asus.calculator"
logScriptName = "saveErrorLog.sh"

themeColor = None
bgColor = None
textColor = None
isLightTheme = False
calculatorBgAlpha = 0.07
calculatorBgOverlay = [255, 255, 255]
toobarRightX = 0.94
toobarRightY = 0.058
lightitemAlpha = 0.6

d = u2.connect()
d.wait_timeout = 10
d.click_post_delay = 1.5
bugIndex = 0

def saveLog(message):
    global bugIndex
    bugIndex = bugIndex+1
    print("bugIndex:",bugIndex,", message:",message)
    d.shell(['sh',"/sdcard/testFiles/"+logScriptName])

def checkError():
    #check crash or ANR
    if d(resourceId="android:id/aerr_wait").exists:
        saveLog("ANR occurred!!!")
    elif d(resourceId="android:id/aerr_close").exists:
        saveLog("CRASH occurred!!!")
    
def checkAreaColor(object, checkColor, checkX, checkY, isSimilar):  #object:name:String, checkColor:array, checkX,Y:float, isSimilar:boolean
    area = 30
    startX = 0
    startY = 0
    conform = 0
    checkX=int(checkX)
    checkY=int(checkY)
    if checkX -area > 0:
        startX = checkX - area
    endX = startX + (area*2)
    if checkY -area > 0:
        startY = checkY - area
    endY = startY + (area*2)
    for numX in range(int(startX), int(endX)):
        for numY in range(int(startY), int(endY)):
            colorGet = getColorByCoordinate(image ,numX, numY)
            if isSimilar:
                if isSimilarColor(colorGet, checkColor):
                    conform = conform+1
            else:
                if isContrastColor(colorGet, checkColor):
                    conform = conform+1
    if conform == 0:
        saveLog("Object :"+str(object)+" , checkColor:"+str(checkColor))
    return conform > 0

def isSimilarColor(color1, color2): #color:color getten, color2:check color
    array1 = int(color2[0]) - int(color1[0])
    array2 = int(color2[1]) - int(color1[1])
    array3 = int(color2[2]) - int(color1[2])
    distance = pow(array1 ** 2 + array2 ** 2 + array3 ** 2, 0.5)
    return distance < 50
    
def isContrastColor(color1, color2):
    array1 = int(color2[0]) - int(color1[0])
    array2 = int(color2[1]) - int(color1[1])
    array3 = int(color2[2]) - int(color1[2])
    distance = pow(array1 ** 2 + array2 ** 2 + array3 ** 2, 0.5)
    return distance > 150

def setRotationTest(orientation,id):
    if d(resourceId=id).wait(timeout = 5):
        d.set_orientation(orientation)
        checkError()
    else:
        saveLog("View id:"+id+" doesn't exist!")

def rotationBasicTest(activity,id):
    print("rotationTest==> "+activity)
    setRotationTest('l',id)
    time.sleep(1)
    setRotationTest('n',id)
    time.sleep(1)
    setRotationTest('r',id)
    time.sleep(1)
    setRotationTest('n',id)
    time.sleep(1)
    print("rotationTest<== "+activity)

def checkObjectExistByID(id, checkColor):
    if d(resourceId=id).wait(timeout = 5):
        if checkColor is not None:
            realColorX, realColorY =d(resourceId=id).center()
            checkAreaColor(id, checkColor, realColorX, realColorY, True)
        return True
    else:
        saveLog("Object id:"+id+" doesn't exist!")
        return False

def checkObjectExistByPath(path, checkColor):
    if d.xpath(path).exists:
        for checkObject in d.xpath(path).all():
            if checkColor is not None:
                realColorX, realColorY = checkObject.center()
                checkAreaColor(path, checkColor, realColorX, realColorY, True)
            break   #Only check the first one
        return True
    else:
        saveLog("Object path:"+path+" doesn't exist!")
        return False

def checkObjectExistByPathOffset(path, checkColor, offsetX, offsetY):
    if d.xpath(path).exists:
        for checkObject in d.xpath(path).all():
            if checkColor is not None:
                realColorX, realColorY = checkObject.center()
                realColorX = realColorX+offsetX
                realColorY = realColorY+offsetY
                checkAreaColor(path, checkColor, realColorX, realColorY, True)
            break   #Only check the first one
        return True
    else:
        saveLog("Object path:"+path+" doesn't exist!")
        return False

def checkColorbyRelativePosition(path, checkColor, x, y):
    checkAreaColor(path, checkColor, imageWidth*x, imageHeight*y, True)

def getColorByCoordinate(checkImage, x, y):
    return checkImage[int(y),int(x)]
    
def testInputPanel(): #Unit Converter panel
    d(resourceId="com.asus.calculator:id/unit_clear").click()
    if None!=d(resourceId="com.asus.calculator:id/unit_value").get_text():
        saveLog("clear error! getText:"+d(resourceId="com.asus.calculator:id/unit_value").get_text())
    d(resourceId="com.asus.calculator:id/unit_1").click()
    d(resourceId="com.asus.calculator:id/unit_00").click()
    d(resourceId="com.asus.calculator:id/unit_0").click()
    if "1000"!=d(resourceId="com.asus.calculator:id/unit_value").get_text():
        saveLog("input 1000 error! getText:"+d(resourceId="com.asus.calculator:id/unit_value").get_text())
    d(resourceId="com.asus.calculator:id/unit_negative").click()
    if "-1000"!=d(resourceId="com.asus.calculator:id/unit_value").get_text():
        saveLog("input negative error! getText:"+d(resourceId="com.asus.calculator:id/unit_value").get_text())
    d(resourceId="com.asus.calculator:id/unit_2").click()
    d(resourceId="com.asus.calculator:id/unit_3").click()
    d(resourceId="com.asus.calculator:id/unit_4").click()
    d(resourceId="com.asus.calculator:id/unit_5").click()
    d(resourceId="com.asus.calculator:id/unit_6").click()
    d(resourceId="com.asus.calculator:id/unit_7").click()
    d(resourceId="com.asus.calculator:id/unit_8").click()
    d(resourceId="com.asus.calculator:id/unit_9").click()
    if "-100023456789"!=d(resourceId="com.asus.calculator:id/unit_value").get_text():
        saveLog("input numbers error! getText:"+d(resourceId="com.asus.calculator:id/unit_value").get_text())
    d(resourceId="com.asus.calculator:id/unit_del").click()
    if "-10002345678"!=d(resourceId="com.asus.calculator:id/unit_value").get_text():
        saveLog("input del error! getText:"+d(resourceId="com.asus.calculator:id/unit_value").get_text())
    d.press("back")
    time.sleep(1)
    if d(resourceId="com.asus.calculator:id/input_panel_divider").exists:
        saveLog("Close panel error.")
    d(resourceId="com.asus.calculator:id/unit_value").click()
    if d(resourceId="com.asus.calculator:id/input_panel_divider").wait(5):
        d(resourceId="com.asus.calculator:id/unit_done").click()
        time.sleep(1)
        if d(resourceId="com.asus.calculator:id/input_panel_divider").exists:
            saveLog("Done panel error.")
    else:
        saveLog("input_panel doesn't show.")

def checkToolBarColor(page, hasRightButton):
    time.sleep(1)
    toolBarBgColor = bgColor if pageName == "Calculator" else getMergedColor(calculatorBgOverlay, bgColor, calculatorBgAlpha)
    checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton', themeColor)
    checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton', toolBarBgColor if page == "Calculator" else bgColor)
    checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.TextView', themeColor)
    checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.TextView',  toolBarBgColor if page == "Calculator" else bgColor)
    if hasRightButton:
        checkColorbyRelativePosition("Toolbar Icon Right", themeColor,toobarRightX,toobarRightY)
        checkColorbyRelativePosition("Toolbar Icon Right",  toolBarBgColor if page == "Calculator" else bgColor,toobarRightX,toobarRightY)

def getMergedColor(overlayColor, coveredColor, alpha):
    return [int((1.0-alpha)*coveredColor[0]+alpha*overlayColor[0]), int((1.0-alpha)*coveredColor[1]+alpha*overlayColor[1]), int((1.0-alpha)*coveredColor[2]+alpha*overlayColor[2])]
    
def getAlphaColor(color, alpha):
    return getMergedColor(bgColor,color,alpha)

def checkStatusbarColor(page):
    print("Check Staturbar color ==> ", page)
    clock = d(resourceId="com.android.systemui:id/clock")
    if clock.wait(2):
        clockX, clockY = clock.center()
        checkAreaColor(page+" status bar color", themeColor, clockX, clockY, False)
    print("Check Staturbar color <== ", page)

def isColorLight(color):
    b=color[0]/255.0
    g=color[1]/255.0
    r=color[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = 0.5 * (mx+mn)*100
    return l > 50

def saveCropImage(x,y,w,h,fileName):
    crop_img = image[y:y+h, x:x+w]
    cv2.imwrite("D:/"+fileName+".jpg", crop_img)

def swapToAdvancedPanelAndCheck(): #Sometimes swipe will failed, so need to check it
    d(resourceId="com.asus.calculator:id/panelswitch").swipe("left", steps=10)
    time.sleep(1)
    if d(resourceId="com.asus.calculator:id/digit5").exists:
        swapToAdvancedPanelAndCheck()
def swapToSimpledPanelAndCheck(): #Sometimes swipe will failed, so need to check it
    d(resourceId="com.asus.calculator:id/panelswitch").swipe("right", steps=10)
    time.sleep(1)
    if d(resourceId="com.asus.calculator:id/tan").exists:
        swapToSimpledPanelAndCheck()

def getDisableSwitchColor():    #check settings switch button
    return bgColor if isLightTheme else getAlphaColor(textColor, 0.4)
print(datetime.datetime.now()," Start==>")

#init app status
d.app_stop(pkgName)
d.app_clear(pkgName)
d.app_start(pkgName)
time.sleep(2)

#print phone status
phoneInfo = d.info
imageWidth = phoneInfo.get("displayWidth")
imageHeight = phoneInfo.get("displayHeight")
print("phone information:",phoneInfo)
appInfo = d.app_info("com.asus.calculator")
print("app information:",appInfo)

if d(resourceId="android:id/alertTitle").exists:
    time.sleep(0.6)
    d(resourceId="android:id/button2").click()
    time.sleep(0.6)
    d.app_start(pkgName)
    time.sleep(0.6)
    d(resourceId="android:id/button1").click()

#get reference colors
image = d.screenshot(format='opencv')
themeColorReference = d(resourceId="com.asus.calculator:id/button_panel_advanced_right")
if themeColorReference.wait(3):
    themeColorX, themeColorY = themeColorReference.center()
    themeColor = getColorByCoordinate(image, themeColorX, themeColorY - 200)
    bgColorX, bgColorY = d(resourceId="com.asus.calculator:id/digit0").center()
    bgColor = getColorByCoordinate(image, bgColorX, bgColorY)
    textColorX, textColorY = d(resourceId="com.asus.calculator:id/digit1").center()
    textColor = getColorByCoordinate(image, textColorX, textColorY)
    print("themeColor:",themeColor,", bgColor:",bgColor,", textColor:",textColor)
    if isSimilarColor(themeColor, bgColor):
        print("themeColor is similar with bgColor!!?? themeColor:",themeColor,", bgColor:",bgColor)
    if isSimilarColor(textColor, bgColor):
        print("textColor is similar with bgColor!!?? textColor:",textColor,", bgColor:",bgColor)
else:
    saveLog("Object id:"+id+" doesn't exist!")
isLightTheme = isColorLight(bgColor)
calculatorBgAlpha = 0.03 if isLightTheme else 0.07
calculatorBgOverlay = [0, 0, 0] if isLightTheme else [255, 255, 255]

#check calculator activity
pageName = "Calculator"
rotationBasicTest(pageName,"com.asus.calculator:id/display")
time.sleep(2)
checkToolBarColor(pageName, True)
checkStatusbarColor(pageName)
checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton', themeColor)
checkObjectExistByID("com.asus.calculator:id/display", getMergedColor(calculatorBgOverlay, bgColor,calculatorBgAlpha))
checkObjectExistByID("com.asus.calculator:id/panelswitch", None)

#check panel color
opColor = getAlphaColor(textColor, 0.5)
eqColor = getAlphaColor(textColor, 0.203)
checkObjectExistByID("com.asus.calculator:id/digit0", textColor)
checkObjectExistByID("com.asus.calculator:id/digit0", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit1", textColor)
checkObjectExistByID("com.asus.calculator:id/digit1", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit2", textColor)
checkObjectExistByID("com.asus.calculator:id/digit2", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit3", textColor)
checkObjectExistByID("com.asus.calculator:id/digit3", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit4", textColor)
checkObjectExistByID("com.asus.calculator:id/digit4", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit5", textColor)
checkObjectExistByID("com.asus.calculator:id/digit5", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit6", textColor)
checkObjectExistByID("com.asus.calculator:id/digit6", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit7", textColor)
checkObjectExistByID("com.asus.calculator:id/digit7", bgColor)
checkObjectExistByID("com.asus.calculator:id/del_simple", opColor)
checkObjectExistByID("com.asus.calculator:id/del_simple", bgColor)
checkObjectExistByID("com.asus.calculator:id/plus", opColor)
checkObjectExistByID("com.asus.calculator:id/plus", bgColor)
checkObjectExistByID("com.asus.calculator:id/minus", opColor)
checkObjectExistByID("com.asus.calculator:id/minus", bgColor)
checkObjectExistByID("com.asus.calculator:id/mul", opColor)
checkObjectExistByID("com.asus.calculator:id/mul", bgColor)
checkObjectExistByID("com.asus.calculator:id/div", opColor)
checkObjectExistByID("com.asus.calculator:id/div", bgColor)
checkObjectExistByID("com.asus.calculator:id/equal", bgColor)
checkObjectExistByID("com.asus.calculator:id/equal", eqColor)
checkObjectExistByID("com.asus.calculator:id/clear", themeColor)
checkObjectExistByID("com.asus.calculator:id/clear", bgColor)
checkObjectExistByID("com.asus.calculator:id/percent", bgColor)
checkObjectExistByID("com.asus.calculator:id/percent", opColor)
checkObjectExistByID("com.asus.calculator:id/negative", opColor)
checkObjectExistByID("com.asus.calculator:id/negative", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit8", textColor)
checkObjectExistByID("com.asus.calculator:id/digit8", bgColor)
checkObjectExistByID("com.asus.calculator:id/digit9", textColor)
checkObjectExistByID("com.asus.calculator:id/digit9", bgColor)
swapToAdvancedPanelAndCheck()
time.sleep(1)
image = d.screenshot(format='opencv')
checkObjectExistByID("com.asus.calculator:id/m_plus", bgColor)
checkObjectExistByID("com.asus.calculator:id/m_plus", themeColor)
checkObjectExistByID("com.asus.calculator:id/m_minus", bgColor)
checkObjectExistByID("com.asus.calculator:id/m_minus", themeColor)
checkObjectExistByID("com.asus.calculator:id/sin", bgColor)
checkObjectExistByID("com.asus.calculator:id/sin", themeColor)
checkObjectExistByID("com.asus.calculator:id/cos", bgColor)
checkObjectExistByID("com.asus.calculator:id/cos", themeColor)
checkObjectExistByID("com.asus.calculator:id/tan", bgColor)
checkObjectExistByID("com.asus.calculator:id/tan", themeColor)
checkObjectExistByID("com.asus.calculator:id/rightParen", bgColor)
checkObjectExistByID("com.asus.calculator:id/rightParen", themeColor)
checkObjectExistByID("com.asus.calculator:id/leftParen", bgColor)
checkObjectExistByID("com.asus.calculator:id/leftParen", themeColor)
checkObjectExistByID("com.asus.calculator:id/lg", bgColor)
checkObjectExistByID("com.asus.calculator:id/lg", themeColor)
checkObjectExistByID("com.asus.calculator:id/degreeID", bgColor)
checkObjectExistByID("com.asus.calculator:id/degreeID", themeColor)
checkObjectExistByID("com.asus.calculator:id/e", bgColor)
checkObjectExistByID("com.asus.calculator:id/e", themeColor)
checkObjectExistByID("com.asus.calculator:id/negative_advanced", bgColor)
checkObjectExistByID("com.asus.calculator:id/negative_advanced", themeColor)
checkObjectExistByID("com.asus.calculator:id/factorial", bgColor)
checkObjectExistByID("com.asus.calculator:id/factorial", themeColor)
checkObjectExistByID("com.asus.calculator:id/mr", bgColor)
checkObjectExistByID("com.asus.calculator:id/mr", themeColor)
checkObjectExistByID("com.asus.calculator:id/mc", bgColor)
checkObjectExistByID("com.asus.calculator:id/mc", themeColor)
checkObjectExistByID("com.asus.calculator:id/del", bgColor)
checkObjectExistByID("com.asus.calculator:id/del", themeColor)
checkObjectExistByID("com.asus.calculator:id/ln", bgColor)
checkObjectExistByID("com.asus.calculator:id/ln", themeColor)
checkObjectExistByID("com.asus.calculator:id/sqrt", bgColor)
checkObjectExistByID("com.asus.calculator:id/sqrt", themeColor)
checkObjectExistByID("com.asus.calculator:id/pi", bgColor)
checkObjectExistByID("com.asus.calculator:id/pi", themeColor)
checkObjectExistByID("com.asus.calculator:id/power", bgColor)
checkObjectExistByID("com.asus.calculator:id/power", themeColor)
checkObjectExistByID("com.asus.calculator:id/clear_advanced", bgColor)
checkObjectExistByID("com.asus.calculator:id/clear_advanced", themeColor)

#test panel
swapToSimpledPanelAndCheck()
d(resourceId="com.asus.calculator:id/digit1").click()
swapToAdvancedPanelAndCheck()
time.sleep(1)
d(resourceId="com.asus.calculator:id/m_plus").click()
text = str(d(resourceId="com.asus.calculator:id/expressionEditTextID").get_text())
if "1" != text:
    saveLog("1 expewssion error! getText:"+text)
d(resourceId="com.asus.calculator:id/digit2").click()
swapToAdvancedPanelAndCheck()
time.sleep(1)
d(resourceId="com.asus.calculator:id/sin").click()
d(resourceId="com.asus.calculator:id/digit3").click()
d(resourceId="com.asus.calculator:id/digit0").click()
d(resourceId="com.asus.calculator:id/del_simple").click()
swapToAdvancedPanelAndCheck()
time.sleep(1)
d(resourceId="com.asus.calculator:id/rightParen").click()
swapToAdvancedPanelAndCheck()
time.sleep(1)
d(resourceId="com.asus.calculator:id/m_minus").click()
text = str(d(resourceId="com.asus.calculator:id/expressionEditTextID").get_text())
if "2sin(3)" != text:
    saveLog("2sin(3) expewssion error! getText:"+text)
text = str(d(resourceId="com.asus.calculator:id/memory").get_text())
if "M0.89532809" != text:
    saveLog("M0.89532809 calculate error! getText:"+text)
d(resourceId="com.asus.calculator:id/plus").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/cos").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/tan").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/leftParen").click()
d(resourceId="com.asus.calculator:id/digit4").click()
d(resourceId="com.asus.calculator:id/minus").click()
d(resourceId="com.asus.calculator:id/digit5").click()
d(resourceId="com.asus.calculator:id/mul").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/lg").click()
d(resourceId="com.asus.calculator:id/digit6").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/rightParen").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/rightParen").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/rightParen").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/degreeID").click()
d(resourceId="com.asus.calculator:id/degreeID").click()
d(resourceId="com.asus.calculator:id/e").click()
d(resourceId="com.asus.calculator:id/equal").click()
text = str(d(resourceId="com.asus.calculator:id/resultEditTextID").get_text())
if "10467191" not in text:
    saveLog("1.10467191 calculate error! getText:"+text)
d(resourceId="com.asus.calculator:id/clear").click()
text = str(d(resourceId="com.asus.calculator:id/resultEditTextID").get_text())
if "" != text:
    saveLog("1.10467191 clear error! getText:"+text)
time.sleep(1)
d(resourceId="com.asus.calculator:id/digit7").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/negative_advanced").click()
d(resourceId="com.asus.calculator:id/factorial").click()
text = str(d(resourceId="com.asus.calculator:id/resultPreviewText").get_text())
if "5,040" not in text:
    saveLog("-5040 calculator error! getText:"+text)
d(resourceId="com.asus.calculator:id/percent").click()
d(resourceId="com.asus.calculator:id/negative").click()
d(resourceId="com.asus.calculator:id/div").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/sqrt").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/mr").click()
text = str(d(resourceId="com.asus.calculator:id/resultPreviewText").get_text())
if "01895363" not in text:
    saveLog("1.01895363 calculator error! getText:"+text)
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/mc").click()
if d(resourceId="com.asus.calculator:id/memory").exists:
    text = str(d(resourceId="com.asus.calculator:id/memory").get_text())
    if "" != text:
        saveLog("memory clear error! getText:"+text)
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/del").click()
d(resourceId="com.asus.calculator:id/ln").click()
d(resourceId="com.asus.calculator:id/digit8").click()
d(resourceId="com.asus.calculator:id/dot").click()
d(resourceId="com.asus.calculator:id/digit9").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/pi").click()
text = str(d(resourceId="com.asus.calculator:id/resultPreviewText").get_text())
if "39391172" not in text:
    saveLog("3.39391172 calculate error! getText:"+text)
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/rightParen").click()
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/power").click()
d(resourceId="com.asus.calculator:id/digit3").click()
text = str(d(resourceId="com.asus.calculator:id/resultPreviewText").get_text())
if "6524068" not in text:
    saveLog("37.6524068 calculate error! getText:"+text)
swapToAdvancedPanelAndCheck()
d(resourceId="com.asus.calculator:id/clear_advanced").click()
text = str(d(resourceId="com.asus.calculator:id/resultPreviewText").get_text())
if "" != text:
    saveLog("advanced clear error! getText:"+text)
text = str(d(resourceId="com.asus.calculator:id/resultEditTextID").get_text())
if "" != text:
    saveLog("37.6524068 clear error! getText:"+text)
time.sleep(1)

#check unitConverter activity
d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
time.sleep(1)
d(resourceId="com.asus.calculator:id/drawer_unitConverter_item_text").click()
pageName = "UnitConverter"
time.sleep(1)
rotationBasicTest(pageName,"com.asus.calculator:id/content_layout")
time.sleep(2)
image = d.screenshot(format='opencv')
checkToolBarColor(pageName, True)
checkStatusbarColor(pageName)
print(pageName," tabcontent test ==>")
index = 0
totalItem = 7
for times in range(1, totalItem+1):    #unit icon seven items
    #get screenshot and check color
    image = d.screenshot(format='opencv')
    unitIconList = d.xpath('//*[@resource-id="com.asus.calculator:id/indicator"]/android.widget.LinearLayout[1]/android.widget.TextView')
    unitIcon = unitIconList.all()[index]
    unitIconX, unitIconY = unitIcon.center()
    showItemsNumber = 0
    size = len(unitIconList.all())
    checkIndex = 1
    for unitCheckIcon in unitIconList.all():
        showItemsNumber = showItemsNumber+1
        #Sometimes the last one doesn't show in screen, but it's OK and depends on screen size
        if (size > 4 and checkIndex > 1 and checkIndex <= 4) or size <= 4:
            unitCheckIconX, unitCheckIconY = unitCheckIcon.center()
            if abs(unitIconX-unitCheckIconX) < 10:
                checkAreaColor("unitCheckIcon "+str(times)+" color", themeColor, unitCheckIconX, unitCheckIconY, True)
            else:
                checkAreaColor("unitCheckIcon "+str(times)+" color", textColor, unitCheckIconX, unitCheckIconY, True)
            checkAreaColor("unitCheckIcon "+str(times)+" bgcolor", bgColor, unitCheckIconX, unitCheckIconY, True)
        checkIndex = checkIndex+1
    #test entering value
    if d(resourceId="com.asus.calculator:id/unit_value").exists:
        d(resourceId="com.asus.calculator:id/unit_value").click()
        if d(resourceId="com.asus.calculator:id/input_panel_divider").wait(5):
            testInputPanel()
        else:
            saveLog(int(times)+" input_panel doesn't show.")
    else:
        saveLog(int(times)+" unit_value field is Disappeared.")
    #test drop down menu
    if d(resourceId="com.asus.calculator:id/unit_from").exists:
        d(resourceId="com.asus.calculator:id/unit_from").click()
        dropDownSize = np.size(d.xpath('//android.widget.ListView/android.widget.CheckedTextView').all())
        d.xpath('//android.widget.ListView/android.widget.CheckedTextView[1]').click()
        for dropDownIndex in range(dropDownSize+1):
            if dropDownIndex > 1:
                d(resourceId="com.asus.calculator:id/unit_from").click()
                time.sleep(1)
                d.xpath('//android.widget.ListView/android.widget.CheckedTextView['+str(dropDownIndex)+']').click()
                dropDownIndex = dropDownIndex+1
                time.sleep(1)
    else:
        saveLog(int(times)+" drop down menu doesn't show.")   
    #click next button and refresh index
    try:
        unitIconList.all()[index+1].click()
        if index < int(showItemsNumber/2):
            index = index+1
        elif (totalItem - times) < showItemsNumber/2:
            index = index+1
    except Exception as e:
        if times != totalItem:
            print("e:",e,", times=",times,", totalItem=",totalItem, ", showItemsNumber=", showItemsNumber)
    time.sleep(1)
print(pageName,"UnitConverter tabcontent test <==")

d.click_post_delay = 0.8
#check Currency activity
d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
time.sleep(1)
d(resourceId="com.asus.calculator:id/drawer_currencyConverter_item_text").click()
pageName = "Currency"
time.sleep(1)
rotationBasicTest(pageName,"com.asus.calculator:id/view_container")
time.sleep(2)
image = d.screenshot(format='opencv')
checkToolBarColor(pageName, True)
checkStatusbarColor(pageName)
print(pageName," content test ==>")
itemParentPath = '//*[@resource-id="com.asus.calculator:id/rateItemList"]/android.widget.RelativeLayout'
itemLayoutIndex = 1
#cehck currency color
for itemLayout in d.xpath(itemParentPath).all():
    checkObjectExistByPath(itemParentPath+"["+str(itemLayoutIndex)+"]/android.widget.TextView", themeColor if itemLayoutIndex == 1 else textColor)
    checkObjectExistByPath(itemParentPath+"["+str(itemLayoutIndex)+"]/android.widget.RelativeLayout[1]/android.widget.EditText", textColor)
    checkObjectExistByPath(itemParentPath+"["+str(itemLayoutIndex)+"]/android.widget.RelativeLayout[1]/android.widget.TextView", getAlphaColor(textColor, lightitemAlpha))
    itemLayoutIndex = itemLayoutIndex+1
checkObjectExistByID("com.asus.calculator:id/fab", themeColor)
d(resourceId="com.asus.calculator:id/fab").click()
print(pageName," content test <==")

#check Currency Add activity
time.sleep(1)
d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
time.sleep(1)
d(resourceId="com.asus.calculator:id/fab").click()
pageName = "Currency Add"
time.sleep(1)
rotationBasicTest(pageName,"com.asus.calculator:id/root_layout")
time.sleep(2)
image = d.screenshot(format='opencv')
checkToolBarColor(pageName, True)
checkStatusbarColor(pageName)
print(pageName," content test ==>")
itemAddParentPath = '//*[@resource-id="com.asus.calculator:id/codeItemList"]/android.widget.RelativeLayout'
itemLayoutIndex = 1
for itemLayout in d.xpath(itemAddParentPath).all():
    itemPath = itemAddParentPath+"["+str(itemLayoutIndex)+"]/android.widget.TextView"
    if itemLayoutIndex == 1:
        checkObjectExistByPathOffset(itemPath, textColor, -100, 0)
    else:
        d.xpath(itemPath).click()
    itemLayoutIndex = itemLayoutIndex+1
d.click(toobarRightX, toobarRightY)
time.sleep(1)
image = d.screenshot(format='opencv')
itemParentPath = '//*[@resource-id="com.asus.calculator:id/rateItemList"]/android.widget.RelativeLayout'
itemLayoutIndex = 1
for itemLayout in d.xpath(itemParentPath).all():
    itemLayoutIndex = itemLayoutIndex+1
if itemLayoutIndex < 9:
    saveLog("Add currency failed")
print(pageName," content test <==")

#check Currency Edit activity
checkObjectExistByID("com.asus.calculator:id/editCurrencyList", themeColor)
d(resourceId="com.asus.calculator:id/editCurrencyList").click()
pageName = "Currency Edit"
time.sleep(1)
rotationBasicTest(pageName,"com.asus.calculator:id/currency_edit_list")
time.sleep(2)
image = d.screenshot(format='opencv')
checkToolBarColor(pageName, False)
checkStatusbarColor(pageName)
print(pageName," content test ==>")
itemEditParentPath = '//*[@resource-id="com.asus.calculator:id/currency_edit_list"]/android.widget.LinearLayout'
for i in range(1,5):
    if d.xpath(itemEditParentPath+"["+str(i)+"]/android.widget.LinearLayout[1]/android.widget.ImageButton[1]").exists:
        d.xpath(itemEditParentPath+"["+str(i)+"]/android.widget.LinearLayout[1]/android.widget.ImageButton[1]").click()
        d(resourceId="android:id/button1").click()
        time.sleep(1)
itemLayoutIndex = 1  
for itemLayout in d.xpath(itemEditParentPath).all():
    checkObjectExistByPath(itemEditParentPath+"["+str(itemLayoutIndex)+"]/android.widget.LinearLayout[1]/android.widget.ImageButton[1]", getAlphaColor(textColor, lightitemAlpha))
    checkObjectExistByPath(itemEditParentPath+"["+str(itemLayoutIndex)+"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]", getAlphaColor(textColor, lightitemAlpha))
    itemLayoutIndex = itemLayoutIndex+1
dragX = 0
dragY = 0
for firstLayout in d.xpath('//*[@resource-id="com.asus.calculator:id/currency_edit_list"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView').all():
    dragX, dragY = firstLayout.center()
for move4Image in d.xpath('//*[@resource-id="com.asus.calculator:id/currency_edit_list"]/android.widget.LinearLayout[4]/android.widget.LinearLayout[1]/android.widget.ImageView').all():
    downX, downY = move4Image.center()
    d.drag(downX, downY, dragX, dragY, 0.5)
for move5Image in d.xpath('//*[@resource-id="com.asus.calculator:id/currency_edit_list"]/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.ImageView').all():
    downX, downY = move5Image.center()
    d.drag(downX, downY, dragX, dragY, 0.5)
for move8Image in d.xpath('//*[@resource-id="com.asus.calculator:id/currency_edit_list"]/android.widget.LinearLayout[8]/android.widget.LinearLayout[1]/android.widget.ImageView').all():
    downX, downY = move8Image.center()
    d.drag(downX, downY, dragX, dragY, 0.5)
time.sleep(1)
if d(text="AOA").exists:
    angX, angY = d(text="AOA").center()
    if abs(dragY-angY) > 5:
        saveLog("Drag currency error!")
d.press("back")
print(pageName," content test <==")

#back to calculator Acitivty
d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
time.sleep(1)
d(resourceId="com.asus.calculator:id/drawer_calculator_item_text").click()
pageName = "Calculator"
image = d.screenshot(format='opencv')
checkObjectExistByID("com.asus.calculator:id/display", getMergedColor(calculatorBgOverlay, bgColor,calculatorBgAlpha))
if checkObjectExistByID("com.asus.calculator:id/toolbar", getMergedColor(calculatorBgOverlay, bgColor,calculatorBgAlpha)):
    d.click(toobarRightX, toobarRightY)
    time.sleep(1)
    if d.xpath('//android.widget.ListView/android.widget.LinearLayout').exists:
        d.xpath('//android.widget.ListView/android.widget.LinearLayout[1]').click()
        #Go to history acitivty
        pageName = "History"
        time.sleep(1)
        rotationBasicTest(pageName,"com.asus.calculator:id/root_layout")
        time.sleep(2)
        image = d.screenshot(format='opencv')
        checkToolBarColor(pageName, True)
        checkStatusbarColor(pageName)
        print(pageName," content test ==>")
        historyIndex = 1
        for itemLayout in d.xpath('//*[@resource-id="com.asus.calculator:id/history_listview"]/android.widget.RelativeLayout').all():
            checkObjectExistByPath('//*[@resource-id="com.asus.calculator:id/history_listview"]/android.widget.RelativeLayout['+str(historyIndex)+']/android.widget.LinearLayout[1]/android.widget.TextView', bgColor)
            historyIndex = historyIndex+1
        if historyIndex < 3:
            saveLog("History error! Only "+str(historyIndex)+" record(s).")
        print(pageName," content test <==")
         #Go to history delete acitivty
        d.click(toobarRightX, toobarRightY)
        time.sleep(1)
        d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
        time.sleep(1)
        d.click(toobarRightX, toobarRightY)
        pageName = "History Delete"
        time.sleep(1)
        rotationBasicTest(pageName,"com.asus.calculator:id/root_layout")
        time.sleep(2)
        image = d.screenshot(format='opencv')
        checkToolBarColor(pageName, True)
        checkStatusbarColor(pageName)
        print(pageName," content test ==>")
        itemIndex = 1
        selectAllId = "com.asus.calculator:id/check_select_all"
        selectAllX, selectAllY = d(resourceId=selectAllId).center()
        itemLayoutPath = '//*[@resource-id="com.asus.calculator:id/history_listview"]/android.widget.RelativeLayout'
        for itemLayout in d.xpath(itemLayoutPath).all():
            checkBoxPath = itemLayoutPath+"["+str(itemIndex)+"]/android.widget.CheckBox"
            checkObjectExistByPath(checkBoxPath, bgColor)
            checkObjectExistByPath(checkBoxPath, getAlphaColor(textColor, lightitemAlpha))
            for checkBox in d.xpath(checkBoxPath).all():
                selectAllX, itemY = checkBox.center()
            itemIndex = itemIndex+1
        checkAreaColor(selectAllId, getAlphaColor(textColor, lightitemAlpha), selectAllX, selectAllY, True)
        print("Select select all.")
        d(resourceId=selectAllId).click()
        time.sleep(1)
        image = d.screenshot(format='opencv')
        itemIndex = 1
        for itemLayout in d.xpath(itemLayoutPath).all():
            checkBoxPath = itemLayoutPath+"["+str(itemIndex)+"]/android.widget.CheckBox"
            for checkBox in d.xpath(checkBoxPath).all():
                checkObjectExistByPath(checkBoxPath, themeColor)
            itemIndex = itemIndex+1
            time.sleep(1)
        print("Unselect select all.")
        d(resourceId=selectAllId).click()
        time.sleep(1)
        image = d.screenshot(format='opencv')
        for itemLayout in d.xpath(itemLayoutPath).all():
            checkBoxPath = itemLayoutPath+"["+str(itemIndex)+"]/android.widget.CheckBox"
            for checkBox in d.xpath(checkBoxPath).all():
                checkObjectExistByPath(checkBoxPath, getAlphaColor(textColor, lightitemAlpha))
            itemIndex = itemIndex+1
            time.sleep(1)
        itemIndex = 1
        for itemLayout in d.xpath(itemLayoutPath).all():
            checkBoxPath = itemLayoutPath+"["+str(itemIndex)+"]/android.widget.CheckBox"
            for checkBox in d.xpath(checkBoxPath).all():
                checkBox.click()
                time.sleep(1)
                image = d.screenshot(format='opencv')
                time.sleep(1)
                checkObjectExistByPath(checkBoxPath, themeColor)
            itemIndex = itemIndex+1
            time.sleep(1)
        checkAreaColor(selectAllId, getAlphaColor(themeColor, lightitemAlpha), selectAllX, selectAllY, True)
        d.click(toobarRightX, toobarRightY)
        if checkObjectExistByID("com.asus.calculator:id/nohistory_text", textColor) == False:
            saveLog("No history text doesn't show!")
        #back to calculator Acitivty
        d.xpath('//*[@resource-id="com.asus.calculator:id/toolbar"]/android.widget.ImageButton[1]').click()
        print(pageName," content test <==")
    else:
        saveLog("Menu dialog doesn't show!")
else:
    saveLog("toolbar doesn't show!")

#back to calculator Acitivty
time.sleep(1)
pageName = "Calculator"
image = d.screenshot(format='opencv')
if checkObjectExistByID("com.asus.calculator:id/toolbar", getMergedColor(calculatorBgOverlay, bgColor,calculatorBgAlpha)):
    d.click(toobarRightX, toobarRightY)
    time.sleep(1)
    if d.xpath('//android.widget.ListView/android.widget.LinearLayout').exists:
        d.xpath('//android.widget.ListView/android.widget.LinearLayout[2]').click()
        #Go to settings acitivty
        pageName = "Settings"
        time.sleep(1)
        rotationBasicTest(pageName,"com.asus.calculator:id/setting_content")
        time.sleep(2)
        image = d.screenshot(format='opencv')
        checkToolBarColor(pageName, False)
        checkStatusbarColor(pageName)
        print(pageName," content test ==>")
        itemPath = '//*[@resource-id="android:id/list"]/android.widget.LinearLayout'
        itemIndex = 1
        switchIndex = 1
        isChangeColor = False
        for itemLayout in d.xpath(itemPath).all():
            parentPath = itemPath+"["+str(itemIndex)+"]/"
            textPath = parentPath+"android.widget.RelativeLayout[1]/android.widget.TextView"
            switchPath = itemPath+"["+str(itemIndex)+"]/android.widget.LinearLayout[1]/android.widget.Switch"
            if d.xpath(parentPath+"android.widget.TextView[1]").exists:
                image = d.screenshot(format='opencv')
                checkObjectExistByPath(parentPath+"android.widget.TextView", themeColor)
            else:
                if d.xpath(switchPath).exists:
                    image = d.screenshot(format='opencv')
                    if isChangeColor == False:
                        checkObjectExistByPath(textPath, textColor)
                    if switchIndex == 1:
                        checkObjectExistByPath(switchPath, getDisableSwitchColor())
                        d.xpath(switchPath+"[1]").click()
                        time.sleep(1)
                        image = d.screenshot(format='opencv')
                        checkObjectExistByPath(switchPath,themeColor)
                        #float calculator
                        if d.xpath('//android.widget.RelativeLayout[1]').exists:
                            d.click(0.079, 0.062)
                            image = d.screenshot(format='opencv')
                            checkObjectExistByID("com.asus.calculator:id/display_float", themeColor)
                            checkObjectExistByID("com.asus.calculator:id/digit1", bgColor)
                            checkObjectExistByID("com.asus.calculator:id/digit1", textColor)
                            checkObjectExistByID("com.asus.calculator:id/digit5", bgColor)
                            checkObjectExistByID("com.asus.calculator:id/digit5", textColor)
                            checkObjectExistByID("com.asus.calculator:id/digit9", bgColor)
                            checkObjectExistByID("com.asus.calculator:id/digit9", textColor)
                            checkObjectExistByID("com.asus.calculator:id/equal", themeColor)
                            checkObjectExistByID("com.asus.calculator:id/equal", bgColor)
                            checkObjectExistByID("com.asus.calculator:id/float_delete", themeColor)
                            checkObjectExistByID("com.asus.calculator:id/float_delete", bgColor)
                            checkObjectExistByID("com.asus.calculator:id/minus", themeColor)
                            checkObjectExistByID("com.asus.calculator:id/minus", getMergedColor(calculatorBgOverlay, bgColor, calculatorBgAlpha))
                        else:
                            saveLog("floating calculator doesn't show!!")
                        d.xpath(switchPath+"[1]").click()
                        time.sleep(1)
                    elif switchIndex == 2:
                        image = d.screenshot(format='opencv')
                        checkObjectExistByPath(switchPath,themeColor)
                        d.xpath(switchPath+"[1]").click()
                        time.sleep(1)
                        image = d.screenshot(format='opencv')
                        checkObjectExistByPath(switchPath,getDisableSwitchColor())
                        d.xpath(switchPath+"[1]").click()
                        time.sleep(1)
                    switchIndex = switchIndex+1
                else:
                    image = d.screenshot(format='opencv')
                    textExists = False
                    if isChangeColor == False:
                        textExists = checkObjectExistByPath(textPath, textColor)
                    else:
                        textExists = d.xpath(textPath+"[1]").exists
                    if textExists:
                        d.xpath(textPath+"[1]").click()
                        itemPath = '//android.widget.ListView/android.widget.LinearLayout'
                        image = d.screenshot(format='opencv')
                        if checkObjectExistByPath(itemPath, bgColor):
                            size = len(d.xpath(itemPath).all())
                            clickIndex = (2 if isLightTheme else 1) if size == 3 else 1
                            currentIndex = 1
                            for item in d.xpath(itemPath).all():
                                if currentIndex == clickIndex:
                                    item.click()
                                currentIndex+=1
                            if 3 == size:   #change color dropdown
                                print("Change theme")
                                image = d.screenshot(format='opencv')
                                bgColor = getColorByCoordinate(image ,int(imageWidth-1), int(imageHeight-1))
                                currentTheme = isColorLight(bgColor)
                                if currentTheme == isLightTheme:
                                    saveLog("Change theme color error!")
                                else:
                                    isLightTheme = currentTheme
                                    calculatorBgAlpha = 0.03 if isLightTheme else 0.07
                                    calculatorBgOverlay = [0, 0, 0] if isLightTheme else [255, 255, 255]
            itemIndex = itemIndex+1
        print(pageName," content test <==")
    else:
        saveLog("Menu dialog doesn't show!")
else:
    saveLog("toolbar doesn't show!")

checkError()
