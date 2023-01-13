import cv2 #opencv library 
from password import Password # Password class implementation

# Landmarks class for face
class LandMarksFace(Password):
    
    #constructor for LandMarks   class
    def __init__(self):
        self.idList_Eye = [145, 130, 159, 243, 463, 359, 374, 386]
        self.idList_Lips = [61, 0, 17, 291]
        self.idList_Eyebrow = [55, 65, 52, 53, 46, 285, 295, 282, 283, 276, 159, 386]
        self.TotalList = []
        self.finger_count = []
    
    #function for calculate eyes
    def calculateEye(self,img, face, detector):
        eye = face[0]
        for id in self.idList_Eye:
            cv2.circle(img, eye[id], 3, (0,0,255), cv2.FILLED)

            left_eye_up = eye[159]
            left_eye_down = eye[23]
            left_eye_left = eye[130]
            left_eye_right = eye[243]
            right_eye_up = eye[463]
            right_eye_down = eye[359]
            right_eye_left = eye[374]
            right_eye_right = eye[386]

            Vertical_lenght_leftEye, _ = detector.findDistance(left_eye_up, left_eye_down)
            Horizontal_lenght_leftEye, _ = detector.findDistance(left_eye_left, left_eye_right)
            Vertical_lenght_rightEye, _ = detector.findDistance(right_eye_up, right_eye_down)
            Horizontal_lenght_rightEye, _ = detector.findDistance(right_eye_left, right_eye_right)

            ratio_leftEye = int((Vertical_lenght_leftEye / Horizontal_lenght_leftEye) * 100)
            ratio_rightEye = int((Vertical_lenght_rightEye / Horizontal_lenght_rightEye) * 10)
            self.decisionEyes(ratio_rightEye,ratio_leftEye)

    #function for calculate mouth
    def calculateMouth(self,img, face, detector):

        lips = face[0]
        for id in self.idList_Lips:
            cv2.circle(img, lips[id], 2, (31,31,31), cv2.FILLED)

            lips_up = lips[0]
            lips_down = lips[17]
            lips_left = lips[61]
            lips_right = lips[291]

            cv2.line(img, lips_up, lips_down, (255,255,255), 2)
            cv2.line(img, lips_left, lips_right, (255,255,255), 2)
        
            Horizontal_lenght_lips, _ = detector.findDistance(lips_left, lips_right)
            Vertical_lenght_lips, _ = detector.findDistance(lips_up, lips_down)

            Lips = float(Horizontal_lenght_lips / Vertical_lenght_lips) * 10
            self.decisionMouth(Lips)

    #function for calculate eyebrow
    def calculateEyebrow(self,img, face, detector):
        eyeB = face[0]
        for id in self.idList_Eyebrow:
            left_right = eyeB[285]
            left_left = eyeB[276]
            left_mid = eyeB[52]
            left_eyemid = eyeB[159]
            right_right = eyeB[55]
            right_left = eyeB[46]
            right_mid = eyeB[282]
            right_eyemid = eyeB[386]

            cv2.line(img, left_left, left_right, (255,255,255), 2)
            cv2.line(img, right_left, right_right, (255,255,255), 2)
            cv2.line(img, left_mid, left_eyemid, (255,255,255), 2)
            cv2.line(img, right_eyemid, right_mid, (255,255,255), 2)

            Horizontal_lenght_left, _ = detector.findDistance(left_left, left_right)
            Vertical_lenght_left, _ = detector.findDistance(left_mid, left_eyemid)

            Horizontal_lenght_right, _ = detector.findDistance(right_right, right_left)
            Vertical_lenght_right, _ = detector.findDistance(right_mid, right_eyemid)

            ratio_eyebrow_left = (Horizontal_lenght_left / Vertical_lenght_left) * 100
            ratio_eyebrow_right = (Horizontal_lenght_right/Vertical_lenght_right) * 100
            #print("\nleft: ",ratio_eyebrow_left,'\nright: ',ratio_eyebrow_right)
            self.decisionEyebrows(ratio_eyebrow_left,ratio_eyebrow_right)

    #function for decision eyes
    def decisionEyes(self,ratr,ratl): #1
        """Make a decision the eyes blinked or not

        Args:
            ratr (int): right eye blink ratio
            ratl (int): left eyeblink ratio
            
            TODO Algoritmada ters yazilmis, fix edilecek. sag yerine sol, sol yerine sag geliyor.
        """
        if ratr > 55 and ratl < 29:
            self.TotalList.append('6')
        else:
            pass
        
        Password().getPassword(self.TotalList)

    #function for decision mouth
    def decisionMouth(self,ratm): #2 and #3
        """Make a decision the mouth position.
        and return smile or open mouth.
        
        Args:
            ratm (int): ratio of mouth position
        """
        if ratm > 34:
            self.TotalList.append('7')
        elif ratm < 15:
            self.TotalList.append('8')
        else:
            pass
        Password().getPassword(self.TotalList)

    #function for decision eyebrows
    def decisionEyebrows(self,ratebl,ratebr):#4
        """Make a decision eyebrows up or not

        Args:
            ratebl (int): _description_
            ratebr (int): _description_
        """
        if ratebl < 200 or ratebr < 200:
            #print("kaşşşş")
            self.TotalList.append('9')
        else:
            pass
        Password().getPassword(self.TotalList)

    #function for decision finger
    def calculateFinger(self, img, lmList):
        fingers = []
        tipId=[4,8,12,16,20]
        if(len(lmList)!=0):
            #thumb
            if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                    fingers.append(1)
            else :
                    fingers.append(0)
            #4 fingers
            for id in range(1,len(tipId)):
                
                if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                    fingers.append(1)
                else :
                    fingers.append(0)
                    
        self.decisionFingerMoves(img,fingers)

    #function for decision finger moves
    def decisionFingerMoves(self,img,arr):
        s=""
        for i in arr:
            s += str(arr[i])
        
        if(s=="00000"):
            Password().getPassword_Finger('0')
        elif(s=="01000"):
            Password().getPassword_Finger('1')
        elif(s=="01100"):
            Password().getPassword_Finger('2') 
        elif(s=="01110"):
            Password().getPassword_Finger('3')
        elif(s=="01111"):
            Password().getPassword_Finger('4')
        elif(s=="11111"):
            Password().getPassword_Finger('5')
