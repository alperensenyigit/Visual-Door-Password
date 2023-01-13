import logging #logging library initialize
import pyautogui
import time

#global variables for password lists
finger_count = []
userList = [-1]

#logging configuration
logging.basicConfig(filename="logs.txt",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#password class
class Password():
    
    #constructor for password class
    def __init__(self):
        self.password=[-1]
        self.pwobject=open("password.txt","r")
        self.pwdump = self.pwobject.readline()
        sifre = self.pwdump.split(",")
        self.password = sifre
        self.psize= len(self.password)
    
    #method for get password fingers
    def getPassword_Finger(self, arr): #GENERATE PASSWORD FOR HAND GESTURES
            
        finger_count.append(arr)
        #print("fC:",finger_count)
        if len(userList)-1 != self.psize:
            
            if finger_count.count('0') == 10:
                if (userList[-1] != '0'):
                    userList.append('0')
                    finger_count.clear()
                
            if finger_count.count('1') == 10:
                if (userList[-1] != '1'):
                    userList.append('1')
                    finger_count.clear()
                    
            if finger_count.count('2') == 10:
                if (userList[-1] != '2'):
                    userList.append('2')
                    finger_count.clear()
                    
            if finger_count.count('3') == 10:
                if (userList[-1] != '3'):
                    userList.append('3')
                    finger_count.clear()
                    
            if finger_count.count('4') == 10:        
                if (userList[-1] != '4'):
                    userList.append('4')
                    finger_count.clear()
                    
            if finger_count.count('5') == 10:        
                if (userList[-1] != '5'):
                    userList.append('5')
                    finger_count.clear()
                
            self.check_password(userList) 

    #method for get password mimics       
    def getPassword(self,sifre): # GENERATE PASSWORD FOR MIMICS
        if len(userList)-1 != self.psize:
        
            if sifre.count('6') == 150:
                if (userList[-1] != '6'):
                    userList.append('6')
                    sifre.clear()
                    
            if sifre.count('7') == 150:        
                if (userList[-1] != '7'):
                    userList.append('7')
                    sifre.clear()
                    
            if sifre.count('8') == 150:
                
                if (userList[-1] != '8'):
                    userList.append('8')
                    sifre.clear()
                    
            if sifre.count('9') == 150:
                if (userList[-1] != '9'):
                    userList.append('9')
                    sifre.clear()
            
            self.check_password(userList)   
                   
    #method for check password   
    def check_password(self,SIFRE):

        if (SIFRE[1:] == self.password):
            global userList
            userList = [-1]
            logger.info("Access Granted...")
            f= open("checkpw.txt","w")
            f.write("1")
            f.close()
       
        else:
            #print("ELSE",SIFRE)
            if(SIFRE[1:] != self.password and len(SIFRE) - 1 == self.psize):
                userList = [-1]
                logger.warning("Access Denied...")
                ss_img = pyautogui.screenshot()
                filename = 'FailedAccess '+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
                ss_img.save(filename, "png")
                f= open("checkpw.txt","w")
                f.write("0")
                f.close()