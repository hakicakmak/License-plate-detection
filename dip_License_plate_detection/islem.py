import fonksiyonlar as fonk
import cv2
import numpy as np
import pytesseract
from Ayarlamalar import OS
import matplotlib.pyplot as plt

def goruntu(resim_adresi):
    try:
        if resim_adresi:  # Seçilen dosya adı null değilsees
            img = fonk.resimAc(resim_adresi)  # Resim Açma İşlemi

            img_gray = fonk.griyecevir(img)  # griye cevirme fonk
            gurultuazalt = fonk.gurultuAzalt(img_gray)  # Gurultu azaltma fonksiyonu
            h_esitleme = fonk.histogramEsitleme(gurultuazalt)  # Histogram Eşitleme
            morfolojik_resim = fonk.morfolojikIslem(h_esitleme)  # Morfolojik islem
            goruntucikarma = fonk.goruntuCikarma(h_esitleme, morfolojik_resim)  # Goruntu Çıkarma İşlemi
            goruntuesikleme = fonk.goruntuEsikle(goruntucikarma)  # Goruntu Eşikleme İşlemi
            cannedge_goruntu = fonk.cannyEdge(goruntuesikleme)  # Canny_Edge İşlemi
            gen_goruntu = fonk.genisletmeIslemi(cannedge_goruntu)  # Dilated (Genişletme İşlemi)
            screenCnt = fonk.konturIslemi(img, gen_goruntu)  # Kontur İşlemi
            yeni_goruntu = fonk.maskelemeIslemi(img_gray, img, screenCnt)  # Maskeleme İşlemi
            fonk.plakaIyilestir(yeni_goruntu)  # Maskelenmiş görüntü üzerinde işlemler.

            img_plaka = fonk.plakaIyilestir(yeni_goruntu)
            text_plaka = pytesseract.image_to_string(img_plaka)
            print("Okunan Metin:", text_plaka)

            # İşlemlerin sonuçlarını tek bir sayfada göstermek için subplot kullanalım
            fig, axs = plt.subplots(2, 4, figsize=(16, 8))
            fig.suptitle(f"Plaka: {text_plaka}", fontsize=16, y=0.98)

            axs[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axs[0, 0].set_title('Orijinal Görüntü')

            axs[0, 1].imshow(img_gray, cmap='gray')
            axs[0, 1].set_title('Griye Çevrilen Görüntü')

            axs[0, 2].imshow(gurultuazalt, cmap='gray')
            axs[0, 2].set_title('Gürültü Azaltılmış Görüntü')

            axs[0, 3].imshow(h_esitleme, cmap='gray')
            axs[0, 3].set_title('Histogram Eşitleme')

            axs[1, 0].imshow(morfolojik_resim, cmap='gray')
            axs[1, 0].set_title('Morfolojik İşlem')

            axs[1, 1].imshow(goruntucikarma, cmap='gray')
            axs[1, 1].set_title('Görüntü Çıkarma')

            axs[1, 2].imshow(gen_goruntu, cmap='gray')
            axs[1, 2].set_title('Genişletme İşlemi')

            axs[1, 3].imshow(yeni_goruntu, cmap='gray')
            axs[1, 3].set_title('Maskeleme İşlemi')

            plt.show()
    

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except Exception as e:
        print("Bir hata oluştu:", str(e))

