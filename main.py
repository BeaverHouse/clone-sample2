from openpyxl import Workbook
import sys
import json
import glob
import cv2
import os
import calculate

def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

if __name__ == "__main__":
    data = json.loads(sys.argv[1])
    nasPath = data["nasPath"]
    inputDir = data["inputDir"]
    outputDir = data["outputDir"]

    os.makedirs(nasPath + outputDir, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.append(["가로비율", "세로비율"])

    img_arr = glob.glob(nasPath + inputDir + "/*.png")
    for i in img_arr:
        file_name = os.path.basename(i)

        img = cv2.imread(i)
        w, h = img.shape[:2]
        ws.append(calculate.getRatio(w,h))

        gray = increase_brightness(img, 150)
        cv2.imwrite(nasPath + outputDir + "/proc_" + file_name, gray)
    
    wb.save(nasPath + outputDir + "/report.csv")