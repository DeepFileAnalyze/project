# coding=utf-8
import os
import io

import pyocr
import pyocr.builders

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser.default import MultifieldParser

from wand.image import Image

from PIL import Image as PI


indexdir = "/home/kaese/git/project/out/index"
textsdir = "/home/kaese/git/project/out/texts"
searchdirs = []

class Helper:
    def mkdir_if_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    def add_to_searchdirs(self, path):
        searchdirs.append(path)


class OCR:
    def pdf_to_jpegs(self):
        req_image = []
        image_pdf = Image(filename=path, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')
        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))
        return req_image

    def jpegs_to_texts(self, req_image):
        h = Helper()
        h.mkdir_if_not_exist(textsdir)
        for img in req_image: 
            txt = tool.image_to_string(PI.open(io.BytesIO(img)), lang=lang, builder=pyocr.builders.TextBuilder())


class SampleSchema(SchemaClass):
    title = TEXT(stored=True)
    content = TEXT()
    keywords = KEYWORD(commas=True)


class Search:
    def create_index(self):
        h = Helper()
        h.mkdir_if_not_exist(indexdir)

        ix = create_in(indexdir, SampleSchema)
        
        writer = ix.writer()
        for directory in searchdirs:
            for filename in os.listdir(directory):
                with open(directory+"/" + filename,"r") as textfile:
                    writer.add_document(title=filename, keywords=directory, content=textfile.read())
        writer.commit()
    
    
    def search(self,str):
        ix = open_dir(indexdir)
    
        with ix.searcher() as searcher:
            parser = MultifieldParser(['keywords',
                                       'content',
                                       'title'], ix.schema)
            query = parser.parse(str)
    
            results = searcher.search(query)
    
            return [list(result.values()) for result in results]
    

if __name__ == '__main__':
    s = Search()
    s.create_index()

    print(s.search("penis"))
