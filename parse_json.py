import os, json, cv2
import numpy as np

currentPath = os.getcwd()
print(currentPath)
os.chdir(currentPath)

dir_idx = "00000001"

img = cv2.imread("./sample_image/" + dir_idx + ".jpg")

with open("./sample_metadata/" + dir_idx + ".json") as json_file:
    json_data = json.load(json_file)

    for bbox in json_data["shapes"]:
        print(bbox["points"])
        points_arr = bbox["points"]
        topleft = (int(points_arr[0][0]),int(points_arr[0][1]))
        bottomright = (int(points_arr[1][0]),int(points_arr[1][1]))

        # print(topleft, bottomright)
        cv2.rectangle(img,topleft, bottomright,(255,0,0), 3)
        cv2.putText(img,bbox["label"],topleft,cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,0),2, cv2.LINE_AA)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.resize(img, (1920,1080))
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(json_data["shapes"][0]["points"])
    # for data in json_data["info"]:
    #     print(data["altitude"])

