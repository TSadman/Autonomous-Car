import cv2
from PIL import Image
import numpy as np
from tensorflow import keras

acc_thresh = 0.75
model = keras.models.load_model('model_keras')

imgWidth= 32         # CAMERA RESOLUTION
imgHeight = 32
brightness = 180
threshold = 0.75         # PROBABLITY THRESHOLD
font = cv2.FONT_HERSHEY_SIMPLEX

def most_frequent(List):
    return max(set(List), key = List.count)

def takeFourth(elem):
  return elem[4]

def make_square(im, fill_color=(0, 0, 0, 0)):
    x= im.shape[0]
    y= im.shape[1]
    #print(im.shape)
    size = max(x, y)
    new_im = np.zeros((size,size,3), np.uint8)
    #print(type(im))
    if x>y:
        new_im[:,:-(x-y),:]=im
    elif x<y:
        new_im[:-(-x+y),:,:]=im
    else:
        new_im = im
    return new_im

def grayscale(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img
def equalize(img):
    img =cv2.equalizeHist(img)
    return img
def preprocessing(img):
    img = grayscale(img)
    img = equalize(img)
    img=img/255
    return img
def getCalssName(classNo):
    if   classNo == 0: return 'Speed Limit 30 km/h'
    elif classNo == 1: return 'Speed Limit 50 km/h'
    elif classNo == 2: return 'Speed Limit 60 km/h'
    elif classNo == 3: return 'Speed Limit 70 km/h'
    elif classNo == 4: return 'Speed Limit 80 km/h'
    elif classNo == 5: return 'Speed Limit 100 km/h'
    elif classNo == 6: return 'Speed Limit 120 km/h'
    elif classNo == 7: return 'No passing'
    elif classNo == 8: return 'Right-of-way at the next intersection'
    elif classNo == 9: return 'Priority road'
    elif classNo == 10: return 'Yield'
    elif classNo == 11: return 'Stop'
    elif classNo == 12: return 'Keep right'
    else: return "nothing"

#img=cv2.imread('/content/drive/MyDrive/Colab Notebooks/Signal/stop.jpg')
#cv2_imshow(img)
#cv2.waitKey(0)

cap=cv2.VideoCapture(0)
cap.set(3,200)
cap.set(4,200)
cap.set(5,10)

n=1
y_range=[]
ynew=np.array([])
prob=0

while True:
    success, image = cap.read()
    #image=cv2.resize(img, (112,96))

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    edged=cv2.Canny(gray,30,200)
    #cv2_imshow(edged)
    #cv2.waitKey(0)

    image2=edged.copy()

    #use a copy of your image, e.g. - edged.copy(), since finding contours alter the image
    #we have to add _, before the contours as an empty argument due to upgrade of the OpenCV version
    contours, hierarchy=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cv2_imshow(edged)
    #cv2.waitKey(0)

    #print(hierarchy)
    #print('Numbers of contours found=' + str(len(contours)))

    ###reorganizes conture list from largest to smallest
    cont_list=[]

    for ii in range(len(contours)):
      cnt = contours[ii]
      x, y, w, h = cv2.boundingRect(cnt)
      cont_list.append([x,y,w,h,w*h])

    cont_list.sort(key = takeFourth, reverse = True)
    #print(cont_list)
    #print(cont_list)


    #######x-reference conture list with model
    #cv2_imshow(image)
    for cnt in cont_list:
        #print(cnt)
        x, y, w, h, _ = cnt
        #print(x, y, w, h)
        if (w>100 or h>100) or (w<32 or h<32):
            continue
        #print(x, y, w, h)

        img1 = image[x:x+w,y:y+h]
        if w!=h:
            img1 = make_square(img1)


        try:
            img=img1
            img =np.asarray(img)
            img=cv2.resize(img, (32,32))
            cv2.imshow("countured images", img)
        except:
            continue


        #print(img)
        #print(type(image))
        #cv2_imshow(img1)
        #im = make_square(img)

        img=preprocessing(img)
        img = img.reshape(1, imgHeight, imgWidth, 1)
        ynew= model.predict_classes(img)
        ynew=ynew.tolist()
        yprob = model.predict_proba(img)
        probability = yprob[0][ynew[0]]
        #print(probability)
        if probability >= acc_thresh:
            prob+=probability
            #print(ynew, probability)
            break

    if len(ynew) == 0:
        continue
    #print(ynew, probability)
    y_range.append(ynew[0])
    #print(ynew,probability)
    n+=1
    if n % 10 == 0:
        #print(y_range)
        ynew = [most_frequent(y_range)]
        if prob/10 < acc_thresh:
            ynew=['Nothing']

        print(" Predicted=",  getCalssName(ynew[0]), "Accuracy: ", prob/10)
        y_range=[]
        prob=0
    cv2.imshow("image", image)
    cv2.waitKey(1)
