#!/usr/bin/env python3
import json, os, urllib.parse, urllib.request
TOKEN=os.environ.get("ADS_TOKEN")
AUTHOR_QUERY=os.environ.get("ADS_AUTHOR_QUERY", "author:\"Blaña, Matias\" OR author:\"Blaña, M\"")
N=int(os.environ.get("ADS_N","6"))
if not TOKEN: raise SystemExit("Missing ADS_TOKEN secret.")
params={"q":AUTHOR_QUERY,"fl":"bibcode,title,author,pubdate,year,doi","sort":"date desc","rows":str(N)}
url="https://api.adsabs.harvard.edu/v1/search/query?"+urllib.parse.urlencode(params)
req=urllib.request.Request(url,headers={"Authorization":f"Bearer {TOKEN}"})
with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
papers=[]
for doc in data.get("response",{}).get("docs",[])[:N]:
    title=doc.get("title",["Untitled"])[0] if isinstance(doc.get("title"),list) else doc.get("title","Untitled")
    authors=doc.get("author",[])
    author_str="; ".join(authors[:4])+("; et al." if len(authors)>4 else "")
    bib=doc.get("bibcode","")
    papers.append({"year":str(doc.get("year") or (doc.get("pubdate","")[:4] if doc.get("pubdate") else "")),"title":title,"authors":author_str,"bibcode":bib,"url":f"https://ui.adsabs.harvard.edu/abs/{bib}/abstract" if bib else "https://ui.adsabs.harvard.edu/"})
open("latest-papers.json","w",encoding="utf-8").write(json.dumps(papers,ensure_ascii=False,indent=2)+"\n")
