"""Zander / Magister (2011), *Full of Grace: Crowned Madonnas from the Vatican Basilica* — catalogue rows.

Pietro Zander (ed.), research and texts Sara Magister, *Full of Grace: Crowned Madonnas from the
Vatican Basilica*, exhibition catalogue, Knights of Columbus Museum, New Haven, 8 May 2011 – 15
January 2012 (Italian ed. *Piene di grazia. Madonne coronate dalla Basilica Vaticana*). The PDF is
published by the Knights of Columbus Italy (kofc.it). Its 89 numbered entries describe the painted
copies of crowned images kept by the Fabbrica di San Pietro, and each entry's "Sources and
bibliography" cites the Chapter's dossier for the coronation — BAV, ACSP, Madonne Coronate, vol.,
cc. — and often the Fabbrica's own *catalogo delle immagini* (AFSP, Arm. 12, F, 11, nr. 10).
Seven further images in the Vatican Basilica itself are treated in an essay (pp. 24-36).

Input : data/zander-magister-2011-extraction.json — the entry headers and sources blocks parsed
        from the PDF text layer (title, location line, "Crowned ..." line, sources block, dates),
        checked by hand against the printed entries. The ACSP and AFSP citations are re-parsed
        here from the sources block, cut at the end of the folio list.
Output: data/zander-magister-2011-catalogue.json

The locality/church/country for each entry is set here by hand from the location line, so that the
locality matches the catalogue's spelling where the image is already present.
"""
import json,pathlib
REPO=pathlib.Path(__file__).resolve().parent.parent
E={e['no']:e for e in json.load(open(REPO/'data/zander-magister-2011-extraction.json',encoding='utf-8'))}
I='Italy'
# no: (locality, church_or_sanctuary, country, subject or None, notes or None)
L={
 1:("Valperga (Sacro Monte di Belmonte)","Sacro Monte di Belmonte",I,None,None),
 2:("Alessandria","Cattedrale di San Pietro",I,None,None),
 3:("Varallo (Sacro Monte)","Basilica dell'Assunta, Sacro Monte di Varallo",I,None,None),
 4:("Villanova Mondovì","Chiesa della Madonna del Pasco",I,None,None),
 5:("Gavi (Valle)","Santuario di Nostra Signora delle Grazie della Valle",I,None,None),
 6:("Novi Ligure","Collegiata di Santa Maria Maggiore",I,None,"Day and month not given in the catalogue ('[?] 1905')."),
 7:("Orta San Giulio","San Nicolao",I,None,None),
 8:("Caraglio","Santuario della Madonna del Castello",I,None,None),
 9:("Cicagna","Santuario di Nostra Signora dei Miracoli",I,None,"Crowned 14 September 1790 and again 14 September 1814."),
 10:("San Bartolomeo al Mare","Santuario di Nostra Signora della Rovere",I,None,None),
 11:("Mallare (Eremita)","Santuario di Nostra Signora della Misericordia all'Eremita",I,None,None),
 12:("Arenzano","Santuario di Nostra Signora Annunziata delle Olivette",I,None,"Catalogue: 'Crowned in 1890 or 1891'."),
 13:("Genoa (Oregina)","Santuario di Nostra Signora di Loreto in Oregina",I,None,None),
 14:("Genoa (Cremeno)","San Pietro Apostolo, Cremeno",I,None,None),
 15:("Genoa (Carbonara)","Santuario della Madonnetta (N. S. Assunta di Carbonara)",I,None,None),
 16:("Cremona","Sant'Abbondio (Beata Vergine Lauretana)",I,None,None),
 17:("Gallivaggio (Valle Spluga), diocese of Como","Santuario dell'Apparizione di Maria Vergine",I,None,None),
 18:("Casalpusterlengo","Santissima Maria Madre del Salvatore (Madonna dei Cappuccini)",I,None,None),
 19:("Ardesio","Santuario della Madonna delle Grazie",I,None,None),
 20:("Castelleone","Santuario della Beata Vergine della Misericordia",I,None,None),
 21:("Stezzano","Santuario della Madonna dei Campi",I,None,None),
 22:("Vall'Alta di Albino","Santuario della Beata Vergine di Altino",I,None,None),
 23:("Albino","Santuario della Madonna del Pianto",I,None,None),
 24:("Montagnaga di Piné","Santuario della Madonna di Piné",I,None,None),
 25:("Grado (Isola di Barbana)","Santuario di Barbana",I,None,None),
 26:("Bettola","Santuario della Beata Vergine della Quercia",I,None,None),
 27:("Macerata","San Giorgio",I,None,"No archival citation in the catalogue entry."),
 28:("Senigallia","San Martino",I,None,None),
 29:("Lucca","Sant'Agostino (Madonna del Sasso)",I,None,None),
 30:("Montepulciano","Santa Maria delle Grazie",I,None,None),
 31:("Monticello Amiata","Santuario della Madonna di Val di Prata",I,None,None),
 32:("Lucca (San Tommaso in Pelleria)","San Tommaso in Pelleria",I,None,None),
 33:("Viareggio","Sant'Andrea Apostolo",I,None,None),
 34:("Narni","Santuario di Santa Maria del Ponte",I,None,None),
 35:("Acquapendente","Sant'Agostino (Madonna delle Grazie)",I,None,None),
 36:("Nettuno","Santuario di Nostra Signora delle Grazie e di Santa Maria Goretti",I,None,None),
 37:("Cava de' Tirreni","Basilica di Maria Santissima Incoronata dell'Olmo",I,None,None),
 38:("Napoli (Santa Restituta)","Basilica di Santa Restituta, cappella di Santa Maria del Principio",I,None,None),
 39:("Napoli (Donnaregina)","Santa Maria di Donnaregina",I,None,None),
 40:("Napoli (Ponticelli)","Santuario di Maria Santissima della Neve",I,None,None),
 41:("Napoli (Annunziata Maggiore)","Basilica dell'Annunziata Maggiore",I,None,None),
 42:("Piano di Sorrento","Basilica della Santissima Trinità",I,None,None),
 43:("Massa Lubrense","Santuario di Santa Maria della Lobra",I,None,None),
 44:("Castellammare di Stabia (Pozzano)","Santa Maria di Pozzano",I,None,None),
 45:("Castellammare di Stabia (Portosalvo)","Santa Maria di Portosalvo",I,None,None),
 46:("Castellammare di Stabia (Quisisana)","Santuario di Santa Maria della Sanità",I,None,None),
 47:("Sorrento","Santa Maria del Carmine",I,None,None),
 48:("Sessa Aurunca","Cattedrale dei Santi Pietro e Paolo",I,None,None),
 49:("Casal di Principe","Santissimo Salvatore",I,None,None),
 50:("Sant'Agnello di Sorrento (Angri)","Santuario di Santa Maria Annunziata",I,None,None),
 51:("Eboli","Collegiata di Santa Maria della Pietà",I,None,None),
 52:("Viggiano","Santa Maria del Monte / Santa Maria alle Mura (del Deposito)",I,None,None),
 53:("Otranto","Cattedrale (Vergine Annunziata)",I,None,None),
 54:("Capurso","Basilica di Santa Maria del Pozzo",I,None,None),
 55:("Bovino","Santa Maria di Valleverde e San Lorenzo",I,None,None),
 56:("Laterza","Santuario diocesano di Maria Santissima Mater Domini",I,None,None),
 57:("Dipignano (Laurignano)","Santuario della Madonna della Catena",I,None,None),
 58:("Cagliari (Calaris)","Santuario di Nostra Signora di Bonaria",I,None,"No archival citation in the catalogue entry."),
 59:("Cuglieri","Basilica di Santa Maria della Neve",I,None,None),
 60:("Sassari","San Pietro in Silki",I,None,None),
 61:("Sindia","Abbazia di Nostra Signora di Corte (Cabuabbas)",I,None,"No archival citation in the catalogue entry. Crowned 4 September 1948 and again 4 September 1998."),
 62:("Palermo (Sant'Antonio di Padova)","Oratorio del monastero di Sant'Antonio di Padova",I,None,None),
 63:("Montserrat","Monestir de Montserrat",'Spain',None,None),
 64:("Oñati (Oñate)","Santuario de Nuestra Señora de Aránzazu",'Spain',None,None),
 65:("Bilbao","Basílica de Begoña",'Spain',None,None),
 66:("Lugo","Catedral de Santa María (Ojos Grandes)",'Spain',None,None),
 67:("Reus","Santuari de la Mare de Déu de Misericòrdia",'Spain',None,None),
 68:("Teror (Gran Canaria)","Basílica de Nuestra Señora del Pino",'Spain',None,None),
 69:("Ponferrada","Basílica de Nuestra Señora de la Encina",'Spain',None,None),
 70:("Andújar","Santuario de Nuestra Señora de la Cabeza",'Spain',None,None),
 71:("Orihuela","Santuario de Nuestra Señora de Monserrate",'Spain',None,None),
 72:("Palma de Mallorca","Sant Miquel",'Spain',None,"No ACSP citation: the entry cites the Palma diocesan archive."),
 73:("Douvres-la-Délivrande","Basilique Notre-Dame de la Délivrande",'France',None,None),
 74:("Périgueux","Couvent de Sainte-Ursule",'France',None,None),
 75:("Vion","Basilique Notre-Dame du Chêne",'France',None,"No archival citation in the catalogue entry."),
 76:("Bar-le-Duc","Saint-Pierre et Saint-Étienne",'France',None,None),
 77:("Hasselt","Basiliek Virga Jesse",'Belgium',None,None),
 78:("Huy","Notre-Dame de la Sarte",'Belgium',None,"Day and month not given in the catalogue ('[?] 1900')."),
 79:("Arlon","Saint-Donat",'Belgium',None,None),
 80:("Cologne (Köln)","Sankt Maria in der Kupfergasse",'Germany',None,"No archival citation in the catalogue entry."),
 81:("Miedniewice","Church of the Visitation (Reformed Franciscans)",'Poland',"Holy Family",
     "No ACSP citation; the entry cites the Fabbrica's catalogo delle immagini and the copy's inscription, which dates the Chapter's decree 8 July 1764."),
 82:("Kraków (Na Piasku)","Church of the Visitation 'in Arenis' (Carmelites, Na Piasku)",'Poland',None,None),
 83:("Svatá Hora, Příbram","Svatá Hora",'Czech Republic',None,None),
 84:("Chełm","Cathedral of the Nativity of the Virgin",'Poland',None,"Catalogue: 'Crowned on September 15, 1765 or September 17, 1767'. Chełm is today in Poland; the catalogue files it under Lutsk (Łuck), the diocese."),
 85:("Valletta","Shrine of Our Lady of Mount Carmel",'Malta',None,None),
 86:("Istanbul","Santa Maria Draperis",'Turkey',None,None),
 87:("El Valle del Espíritu Santo (Isla Margarita)","Basílica menor de Nuestra Señora del Valle",'Venezuela',None,None),
 88:("Lima","Basílica de Nuestra Señora de la Merced",'Peru',None,None),
 89:("Aparecida","Santuário Nacional de Nossa Senhora Aparecida",'Brazil',None,None),
}
# Chełm: keep the earlier alternative as the date, note the other
DATE_OVERRIDE={84:['1765-09-15'],12:['1890'],9:['1790-09-14','1814-09-14'],61:['1948-09-04','1998-09-04']}

