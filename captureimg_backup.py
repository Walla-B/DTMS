import os,cv2, json

os.chdir(os.getcwd())

cap = cv2.VideoCapture("./sample_image/%8d.jpg")

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)

    if ret:

        frameNo = '{0:08d}'.format(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        print(frameNo)

        with open("./sample_metadata/" + frameNo + ".json") as json_file:
            json_data = json.load(json_file)

            for bbox in json_data["shapes"]:
                points_arr = bbox["points"]

                topleft = (int(points_arr[0][0]),int(points_arr[0][1]))
                bottomright = (int(points_arr[1][0]),int(points_arr[1][1]))

                print(topleft, bottomright)

                cv2.rectangle(frame ,topleft, bottomright,(255,0,0), 3)
        
        cv2.imshow('video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
