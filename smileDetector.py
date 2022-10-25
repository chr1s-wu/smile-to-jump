import cv2
import win32api
import win32con

def keybd_event(VK_CODE):
    VK_CODE = int(VK_CODE)
    win32api.keybd_event(VK_CODE, 0, 0, 0)
    win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
pre_smile = False

while(True):
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, 1.3, 2  )
    img = frame
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        face_area = img[y:y+h, x:x+w]

        smiles = smile_cascade.detectMultiScale(face_area, scaleFactor= 1.2, minNeighbors=65, minSize=(25, 25),flags=cv2.CASCADE_SCALE_IMAGE)
        for (ex,ey,ew,eh) in smiles:
            cv2.rectangle(face_area,(ex,ey),(ex+ew,ey+eh),(0,0,255),1)
            cv2.putText(img,'Smile',(x,y-7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)

        if len(smiles) != 0:
            if not pre_smile:
                keybd_event(32)
                pre_smile = True
        else:
            pre_smile = False

    cv2.imshow('frame2',img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()