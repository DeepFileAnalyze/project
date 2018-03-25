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
pdfsdir = "/home/kaese/git/project/out/pdfs"
searchdirs = []

class Helper:
    def mkdir_if_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    def add_to_searchdirs(self, path):
        if path not in searchdirs:
            searchdirs.append(path)
    def write_to(self, string, path):
        f = open(path, 'w+')
        f.write(string)
        f.close()
    def build_searchdirs_from_existing(self):
        for directory in os.listdir(textsdir):
            path = textsdir + "/" + directory
            if os.path.isdir(path):
                self.add_to_searchdirs(path)


class OCR:
    def pdfs_to_texts(self, path):
        req_images = []
        h = Helper()
        h.mkdir_if_not_exist(path)
        pdfnames = os.listdir(path)
        for filename in pdfnames:
            req_images.append(self.pdf_to_jpegs(path + "/" + filename))
        for i, images in enumerate(req_images):
            self.jpegs_to_texts(images, pdfnames[i])

    def pdf_to_jpegs(self, path):
        req_image = []
        image_pdf = Image(filename=path, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')
        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))
        return req_image

    def jpegs_to_texts(self, req_image, pdfname):
        h = Helper()
        h.mkdir_if_not_exist(textsdir + "/" + pdfname)
        tool = pyocr.get_available_tools()[0]
        lang = tool.get_available_languages()[0]
        for i, img in enumerate(req_image): 
            txt = tool.image_to_string(PI.open(io.BytesIO(img)), lang=lang, builder=pyocr.builders.TextBuilder())
            path = textsdir + "/" + pdfname  + "/" + str(i)
            h.write_to(txt, path)
            h.add_to_searchdirs(textsdir + "/" + pdfname)

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
#    o = OCR()
#    o.pdfs_to_texts(pdfsdir)
    h = Helper()
    h.build_searchdirs_from_existing()
    print(searchdirs)
    s = Search()
    s.create_index()

    print(s.search("Routing"))
