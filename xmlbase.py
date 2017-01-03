# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ElementTree
import logging
import os.path



# KONSTANTEN---------------------
XML_KEY                 = "KEY"
XML_VALUE               = "VALUE"
#-------------------------------

class CXmlBaseReader():
    """Diese Klasse stellt Basisdienste für das Lesen von XML Dateien
    zur Verfügung"""
    def __init__(self, pXmlFile):
        self._XmlFile = pXmlFile

    def readXMLelement (self, pXMLelement):
        """ Liefert den Wert eines einzelnen XML Tags zurück, es wird vorausgesetzt dass der übergebene Tag ein Attribute
            mit der Bezeichung "typ" besitzt welches die Werte "str und "int" annehmen kann"""
        # Dictionary zur Typkonvertierung
        typen = {"int" : int, "str" : str}
        #Den Wert des Tag Attributes "typ" als String auslesen, zulässige Werte sind hier "str" oder "int" 
        typ = pXMLelement.get("typ", "str")
        try:
            value =  typen [typ](pXMLelement.text)
            return value
        except KeyError:
            pXMLelement.text    

    def readXmlBaseEntry (self, pXmlBaseEntry):
        """ Diese Methode liest XML Element auf der obersten Ebene ein. Hier wird unterstellt das diese Elemente auschließlich
            aus Paaren Attribut/Wert bestehen. Diese werden in ein Dictionary gelesen und dieses wird zurück geliefert.
            Wenn komplexere XML Strukturen eingelesen werden, muss diese Methode überschrieben werden"""        
        dDict = {}
        #alle Einträge 
        for xmlTag in pXmlBaseEntry:
            tagKey   = xmlTag.find(XML_KEY)
            tagValue = xmlTag.find(XML_VALUE)
            # Einträge im Dictionary bestehen aus Paaren Schlüssel / Wert....
            dDict [self.readXMLelement (tagKey)] = self.readXMLelement (tagValue)
        return dDict
        

    def readXmlFile (self):
        """ Lies die XML Daten in eine Liste ein. Wenn abgeleitete Klassen die entsprechenden Methoden nicht überschrieben
            haben ist jedes Listenelement ein Dictionary, welche Paare Attribut/Wert enthält"""
        logging.info ("Lese XML Datei " + self._XmlFile)
        listOfDict = []
        #Prüfen ob die Datei existiert
        if not os.path.exists (self._XmlFile):
            raise FileNotFoundError
        # XML Datei in Baumstruktur einlesen
        tree = ElementTree.parse (self._XmlFile)
        rootDict = tree.getroot()
        for xmlBaseEntry in rootDict:
        #für baseEntry wurde bewußt kein Typ festgelegt, da der Typ abhängig von der Struktur der zu leseneden XML Datei ist
        # im einfachsten Fall ist das ein Dictionary, sonst können das wiederum Listen sein.     
            baseEntry = self.readXmlBaseEntry (xmlBaseEntry)        
            listOfDict.append(baseEntry)    
        return listOfDict
            
            
        
