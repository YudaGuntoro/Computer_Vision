import numpy as np
import cv2
import argparse
import time
import imutils
import serial

#===============================================================================================
colour = 255,255,255
font   = cv2.FONT_HERSHEY_COMPLEX
scale  = 0.5
ser = serial.Serial("/dev/ttyUSB0",115200)

def callback(value):
    pass 
 
    
def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)
 
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255
 
        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)
    v1_min, v2_min, v3_min = 0,150,52
 
def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-w', '--yuda', required=False,
                    help='Use webcam', action='store_true')
    args = vars(ap.parse_args())
 
    if not args['filter'].upper() in ['RGB', 'HSV']:
        ap.error("Please speciy a correct filter.")
 
    return args

def get_trackbar_values(range_filter):
    values = []
 
    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values
#===============================================================================================
def main():
    args = get_arguments()
    range_filter = args['filter'].upper()
    camera = cv2.VideoCapture(1)
    setup_trackbars(range_filter)
    
    while True:
        if args['yuda']:
            ret, frame = camera.read()
 	          frame = imutils.resize(frame, width=400)
	          frame1 = imutils.resize(frame, width=400)
	          cv2.line(frame1,(0,100),(400,100),(0,0,255),1) # ---- 1
            cv2.line(frame1,(0,200),(400,200),(0,0,255),1) # ---- 2
            cv2.line(frame1,(133,0),(133,300),(0,0,255),1) # |||| 1
    	      cv2.line(frame1,(266,0),(266,300),(0,0,255),1) # |||| 2
     	      cv2.line(frame1,(133,233),(266,233),(0,0,255),1) 
            cv2.line(frame1,(133,266),(266,266),(0,0,255),1) 
            cv2.line(frame1,(177,200),(177,300),(0,0,255),1)	    
            cv2.line(frame1,(221,200),(221,300),(0,0,255),1)		    

	    if not ret:
                break
            if range_filter == 'RGB':
                frame = frame.copy()
            else:
                hasil = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
           
#================================================================================================	
	v1_min, v2_min, v3_min = 54,109,54  	
	lower  = np.array([v1_min,v2_min,v3_min])
  upper  = np.array([v1_max, v2_max, v3_max])
#================================================================================================		    
  blur   = cv2.GaussianBlur(frame,(11,11),0)	 
  hasil  = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)    
  mask   = cv2.inRange(hasil,(lower),(upper))
  #mask  = cv2.inRange(hasil,(v1_min,v2_min,v3_min),(v1_max,v2_max,v3_max))	    
  vector = cv2.bitwise_and(frame, frame, mask=mask)
	kernel = np.ones((5,5),np.uint8)
	mask   = cv2.erode(mask, None, iterations=8)
	mask   = cv2.dilate(mask, None, iterations=5)
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		   
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None
  
 	if len(cnts)>0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
        		#center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 			cv2.circle(frame1, (int(x), int(y)), int(radius),(colour),2)
        		#cv2.circle(frame1, center, 3, (0, 0, 255), -1)
        		#cv2.putText(frame1,"", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
        		#cv2.putText(frame1,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
			cv2.putText(frame1,"Objek Terdeteksi",(10,60),font,scale,(255,255,255))
			
			
	if len(cnts)==0:
			x = 0
      y = 0			
	cv2.putText(frame1,"x = %d"%x,(10,25),font,scale,(255,255,255))
	cv2.putText(frame1,"y = %d"%y,(10,40),font,scale,(255,255,255))
	print " Kx %i --- Ky %i" %(x,y)
	y = y+500		
	ser.write(str(x))
	ser.write(str(y))
	cv2.imshow('mask',mask)
	cv2.imshow('Ori',frame1)	
		       
		
        if cv2.waitKey(1) & 0xFF == ord('q'):
    	 	break

if __name__ == '__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()