import re
FOLIOS=re.compile(r'^(\d+(?: \(\d\))?), (cc?\.\s*\d[0-9rv\-–, ]*\d[rv]?)')
def acsp_refs(sources):
    """Every 'BAV, ACSP, Madonne Coronate, Vol. N, cc. ...' in the sources block, cut at the end of the
    folio list: the bibliography that follows it in the printed entry is not part of the citation."""
    out=[]
    for m in re.finditer(r'BAV, ACSP, Madonne Coronate, Vol\. (.*?)(?=BAV, ACSP|AFSP,|$)',sources or ''):
        f=FOLIOS.match(m.group(1).strip())
        if f: out.append(f"{f.group(1)}, {f.group(2).strip()}")
    return out
def afsp_refs(sources):
    """The Fabbrica's catalogo delle immagini, cited as 'AFSP, Arm. 12, F, 11, nr. 10' (once 'no. 10')."""
    return [m.group(1).strip() for m in re.finditer(
        r'AFSP, Arm\. 12, F, 11, n[ro]\. 10, catalogo delle immagini, (cc?\.\s*[IVXLC]+[rv]?(?:,\s*[IVXLC]+[rv]?)*)',sources or '')]
rows=[]
for n in sorted(E):
    e=E[n]; loc,church,country,subject,notes=L[n]
    dates=DATE_OVERRIDE.get(n,e['dates'])
    rows.append({'no':n,'page':e['page'],'title':e['title'].strip(),'location_as_given':e['location'],
      'crowned_as_given':e['crowned'],'coronation_dates':dates,
      'locality':loc,'church_or_sanctuary':church,'country':country,
      'subject':subject or 'Blessed Virgin Mary',
      'refs':acsp_refs(e['sources']),'afsp_refs':afsp_refs(e['sources']),'sources_as_given':e['sources'],'notes':notes})

