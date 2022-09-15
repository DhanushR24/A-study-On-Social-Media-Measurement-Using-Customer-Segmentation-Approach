from urllib import request
import PyPDF2
import io
import re

def getPDFContent(URL : str) -> tuple[float, float, float, float]:
    req               = request.Request(URL, headers={'User-Agent' : "Magic Browser"})
    remote_file       = request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote     = PyPDF2.PdfFileReader(remote_file_bytes)

    numberOfPages = pdfdoc_remote.getNumPages()

    for i in range(numberOfPages):
        try:
            page        = pdfdoc_remote.getPage(i)
            pageContent = re.sub(r" +", " ", page.extractText())

            DAP = float(re.search(r"DAP was (\d+|\d+\.\d+) billion", pageContent).group(1))
            MAP = float(re.search(r"MAP was (\d+|\d+\.\d+) billion", pageContent).group(1))
            DAU = float(re.search(r"DAUs were (\d+|\d+\.\d+) billion", pageContent).group(1))
            MAU = float(re.search(r"MAUs were (\d+|\d+\.\d+) billion", pageContent).group(1))
            
            return DAP, MAP, DAU, MAU
        except:
            try:
                DAU = float(re.search(r"DAUs were (\d+|\d+\.\d+) billion", pageContent).group(1))
                MAU = float(re.search(r"MAUs were (\d+|\d+\.\d+) billion", pageContent).group(1))
                return 0, 0, DAU, MAU
            except:
                continue
