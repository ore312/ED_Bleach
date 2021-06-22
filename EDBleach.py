from directKeys import PressKey, ReleaseKey
import keyboard
import time
import json

CONFIG_PATH = "config.json"

PASS_CONTAINER = "passContainer.txt"

#操作関連
mKeyInteract = 18   #"e"
mKeySelect = 57     #"space"
mKeyUp = 17         #"w"
mKeyDown = 31       #"s"
mKeyRight = 32      #"d"
mKeyLeft = 30       #"a"

mTriggerContainer = ""

mLoopDelay = 0
mKeyDelay = 0
mBleachDelayBefore = 0
mBleachDelayAfter = 0

def readConfig(pPath):
    aStr = ""
    with open(pPath, mode="r", encoding="utf-8") as aFNo:
        aStr = aFNo.read()
    return json.loads(aStr)

def readPassList(pPath):
    aStr = ""
    with open(pPath, mode="r", encoding="utf-8") as aFNo:
        aStr = aFNo.read()
    return aStr.split("\n")[0:-1]

def sendKey(pVK):
    PressKey(pVK)
    time.sleep(mKeyDelay)
    ReleaseKey(pVK)
    time.sleep(mKeyDelay)

def selNum(pBNo, pNNo):
    # 1 2 3
    # 4 5 6
    # 7 8 9
    #   0 >

    def getMapNoToIJ(pNo):
        aKeyNoMap = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [-1, 0, 10]
        ]
        for i in range(len(aKeyNoMap)):
            for j in range(len(aKeyNoMap[i])):
                if pNo == aKeyNoMap[i][j]:
                    return i, j
        return None, None

    def isMapEnd(pMap):
        for i in range(len(pMap)):
            for j in range(len(pMap[i])):
                if pMap[i][j] == -1:
                    return False
        return True

    #存在しない番号の時は抜ける
    aBI, aBJ = getMapNoToIJ(pBNo)
    if aBI == None or aBJ == None:
        return
    aNI, aNJ = getMapNoToIJ(pNNo)
    if aNI == None or aNJ == None:
        return

    aMap = [
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1]
    ]

    #行先から徐々に距離をaMapに入れていく
    aNow = 0
    aMap[aNI][aNJ] = aNow
    while isMapEnd(aMap) != True:
        for i in range(len(aMap)):
            for j in range(len(aMap[i])):
                if aMap[i][j] == aNow:
                    #上
                    if 0 <= i - 1:
                        if aMap[i - 1][j] == -1:
                            aMap[i - 1][j] = aNow + 1
                    #下
                    if i + 1 <= len(aMap) - 1:
                        if aMap[i + 1][j] == -1:
                            aMap[i + 1][j] = aNow + 1
                    #右
                    if j + 1 <= len(aMap[i]) - 1:
                        if aMap[i][j + 1] == -1:
                            aMap[i][j + 1] = aNow + 1
                    #左
                    if 0 <= j - 1:
                        if aMap[i][j - 1] == -1:
                            aMap[i][j - 1] = aNow + 1
        aNow += 1

    #debug
    print(aMap)

    #移動手順を取得
    aMove = []
    i = aBI
    j = aBJ
    aNow = aMap[i][j]
    #debug
    print(aNow)
    while aNow != 0:
        aHand = [-1, -1, -1, -1]
        #上
        if 0 <= i - 1:
            aHand[0] = aMap[i - 1][j]
        #下
        if i + 1 <= len(aMap) - 1:
            aHand[1] = aMap[i + 1][j]
        #右
        if j + 1 <= len(aMap[i]) - 1:
            aHand[2] = aMap[i][j + 1]
        #左
        if 0 <= j - 1:
            aHand[3] = aMap[i][j - 1]

        #debug
        print("i:" + str(i) + " j:" + str(j), end=" ")
        print(aHand)

        for k in range(len(aHand)):
            if aHand[k] != -1:
                if aHand[k] <= aNow:
                    if k == 0:
                        i = i - 1
                    elif k == 1:
                        i = i + 1
                    elif k == 2:
                        j = j + 1
                    elif k == 3:
                        j = j - 1
                    aNow = aHand[k]
                    aMove.append(k)
                    break

    aMove.reverse()

    #移動
    for i in aMove:
        if i == 0:
            #debug
            print("上")
            sendKey(mKeyUp)
        elif i == 1:
            #debug
            print("下")
            sendKey(mKeyDown)
        elif i == 2:
            #debug
            print("右")
            sendKey(mKeyRight)
        elif i == 3:
            #debug
            print("左")
            sendKey(mKeyLeft)

    #確定
    #debug
    print("確定")
    sendKey(mKeySelect)

def sendNum(pNumStr):
    aNum = 1
    for i in range(len(pNumStr)):
        selNum(aNum, int(pNumStr[i:i + 1]))
        aNum = int(pNumStr[i:i + 1])
        if len(pNumStr) - 1 == i:
            print("決定")
            selNum(aNum, 10)

def bleachPass(pList):
    for aL in pList:
        if keyboard.is_pressed(mTriggerContainer) != True:
            break
        #debug
        print("インタラクト")
        sendKey(mKeyInteract)
        time.sleep(mBleachDelayBefore)
        sendNum(aL)
        time.sleep(mBleachDelayAfter)

def bleachContainer():
    bleachPass(readPassList(PASS_CONTAINER))

def LoadConfig():
    global mKeyInteract
    global mKeySelect
    global mKeyUp
    global mKeyDown
    global mKeyRight
    global mKeyLeft
    global mTriggerContainer
    global mLoopDelay
    global mKeyDelay
    global mBleachDelayBefore
    global mBleachDelayAfter

    aJson = readConfig(CONFIG_PATH)

    if aJson == None:
        return

    mKeyInteract = aJson.get("KeyInteract")
    mKeySelect = aJson.get("KeySelect")
    mKeyUp = aJson.get("KeyUp")
    mKeyDown = aJson.get("KeyDown")
    mKeyRight = aJson.get("KeyRight")
    mKeyLeft = aJson.get("KeyLeft")

    mTriggerContainer = aJson.get("TriggerContainer")

    mLoopDelay = aJson.get("LoopDelay")
    mKeyDelay = aJson.get("KeyDelay")
    mBleachDelayBefore = aJson.get("BleachDelayBefore")
    mBleachDelayAfter = aJson.get("BleachDelayAfter")

def main():
    LoadConfig()

    while True:
        time.sleep(mLoopDelay)

        if keyboard.is_pressed(mTriggerContainer) == True:
            print("Container")
            bleachContainer()
            continue

if __name__ == "__main__":
    main()
