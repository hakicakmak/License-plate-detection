import cv2
# Opencv Kütüphanesini Projeme Dahil ediyorum.
import numpy as np
#Numpy kütühanesi dahil etme işlemi // Maskeleme işlemlerinde kullanılacak

def resimAc(sec):
    # Dosyadan resim okumak için dosyamın yolunu seciyoruz.
    img = cv2.imread("Resim/" + sec)

    return img

# RGB uzayından Gri seviyeli resme dönüş işlemi
def griyecevir(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    return img_gray

#2. Gauss Filtreleme , Medyan ortalama ile aynı işi yapan fonk.
## gürültü azaltıcı yumuşatma işlemi
#Her pikselin yoğunluğunu, yakındaki piksellerin yoğunluk ortalamasının ağırlıklı ortalaması ile değiştirir
#Diğer üç filtre kenarları pürüzsüz hale getirirken sesleri kaldırır, ancak bu filtre, kenar #koruyarak görüntünün gürültüyü azaltabilir. 

def gurultuAzalt(img_gray):
    gurultuazalt = cv2.bilateralFilter(img_gray, 9, 75, 75)
    return  gurultuazalt

# Daha iyi sonuç elde etmek için histogram eşitleme işlemi yapıyoruz
def histogramEsitleme(gurultuazalt):
    histogram_e = cv2.equalizeHist(gurultuazalt)
    return histogram_e


# Açma İşlemi(Opening):
#Aşındırma ile küçük parçalar yok edildikten sonra dilation ile görüntü tekrar genişletilerek küçük parçaların kaybolması sağlanır.
#gürültülerin etkisi azaltılır.
def morfolojikIslem(h_esitleme):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morfolojikresim = cv2.morphologyEx(h_esitleme, cv2.MORPH_OPEN, kernel, iterations=15)
    return  morfolojikresim


#Resim üzerinde düzensiz bölümleri dengelemek.
# veya iki resim arasındaki değişiklikleri saptamak için görüntü çıkarma kullanılır.(Image subtraction).

def goruntuCikarma(h_esitleme,morfolojik_resim):
    # Görüntü çıkarma (Morph görüntüsünü histogram eşitlenmiş görüntüsünden çıkarmak)
    gcikarilmisresim = cv2.subtract(h_esitleme, morfolojik_resim)
    return gcikarilmisresim



#   görüntüdeki her pikseli siyah bir piksel ile değiştirir; Formul var ona göre yapıyor
# görüntü yoğunluğu bu sabitten büyükse beyaz bir piksel

def goruntuEsikle(goruntucikarma):
    ret, goruntuesikle = cv2.threshold(goruntucikarma, 0, 255, cv2.THRESH_OTSU)
    return goruntuesikle


#Görüntünün kenarlarını algılamak için canny edge kullandım

def cannyEdge(goruntuesikleme):
    canny_goruntu = cv2.Canny(goruntuesikleme, 250, 255)
    canny_goruntu = cv2.convertScaleAbs(canny_goruntu)
    return canny_goruntu


#Dilatasyon operatörü, girdi olarak iki veri alanını alır.
# Birincisi dilate edilecek olan resimdir. İkincisi, yapılandırma unsuru cekirdek
#Dilate, Büyümek, Genişletmek

def genisletmeIslemi(cannedge_goruntu):
    # Kenarları güçlendirmek için genleşme
    cekirdek = np.ones((3, 3), np.uint8)
    # Genişletme için çekirdek oluşturma
    gen_goruntu = cv2.dilate(cannedge_goruntu, cekirdek, iterations=1)
    return gen_goruntu


def konturIslemi(img,gen_goruntu):
    # Kenarlara dayanan resimdeki Konturları Bulma
    contours, hierarchy = cv2.findContours(gen_goruntu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    # Rakamları alana göre sıralama, böylece sayı plakası ilk 10 konturda olacak
    screenCnt = None
    # kontur dng işlemi
    for c in contours:
        # yaklaşık çizgi belirliyoruz
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # % 6 hata ile yaklaşıklık
        # Yaklaşık konturuzun dört noktası varsa, o zaman
        # ----Plakamızı yaklaşık olarak bulduğumuzu varsayabiliriz.

        if len(approx) == 4:  # Konturu 4 köşeli olarak seçiyoruz
            screenCnt = approx
            break
    	
    final = cv2.drawContours(img, [screenCnt],-1, (9, 236, 255), 3)  # KARENİN RENGİ VE ÇİZİMİ
    # Seçilen konturun orijinal resimde çizilmesi
    return  screenCnt

##Belirnenen alan dışında kalan yerleri maskeleme
def maskelemeIslemi(img_gray,img,screenCnt):
    # Numara plakası dışındaki kısmı maskeleme
    mask = np.zeros(img_gray.shape, np.uint8)
    yeni_goruntu = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    yeni_goruntu = cv2.bitwise_and(img, img, mask=mask)
    return yeni_goruntu

def plakaIyilestir(yeni_goruntu):
    # Daha fazla işlem için numara plakasını geliştirmek için histogram eşitleme
    y, cr, cb = cv2.split(cv2.cvtColor(yeni_goruntu, cv2.COLOR_RGB2YCrCb))
    # Görüntüyü YCrCb modeline dönüştürme ve 3 kanalı bölme
    y = cv2.equalizeHist(y)
    # Histogram eşitleme uygulama
    son_resim = cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2RGB)
    # 3 kanalı birleştirme
    #cv2.namedWindow("Gelismis_plaka_no", cv2.WINDOW_NORMAL)
    #cv2.imshow("Gelismis_plaka_no", son_resim)
    return son_resim
