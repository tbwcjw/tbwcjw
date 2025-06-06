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

def create_entry(title, desc, link, category, updated=None):
    entry = ET.SubElement(feed, ET.QName(ATOM_NS, "entry"))
    ET.SubElement(entry, ET.QName(ATOM_NS, "title")).text = title
    ET.SubElement(entry, ET.QName(ATOM_NS, "link"), href=link)
    ET.SubElement(entry, ET.QName(ATOM_NS, "id")).text = link
    if updated:
        ET.SubElement(entry, ET.QName(ATOM_NS, "updated")).text = updated
    ET.SubElement(entry, ET.QName(ATOM_NS, "summary")).text = desc

    entry_author = ET.SubElement(entry, ET.QName(ATOM_NS, "author"))
    ET.SubElement(entry_author, ET.QName(ATOM_NS, "name")).text = "tbwcjw"

    ET.SubElement(entry, ET.QName(ATOM_NS, "category"), term=category)

# software projects
software_heading = soup.find("h2", string=lambda s: s and "Software projects" in s)
if software_heading:
    software_list = software_heading.find_next_sibling("div", class_="list-group")
    if software_list:
        for item in software_list.select(".list-group-item"):
            title = item.h5.get_text(strip=True)
            desc = item.p.get_text(strip=True)
            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else "https://tbwcjw.online#software-projects"
            create_entry(title, desc, link, "Software Project")

# just For Fun projects
jff_heading = soup.find("h2", string=lambda s: s and "Just For Fun projects" in s)
if jff_heading:
    jff_list = jff_heading.find_next_sibling("div", class_="list-group")
    if jff_list:
        for item in jff_list.select(".list-group-item"):
            title = item.h5.get_text(strip=True)
            desc = item.p.get_text(strip=True)
            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else "https://tbwcjw.online#jff-projects"
            create_entry(title, desc, link, "Just For Fun Project")

# notes
notes_heading = soup.find("h2", string=lambda s: s and "Notes" in s)
if notes_heading:
    notes_list = notes_heading.find_next_sibling("div", class_="list-group")
    if notes_list:
        for note in notes_list.select(".list-group-item"):
            title = note.b.get_text(strip=True)
            desc = note.p.get_text(strip=True)
            date_text = note.find("small").text.strip()
            pub_date = datetime.strptime(date_text, "%m/%d/%y %I:%M %p").strftime("%Y-%m-%dT%H:%M:%SZ")
            note_id = f"https://tbwcjw.online/#notes-{title.replace(' ', '-')}"
            create_entry(title, desc, note_id, "Note", updated=pub_date)

# prettify
rough_string = ET.tostring(feed, 'utf-8')
reparsed = xml.dom.minidom.parseString(rough_string)
pretty_xml = reparsed.toprettyxml(indent="  ")

with open("atom.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