# The seven images in the Vatican Basilica itself (essay, pp. 24-36)
VAT=[
 ('V1',25,"Madonna della Febbre","Rome, Vatican Basilica (sacristy)","Sagrestia Vaticana, Cappella dei Beneficiati",['1631-08-27'],[],
  "First image crowned by the Chapter; the essay gives the day (27 August 1631) but no folio."),
 ('V2',26,"Madonna della Pietà (Michelangelo's Pietà)","Rome, Vatican Basilica (Pietà)","Basilica Vaticana",['1637-08-31'],
  ['1, c. 69r','1, c. 4r'],"Crowned 31 August 1637 while still in the seventeenth-century Choir Chapel; crown donated by Count Sforza and consigned to Canon Ugo Ubaldini for the crowning (BAV, ACSP, Madonne Coronate, vol. 1, c. 4r); listed among the thirteen crowns granted in Sforza's lifetime (vol. 1, c. LXIXr)."),
 ('V3',28,"Madonna del Soccorso","Rome, Vatican Basilica (Cappella Gregoriana)","Cappella Gregoriana, Basilica Vaticana",['1643-11-17'],[],None),
 ('V4',30,"Madonna della Colonna (Mater Ecclesiae)","Rome, Vatican Basilica (Madonna della Colonna)","Cappella della Madonna della Colonna, Basilica Vaticana",['1645-01-01'],[],None),
 ('V5',32,"Madonna Immacolata","Rome, Vatican Basilica (Cappella del Coro)","Cappella del Coro, Basilica Vaticana",['1854-12-08'],[],
  "Crowned by Pius IX on the day of the definition of the Immaculate Conception."),
 ('V6',34,"Madonna Regina degli Apostoli","Rome, Vatican Grottoes (Regina Apostolorum)","Grotte Vaticane",['1950-11-04'],[],None),
 ('V7',35,"Nostra Signora di Częstochowa (copy)","Rome, Vatican Grottoes (Chapel of the Polish Nation)","Grotte Vaticane, cappella della Nazione Polacca",['2005-04-02'],[],
  "Copy of the Jasna Góra image in the Vatican Grottoes, crowned 2 April 2005 — the day of John Paul II's death."),
]
for no,pg,title,loc,church,dates,refs,notes in VAT:
    rows.append({'no':no,'page':pg,'title':title,'location_as_given':None,'crowned_as_given':None,'coronation_dates':dates,
      'locality':loc,'church_or_sanctuary':church,'country':I,'subject':'Blessed Virgin Mary','refs':refs,'afsp_refs':[],
      'sources_as_given':None,'notes':notes})

