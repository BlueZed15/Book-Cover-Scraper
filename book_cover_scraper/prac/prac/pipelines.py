from itemadapter import ItemAdapter
import cv2
import os
import requests
import numpy as np


class PracPipeline:
    def process_item(self, item, spider):
        book_adapter=ItemAdapter(item)

        #removing leading and trailing spaces of book titles
        title=book_adapter.get('book_title')
        book_adapter['book_title']=title.strip()

        #retrieving and saving images
        path=''
        raw_img=requests.get(book_adapter.get('cover_url')).content
        array_img=np.frombuffer(raw_img,np.uint8)
        image=cv2.imdecode(array_img,cv2.IMREAD_COLOR)

        if not os.path.exists(os.path.join(path,'book_covers')):
            os.mkdir(os.path.join(path,'book_covers'))

        if path=='':
            cv2.imwrite(os.path.join('book_covers',book_adapter.get('book_title')+'.png'),image)
        else:
            cv2.imwrite(os.path.join(path+'\\book_covers', book_adapter.get('book_title') + '.png'), image)



        return item

class PG_Pipeline:
    def process_item(self,item,spider):
        cover=ItemAdapter(item)

        # retrieving and saving images
        path = ''
        raw_img = requests.get(cover.get('cover_url')).content
        array_img = np.frombuffer(raw_img, np.uint8)
        image = cv2.imdecode(array_img, cv2.IMREAD_COLOR)

        if not os.path.exists(os.path.join(path, 'book_covers')):
            os.mkdir(os.path.join(path, 'book_covers'))
        print('\nyeepee')
        if path == '':
            cv2.imwrite(os.path.join('book_covers', cover.get('id') + '.png'), image)
        else:
            cv2.imwrite(os.path.join(path + '\\book_covers', cover.get('id') + '.png'), image)

        return item

