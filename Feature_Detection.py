import cv2
from matplotlib import pyplot as plt

'''
依照特徵點比對
'''

class Feature_Detection():

    def __init__(self):
        pass

    '''
    For BF matcher, first we have to create the BFMatcher object using cv2.BFMatcher(). 
    It takes two optional params. First one is normType. 
    It specifies the distance measurement to be used. 
    By default, it is cv2.NORM_L2. It is good for SIFT, SURF etc (cv2.NORM_L1 is also there). 
    For binary string based descriptors like ORB, BRIEF, BRISK etc, cv2.NORM_HAMMING should be used, 
    which used Hamming distance as measurement. If ORB is using VTA_K == 3 or 4, cv2.NORM_HAMMING2 should be used.
    
    Second param is boolean variable, crossCheck which is false by default. 
    If it is true, Matcher returns only those matches with value (i,j) 
    such that i-th descriptor in set A has j-th descriptor in set B as the best match and vice-versa. 
    That is, the two features in both sets should match each other. 
    It provides consistant result, and is a good alternative to ratio test proposed by D.Lowe in SIFT paper.
    '''

    '''
    DMatch.distance - Distance between descriptors. The lower, the better it is.
    DMatch.trainIdx - Index of the descriptor in train descriptors
    DMatch.queryIdx - Index of the descriptor in query descriptors
    DMatch.imgIdx - Index of the train image.
    '''
    #ORB 暴力尋找法
    def ORB_Brute_Matching(self,Query_Image,Train_Image):
        Query_Image=cv2.imread(Query_Image,0)
        Train_Image=cv2.imread(Train_Image,0)
        ORB=cv2.ORB()
        kp1,des1=ORB.detectAndCompute(Query_Image,None)
        kp2,des2=ORB.detectAndCompute(Train_Image,None)
        BFMatch = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
        Matchers=BFMatch.match(des1,des2)
        Matchers=sorted(Matchers,key= lambda x:x.distance)
        # Draw first 10 matches.
        img3 = cv2.drawMatches(Query_Image, kp1, Train_Image, kp2, Matchers[:10], flags=2)
        plt.imshow(img3), plt.show()

    #比對圖片相似度
    def Similarity(self,Image_1,Image_2):
        try:
            #讀圖
            img1 = cv2.imread(Image_1, 0)
            img2 = cv2.imread(Image_2, 0)

            # ORB檢測器
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)

            # 特徵點
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)

            # knn塞選
            matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

            '''
            匹配點數目
            比值測試消除異常點，小於閾值時（0.75）才被認為是匹配，
            因為假設匹配是一一對應的，真正的匹配的理想距離為0
            '''
            good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
            print(len(good))
            print(len(matches))
            similary = len(good) / len(matches)
            print("相似度:%s" % similary)
            return similary

        except:
            print('無法計算相似度')


