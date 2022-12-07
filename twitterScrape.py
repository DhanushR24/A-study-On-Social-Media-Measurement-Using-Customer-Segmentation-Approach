from urllib import request
import PyPDF2
import io
import re

import pandas as pd

URLs = ["https://s22.q4cdn.com/826641620/files/doc_financials/2018/q4/Q4-2018-Selected-Company-Financials-and-Metrics.pdf",
        "https://s22.q4cdn.com/826641620/files/doc_financials/2021/q4/Final-Q4'21-Selected-Metrics-and-Financials.pdf"]


def getQuarterlyDataCSV(URLs):
    quarterlyData = {
        "quarter": [],
        "DAU": []
    }

    for URL in URLs:
        req = request.Request(URL, headers={'User-Agent': "Magic Browser"})
        remote_file = request.urlopen(req).read()
        remote_file_bytes = io.BytesIO(remote_file)
        pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes)

        page = pdfdoc_remote.getPage(0)

        titlesRow = re.findall(r"Financials(?:\(.*\))?.+?Company",
                               str(page.extractText()))[0]

        titlesCleaned = re.sub(r"Financials(\(.*\))?", "",
                               str(titlesRow))

        titles = list()

        for i in range(0, len(titlesCleaned), 5):
            quarter = titlesCleaned[i:i+5]

            if 'Q' not in quarter:
                break

            titles.append(quarter)

        row = re.search(r"Worldwide[^Q]*", page.extractText()).group(0)
        rowCleaned = re.sub(r"\(\d+\)", "", str(row))
        numbers = str(re.sub(r"Worldwide", "", str(rowCleaned)))

        quarter = list()
        for i in range(0, len(titles)):

            quarter.append(numbers[i*3:i*3+3])

        quarterlyData["quarter"].extend(titles)
        quarterlyData["DAU"].extend(quarter)

    df = pd.DataFrame(quarterlyData, columns=quarterlyData)
    df.to_csv("Tw.csv", index=False)

    print(df)


getQuarterlyDataCSV(URLs)
