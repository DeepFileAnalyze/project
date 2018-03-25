# coding=utf-8
import os
import io

import textract
from PyPDF2 import PdfFileWriter, PdfFileReader
#import pyocr
#import pyocr.builders

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser.default import MultifieldParser

#from wand.image import Image

#from PIL import Image as PI


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
    def build_searchdirs_from_existing(self, direc):
        for directory in os.listdir(direc):
            path = textsdir + "/" + directory
            if os.path.isdir(path):
                self.add_to_searchdirs(path)
    def clear_searchdirs(self):
        searchdirs = []

class OCR:
    def pdfs_to_texts(self, path):
        h = Helper()
        pdfnames = os.listdir(path)
        for filename in pdfnames:
            full = path + "/" + filename
            if not os.path.isdir(full):
                pdfReader= PdfFileReader(open(full, 'rb'))
                full += "_seperate"
                h.mkdir_if_not_exist(full)
                h.mkdir_if_not_exist(textsdir + "/" + filename)
                for i in range(pdfReader.numPages):
                    output = PdfFileWriter()
                    output.addPage(pdfReader.getPage(i))
                    with open(full + "/" + str(i) + ".pdf", "wb") as outputStream:
                        output.write(outputStream)
                    text = textract.process(full + "/" + str(i) + ".pdf")
                    textpath = textsdir + "/" + filename  + "/" + str(i)
                    h.write_to(text.decode("utf-8"), textpath)
                    h.add_to_searchdirs(textsdir + "/" + filename)

#    def pdfs_to_texts(self, path):
#        req_images = []
#        h = Helper()
#        h.mkdir_if_not_exist(path)
#        pdfnames = os.listdir(path)
#        for filename in pdfnames:
#            req_images.append(self.pdf_to_jpegs(path + "/" + filename))
#        for i, images in enumerate(req_images):
#            self.jpegs_to_texts(images, pdfnames[i])
#
#    def pdf_to_jpegs(self, path):
#        req_image = []
#        image_pdf = Image(filename=path, resolution=300)
#        image_jpeg = image_pdf.convert('jpeg')
#        for img in image_jpeg.sequence:
#            img_page = Image(image=img)
#            req_image.append(img_page.make_blob('jpeg'))
#        return req_image
#
#    def jpegs_to_texts(self, req_image, pdfname):
#        h = Helper()
#        h.mkdir_if_not_exist(textsdir + "/" + pdfname)
#        tool = pyocr.get_available_tools()[0]
#        lang = tool.get_available_languages()[0]
#        for i, img in enumerate(req_image): 
#            txt = tool.image_to_string(PI.open(io.BytesIO(img)), lang=lang, builder=pyocr.builders.TextBuilder())
#            path = textsdir + "/" + pdfname  + "/" + str(i)
#            h.write_to(txt, path)
#            h.add_to_searchdirs(textsdir + "/" + pdfname)

class SampleSchema(SchemaClass):
    title = TEXT(stored=True)
    content = TEXT()
    keywords = KEYWORD(commas=True)


class Search:
    def create_index(self, direc):
        h = Helper()
        h.mkdir_if_not_exist(direc)

        ix = create_in(direc, SampleSchema)
        
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
    
class ExampleClass:
    def hackathonexample(self):
        o = OCR()
        o.pdfs_to_texts(pdfsdir)
    #    h = Helper()
    #    h.build_searchdirs_from_existing(textsdir)
        s = Search()
        s.create_index(indexdir)
        liste = s.search("Satz")
        direc = textsdir + "/vorlesung-t3.pdf"
    #    h = Helper()
    #    h.mkdir_if_not_exist("/tmp/tmpindex")
    #    h.clear_searchdirs()
    #    h.build_searchdirs_from_existing(direc)
    #    s.create_index("/tmp/tmpindex")
    #    lt = s.search("Satz")
    #    a = lt+l
    #    dupes = [x for n, x in enumerate(a) if x in a[:n]]
        al = []
        for i in range(len(liste)):
            with open(direc + "/" + liste[i][0]) as f:
                text = f.read()
            al.append(text)
        return al

if __name__ == '__main__':
    e = ExampleClass()
    print(e.hackathonexample())
