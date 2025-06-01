from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom

with open("index.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

ATOM_NS = "http://www.w3.org/2005/Atom"
ET.register_namespace('', ATOM_NS)

feed = ET.Element(ET.QName(ATOM_NS, "feed"))

ET.SubElement(feed, ET.QName(ATOM_NS, "title")).text = "tbwcjw.online Feed"
ET.SubElement(feed, ET.QName(ATOM_NS, "link"), href="https://tbwcjw.online", rel="alternate")
ET.SubElement(feed, ET.QName(ATOM_NS, "link"), href="https://tbwcjw.online/atom_feed.xml", rel="self")
ET.SubElement(feed, ET.QName(ATOM_NS, "updated")).text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
ET.SubElement(feed, ET.QName(ATOM_NS, "id")).text = "https://tbwcjw.online/"

author = ET.SubElement(feed, ET.QName(ATOM_NS, "author"))
ET.SubElement(author, ET.QName(ATOM_NS, "name")).text = "tbwcjw"

project_items = soup.select("div.col-md-6 h2:-soup-contains('Software projects') ~ .list-group .list-group-item")

for item in project_items:
    title = item.h5.get_text(strip=True)
    desc = item.p.get_text(strip=True)
    link_tag = item.find("a", href=True)
    link = link_tag["href"] if link_tag else "https://tbwcjw.online#software-projects"
    
    entry = ET.SubElement(feed, ET.QName(ATOM_NS, "entry"))
    ET.SubElement(entry, ET.QName(ATOM_NS, "title")).text = title
    ET.SubElement(entry, ET.QName(ATOM_NS, "link"), href=link)
    ET.SubElement(entry, ET.QName(ATOM_NS, "id")).text = link
    ET.SubElement(entry, ET.QName(ATOM_NS, "summary")).text = desc
    
    author = ET.SubElement(entry, ET.QName(ATOM_NS, "author"))
    ET.SubElement(author, ET.QName(ATOM_NS, "name")).text = "tbwcjw"
    
    ET.SubElement(entry, ET.QName(ATOM_NS, "category"), term="Software Project")

notes = soup.select("h2:-soup-contains('Notes') + .list-group .list-group-item")
for note in notes:
    title = note.b.get_text(strip=True)
    desc = note.p.get_text(strip=True)
    date_text = note.find("small").text.strip()
    pub_date = datetime.strptime(date_text, "%m/%d/%y %I:%M %p").strftime("%Y-%m-%dT%H:%M:%SZ")
    
    entry = ET.SubElement(feed, ET.QName(ATOM_NS, "entry"))
    ET.SubElement(entry, ET.QName(ATOM_NS, "title")).text = title
    

    note_id = f"https://tbwcjw.online/#notes-{title.replace(' ', '-')}"
    ET.SubElement(entry, ET.QName(ATOM_NS, "link"), href=note_id)
    ET.SubElement(entry, ET.QName(ATOM_NS, "id")).text = note_id
    ET.SubElement(entry, ET.QName(ATOM_NS, "updated")).text = pub_date
    ET.SubElement(entry, ET.QName(ATOM_NS, "summary")).text = desc
    
    author = ET.SubElement(entry, ET.QName(ATOM_NS, "author"))
    ET.SubElement(author, ET.QName(ATOM_NS, "name")).text = "tbwcjw"
    
    ET.SubElement(entry, ET.QName(ATOM_NS, "category"), term="Note")

rough_string = ET.tostring(feed, 'utf-8')
reparsed = xml.dom.minidom.parseString(rough_string)
pretty_xml = reparsed.toprettyxml(indent="  ")

with open("atom.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