out={'source':("Pietro Zander (ed.), research and texts Sara Magister, Full of Grace: Crowned Madonnas from the Vatican Basilica, "
  "exhibition catalogue, Knights of Columbus Museum, New Haven, 8 May 2011 - 15 January 2012 (Italian ed.: Piene di grazia. "
  "Madonne coronate dalla Basilica Vaticana). 89 catalogue entries (pp. 46-229) on the painted copies of crowned images kept "
  "by the Fabbrica di San Pietro, each with the coronation date and the Chapter dossier cited as BAV, ACSP, Madonne Coronate, "
  "vol., cc.; plus seven images in the Vatican Basilica itself (pp. 24-36)."),
 'pdf':'https://www.kofc.it/pdf/E-Book-Full_of_Grace_Crowend_Madonnas_from_the_Vatican_Basilica/ (Knights of Columbus Italy e-book; the flipbook source is the PDF)',
 'note':("SECONDARY: reported by the catalogue, not read here. `refs` are its citations of BAV, ACSP, Madonne Coronate "
  "(volume, cc. = carte, the stamped foliation); `afsp_refs` its citations of the Fabbrica's catalogo delle immagini "
  "(AFSP, Arm. 12, F, 11, nr. 10). `coronation_dates` holds every date the entry gives ('and again ...' = a re-crowning). "
  "Rows without a folio are `low`."),
 'work':'Zander/Magister 2011','row_count':len(rows),'rows':rows}
json.dump(out,open(REPO/'data/zander-magister-2011-catalogue.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('rows',len(rows),'with ACSP refs',sum(1 for r in rows if r['refs']))
