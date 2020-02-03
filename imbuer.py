import numpy as np
import cv2 as cv
import pandas as pd

#Loading CSV values and video
cap = cv.VideoCapture('/home/jakyx/Storage/Marko stuff/mjaklin_NSA/NSA_4_rekr_aceton/NSA_4_rekr_aceton.avi')
csv = open('/home/jakyx/Storage/Marko stuff/mjaklin_NSA/NSA_4_rekr_aceton/NSA_4_rekr_aceton.txt', "r")

#Defining output
output = '/home/jakyx/Desktop/Python scripts/NSA_4_rekr_aceton_subtitled.avi'


#Loading csv(TextWrapper object)
csv.seek(0)
p = pd.read_csv(csv, sep = ";")
p = p.reset_index()
p.columns = ["Time", "Temperature"]
df = p.to_numpy()
df = np.delete(df,0,0)


#Getting frame's timestamps
cap.set(cv.CAP_PROP_POS_MSEC, 0)
frame_timestamps = []
i = 0
while True:
    i = i + 1
    h = cap.grab()
    frame_time = cap.get(cv.CAP_PROP_POS_MSEC)
    frame_timestamps.append(frame_time/1000)
    print(i, end='\r', flush=True)
    if (i % 1000) == 0:
        print(i, end='\r', flush=True)

    if h == False:
        break


#Determining relations between frames and temperature
frame_temp = []
frame = 1
for frame_time in frame_timestamps:
    print(frame, end='\r', flush=True)
    time_list = []
    for element in df:
        temp_str = element[0].replace(',', '.')
        time_diffrence = abs(frame_time - float(temp_str))
        time_list.append(time_diffrence)

    time_list = np.asarray(time_list)
    a = [frame, df[np.argmin(time_list)][1]]
    frame_temp.append(a)
    time_list = time_list.tolist()
    frame += 1


#Initializing output video
cap.set(cv.CAP_PROP_POS_MSEC, 0)
fps = cap.get(cv.CAP_PROP_FPS)
maxwidth = cap.get(cv.CAP_PROP_FRAME_WIDTH)
maxheight = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
fourcc = cv.VideoWriter_fourcc(*'MJPG')
out = cv.VideoWriter(output, int(fourcc), int(fps), (int(maxwidth), int(maxheight)))

#Imbuing temperature on a frame
i = 0
display = False
while(cap.isOpened()):
    print(i, end='\r', flush=True)
    ret, frame = cap.read()
    cv.putText(frame, frame_temp[i][1], (10,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA)
    if display:
        cv.imshow('image', frame)
        cv.waitKey(0)
        cv.destroyAllWindows()

    out.write(frame)
    i += 1
    if ret == False:
        break

cap.release()
out.release()
cv.destroyAllWindows()
