'''
Created on 16.10.2016

@author: Tommi
'''

from datetime import datetime
import os, requests, bs4, sys, shutil

if __name__ == '__main__':
    
    ### Variables ###
    # DIRs
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGES_DIR = os.path.abspath(os.path.join(ROOT_DIR, os.pardir, os.pardir, 'images'))
    DUMP_DIR = None
   
    # Web
    url = ''
    headers = { 'Accept-Language':'en-US,en;q=0.5',
               'User-Agent':'Mozilla/5.0'
    }
    
    # Other
    imageCount = 0
    
    ### Functions ###
    def initialize():
        if not os.path.isdir(IMAGES_DIR):
            os.makedirs(IMAGES_DIR, 0o777, False)
            
        time = datetime.now()
        dumpDir = '%s-%s-%s' % (time.day, time.month, time.year)
        dumpDir = os.path.abspath(os.path.join(ROOT_DIR, os.pardir, os.pardir, 'images', dumpDir))
        if not os.path.isdir(dumpDir):
            os.makedirs(dumpDir, 0o777, False)
            
        return dumpDir
    
    def downloadImage(link, imageName, fileType='.jpg'):
        imagePath = DUMP_DIR + '/' + imageName + fileType
        if not os.path.isfile(imagePath):
            request = requests.get(link, stream = True, headers = headers) #stream!!!
            request.raise_for_status()#kaataa
            with open(imagePath, 'wb') as out_file:
                request.raw.decode_content = True
                shutil.copyfileobj(request.raw, out_file)
            out_file.close()
            del request
            return True
        else:
            #print('Oli jo')
            return False
    
    
    ### Execution ###
    # print(sys.path) #Jos haluaa katsella mistä moduuleja haetaan yms / for debugging..
    DUMP_DIR = initialize()
    
    res = requests.get(url, headers = headers)
    print(res.status_code)
    res.raise_for_status()  #Tähän kaatuu, jos kaatuu!
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    
    links = soup.select('figcaption > a')  # tajuaa, että nämä ovat tag-elementtejä
    for link in links:
        if '.jpg' in link.get('href'):
            print(link.get('href') + " // " + link.string) #testiprintti
            if downloadImage('https:' + link.get('href'), link.string, '.jpg') == True:
                imageCount += 1
        elif '.png' in link.get('href'):
            print(link.get('href') + " // " + link.string) #testiprintti
            if downloadImage('https:' + link.get('href'), link.string, '.png') == True:
                imageCount += 1
    del res
    print('\nImages downloaded: ' + str(imageCount))
