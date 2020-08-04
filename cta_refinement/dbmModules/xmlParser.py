from xml.dom import minidom


doc = minidom.parse('simpleCta.xml')
initRef = doc.getElementsByTagName('init')
init = initRef[0].attributes['ref'].value

locations = doc.getElementsByTagName("location")

for i in range(len(locations)):
    if locations[i].attributes["id"].value == init:
        firstLocation = locations[i]
    else:
        pass

locationName = firstLocation.getElementsByTagName("name")
name = locationName[0].firstChild.nodeValue

source = doc.getElementsByTagName("source")
sources = []
for i in range(len(source)):
    sources.append(source[i].attributes["ref"].value)

target = doc.getElementsByTagName("target")
targets = []
for i in range(len(target)):
    targets.append(target[i].attributes["ref"].value)

print("Cta simpleCta = {Init " + init + "; \n" + init + " UM!" + name + " " + targets[0] + ";};")