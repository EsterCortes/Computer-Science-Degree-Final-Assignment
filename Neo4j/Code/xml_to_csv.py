
import xml.etree.ElementTree as ET
import pandas as pd
from collections import OrderedDict

parser = ET.XMLParser(encoding='ISO-8859-1')

parser.entity["agrave"] = 'à'
parser.entity["uuml"] = 'ü'
parser.entity["Eacute"] = 'É'
parser.entity["eacute"] = 'é'
parser.entity["aacute"] = 'á'
parser.entity["iacute"] = 'í'
parser.entity["ouml"] = 'ö'
parser.entity["ccedil"] = 'ç'
parser.entity["egrave"] = 'è'
parser.entity["auml"] = 'ä'
parser.entity["uacute"] = 'ú'
parser.entity["aring"] = 'å'
parser.entity["oacute"] = 'ó'
parser.entity["szlig"] = 'ß'
parser.entity["oslash"] = 'ø'
parser.entity["yacute"] = 'ỳ'
parser.entity["iuml"] = 'ï'
parser.entity["igrave"] = 'í'
parser.entity["ocirc"] = 'ô'
parser.entity["icirc"] = 'î'
parser.entity["Uuml"] = 'Ü'
parser.entity["euml"] = 'ë'
parser.entity["acirc"] = 'â'
parser.entity["atilde"] = 'ã'
parser.entity["Uacute"] = 'Ù'
parser.entity["Aacute"] = 'À'
parser.entity["ntilde"] = 'ñ'
parser.entity["Auml"] = 'Ä'
parser.entity["Oslash"] = 'Ø'
parser.entity["Ccedil"] = 'Ç'
parser.entity["otilde"] = 'õ'
parser.entity["ecirc"] = 'ê'
parser.entity["times"] = '×'
parser.entity["Ouml"] = 'Ö'
parser.entity["reg"] = '®'
parser.entity["Aring"] = 'Å'
parser.entity["Oacute"] = 'Ò'
parser.entity["ograve"] = 'ó'
parser.entity["yuml"] = 'ÿ'
parser.entity["eth"] = 'ð'
parser.entity["aelig"] = 'æ'
parser.entity["AElig"] = 'Æ'
parser.entity["Agrave"] = 'Á'
parser.entity["Iuml"] = 'Ï'
parser.entity["micro"] = 'µ'
parser.entity["Acirc"] = 'Â'
parser.entity["Otilde"] = 'Õ'
parser.entity["Egrave"] = 'É'
parser.entity["ETH"] = 'Ð'
parser.entity["ugrave"] = 'ú'
parser.entity["ucirc"] = 'û'
parser.entity["thorn"] = 'þ'
parser.entity["THORN"] = 'Þ'
parser.entity["Iacute"] = 'Ì'
parser.entity["Icirc"] = 'Î'
parser.entity["Ntilde"] = 'Ñ'
parser.entity["Ecirc"] = 'Ê'
parser.entity["Ocirc"] = 'Ô'
parser.entity["Ograve"] = 'Ó'
parser.entity["Igrave"] = 'Í'
parser.entity["Atilde"] = 'Ã'
parser.entity["Yacute"] = 'Ỳ'
parser.entity["Ucirc"] = 'Û'
parser.entity["Euml"] = 'Ë'

tree = ET.parse("dblp.xml",parser=parser)
root = tree.getroot()

publication_types = ["article","inproceedings","incollection"]

authors_dict = OrderedDict()
authors_dict["authorId:ID(Authors)"] = []
authors_dict["name"] = []
authors_dict[":LABEL"] = []

publications_dict = OrderedDict()
publications_dict["publicationId:ID(Publications)"] = []
publications_dict["title"] = []
publications_dict["type"] = []
publications_dict["year"] = []
publications_dict[":LABEL"] = []

relationshipsPA_dict = OrderedDict()
relationshipsPA_dict[":START_ID(Publications)"] = []
relationshipsPA_dict[":END_ID(Authors)"] = []
relationshipsPA_dict[":TYPE"] = []

authorId = 1
publicationId = 1

aux_authors_dict = OrderedDict()

for child in root:
    if child.tag in publication_types:
        author_rel_list = []
        year = None
        for elem in child:
            if elem.tag == "title":
                publications_dict["publicationId:ID(Publications)"].append(publicationId)
                myId = publicationId
                publicationId +=1
                publications_dict["title"].append(elem.text)
                publications_dict[":LABEL"].append("Publication")
                publications_dict["type"].append(child.tag)
            elif elem.tag == "author":
                if elem.text not in aux_authors_dict:
                    authors_dict["authorId:ID(Authors)"].append(authorId)
                    aux_authors_dict[elem.text] = authorId
                    authorId += 1
                    authors_dict["name"].append(elem.text)
                    authors_dict[":LABEL"].append("Author")
                author_rel_list.append(aux_authors_dict[elem.text])
            elif elem.tag == "year":
                publications_dict["year"].append(int(elem.text))
                year = elem.text
        if year == None:
            publications_dict["year"].append(0)
        for author in range(len(author_rel_list)):
            relationshipsPA_dict[":START_ID(Publications)"].append(myId)
            relationshipsPA_dict[":END_ID(Authors)"].append(author_rel_list[author])
            relationshipsPA_dict[":TYPE"].append("Has_Author")

authors = pd.DataFrame(authors_dict)
publications = pd.DataFrame(publications_dict)
PA_relationships = pd.DataFrame(relationshipsPA_dict)

authors.to_csv("authors.csv", index=False)
publications.to_csv("documents.csv", index=False)
PA_relationships.to_csv("PA_relationships.csv", index=False)