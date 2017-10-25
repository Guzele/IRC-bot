import urllib
import cv2


direc = '1'

def downloadImage(url, imageName):
     try:
       urllib.urlretrieve(url, direc + '/'+ imageName)
       return True   
     except Exception as e :
       return False


def transformImage(img):
    height, width, channels = img.shape
    height, width = decreaseSize (height, width)
    
    img = cv2.resize(img,(width, height))
    #cv2.imshow("Buildings",img)
    #cv2.waitKey(0)

    pixelSize = 8

    H = height / pixelSize;
    W =  width / pixelSize;

    r = []
    for h in range (0, H):
        res = ''
        for w in range (0, W):
            res += getSymbol(img, w, h, pixelSize);
        r.append(res)
    return r

def showImage(imageName):
    img = cv2.imread(direc + '/'+ imageName)
    #cv2.imshow("Buildings",img)
    #cv2.waitKey(0)
    return transformImage(img)

patternSchale = " .:-=+*#%@"


def averageBrigtness3 (img, x, y):
   a, b, c = img [y, x]
   return int(a) + int(b) + int(c)


def averageBrigtnessOfBlock (img, w, h, pixelsize):
    sum = 0
    w1 = w * pixelsize
    w2 = w1 + pixelsize;

    h1 = h * pixelsize;
    h2 = h1 + pixelsize;

    for  i in range (w1, w2):
        for j in range (h1, h2):
            sum += averageBrigtness3 (img, i, j);
    return sum / 3 / pixelsize / pixelsize

def getSymbol(img, w, h, pixelsize):
    br = averageBrigtnessOfBlock(img, w, h, pixelsize);
    num = br * 10 / 256 ;
    return patternSchale[num];

def decreaseSize (height, width):
    while width > 400 or height > 400:
        width /= 2
        height /= 2
    return (height, width)


#downloadImage("http://www.drodd.com/images15/nature21.jpg", direc + '/'+"00000001.jpg")
#"http://www.drodd.com/images15/nature21.jpg"

#showImage( "2.jpg")
