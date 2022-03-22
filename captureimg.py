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

    # print("altitude : ", altitude)
    # print("newheight : ", newheight, "newwidth : ", newwidth)

    pts1 = np.float32([[0,0],[0,img_height],[img_width,0],[img_width,img_height]])
    pts2 = np.float32([[0,0],[(img_width - newwidth)/2 ,newheight],[img_width,0],[(img_width + newwidth)/2,newheight]])
    
    return cv2.getPerspectiveTransform(pts1, pts2)
    
def onChange(x):
    pass

cap = cv2.VideoCapture("./sample_image/%8d.jpg")
cv2.namedWindow('video', cv2.WINDOW_NORMAL)

cv2.createTrackbar('Low threshold', 'video', 30, 255, onChange)
cv2.createTrackbar('High threshold', 'video', 90, 255, onChange)
cv2.createTrackbar('Hough threshold', 'video', 100, 300, onChange)

# pts1 = np.float32([[0,0],[0,2160],[3840,0],[3840,2160]])
# pts2 = np.float32([[0,0],[1089,1803],[3840,0],[2751,1803]])

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        
        ####### Parse json to get data  #######

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

                # cv2.rectangle(frame ,topleft, bottomright,(255,0,0), 3)

        ####### Display Midpoint  #######
        h, w = frame.shape[:2]
        
        cv2.circle(frame, (int(w/2), int(h/2)), 30, (255, 255, 255), 3)
        
        ####### Grayscale and Canny Edge detector  #######

        # low = cv2.getTrackbarPos('Low threshold', 'video')
        # high = cv2.getTrackbarPos('High threshold', 'video')

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.GaussianBlur(frame,(31,31),0)
        # frame = cv2.Canny(frame, low, high)
        

        ####### Hough line detection #######

        # houghThresh = cv2.getTrackbarPos('Hough threshold', 'video')
        # 
        # h, w = frame.shape[:2]
        # lines = cv2.HoughLines(frame, 1, np.pi/180, houghThresh)
        # 
        # if lines is not None:
        #     for line in lines:
        #         r,theta = line[0]
        #         tx, ty = np.cos(theta), np.sin(theta)
        #         x0, y0 = tx*r, ty*r
        #         
        #         # cv2.circle(frame , (abs(x0), abs(y0)), 3, (0,0,255), -1)
        #         
        #         x1, y1 = int(x0 + w*(-ty)), int(y0 + h * tx)
        #         x2, y2 = int(x0 - w*(-ty)), int(y0 - h * tx)
        #         
        #         cv2.line(frame, (x1, y1), (x2, y2), (255,255,255), 3)

        # lines = cv2.HoughLinesP(frame, 1, np.pi/180, 10, None, 20, 2)
        # for line in lines:
        #     print(line)
        #     x1, y1, x2, y2 = line[0]
        #     cv2.line(frame, (x1,y1), (x2, y2), (255,255,255), 8)
       

        ####### Warp Matrix  #######

        warpMatrix = getWarpMatrix(cam_alt, cam_angle)
        frame = cv2.warpPerspective(frame, warpMatrix, (3840,2160))

        ####### Corner Detection  #######

        # corners = cv2.goodFeaturesToTrack(frame, 30, 0.3, 5, blockSize=3, useHarrisDetector=True, k=0.03)
        # if corners is not None:
        #     for i in corners:
        #         cv2.circle(frame, tuple(i[0]), 30, (255, 255, 255), 3)

        #################################
        cv2.imshow('video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
