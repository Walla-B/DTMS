import os,cv2, json, math
import numpy as np

os.chdir(os.getcwd())

def getWarpMatrix(altitude, capture_angle):
    img_width, img_height = 3840, 2160
    width_fov, height_fov = math.radians(77), math.radians(77 * (img_height / img_width))
    # print("height_fov : ",math.degrees(height_fov))
    angle = math.radians(capture_angle)

    lo_ray_dist = altitude / math.cos(angle - (height_fov/2))
    hi_ray_dist = altitude / math.cos(angle + (height_fov/2))

    bottom_half_dist = lo_ray_dist * math.tan(width_fov/2)
    top_half_dist = hi_ray_dist * math.tan(width_fov/2)
    
    # print(altitude * math.tan(angle + (height_fov/2)))
    mid_dist = altitude * (math.tan(angle + (height_fov/2)) - math.tan(angle - (height_fov/2)))
    top_bottom_ratio = top_half_dist/bottom_half_dist
    top_height_ratio = top_half_dist * 2 /mid_dist

    newheight = int(img_width/top_height_ratio)
    newwidth = int(img_width/top_bottom_ratio)

    print("altitude : ", altitude)
    print("newheight : ", newheight, "newwidth : ", newwidth)

    pts1 = np.float32([[0,0],[0,img_height],[img_width,0],[img_width,img_height]])
    pts2 = np.float32([[0,0],[(img_width - newwidth)/2 ,newheight],[img_width,0],[(img_width + newwidth)/2,newheight]])
    
    return cv2.getPerspectiveTransform(pts1, pts2)
    

cap = cv2.VideoCapture("./sample_image/%8d.jpg")

# pts1 = np.float32([[0,0],[0,2160],[3840,0],[3840,2160]])
# pts2 = np.float32([[0,0],[1089,1803],[3840,0],[2751,1803]])

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)

    if ret:

        frameNo = '{0:08d}'.format(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        print(frameNo)

        with open("./sample_metadata/" + frameNo + ".json") as json_file:
            json_data = json.load(json_file)

            cam_alt = float(json_data["info"]["altitude"])
            cam_angle = float(json_data["info"]["angle"])

            for bbox in json_data["shapes"]:
                points_arr = bbox["points"]

                topleft = (int(points_arr[0][0]),int(points_arr[0][1]))
                bottomright = (int(points_arr[1][0]),int(points_arr[1][1]))

                # print(topleft, bottomright)
                cv2.rectangle(frame ,topleft, bottomright,(255,0,0), 3)

        warpMatrix = getWarpMatrix(cam_alt, cam_angle)
        dst = cv2.warpPerspective(frame, warpMatrix, (3840,2160))
        # cv2.imshow('video', frame)
        cv2.imshow('video', dst)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
