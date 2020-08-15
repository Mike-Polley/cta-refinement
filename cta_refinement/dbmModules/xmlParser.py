from xml.dom import minidom

class xmlParser:

    def __init__(self,doc):
        try:
            self.doc = minidom.parse(doc)
        except:
            return "Failed to open document"

    def get_init(self):
        self.initRef = self.doc.getElementsByTagName('init')
        self.init = self.initRef[0].attributes['ref'].value
        return self.init

    def get_cta_name(self):
        self.cta_name = self.doc.getElementsByTagName("name")[0].firstChild.nodeValue
        return self.cta_name

    def get_sources(self):
        self.sources = []
        doc_sources = self.doc.getElementsByTagName("source")
        for i in range(len(doc_sources)):
            self.sources.append(doc_sources[i].attributes["ref"].value)
        return self.sources

    def get_targets(self):
        self.targets = []
        doc_targets = self.doc.getElementsByTagName("target")
        for i in range(len(doc_targets)):
            self.targets.append(doc_targets[i].attributes["ref"].value)
        return self.targets

    def get_synchronisations(self):
        self.synchronisations = []
        doc_labels = self.doc.getElementsByTagName("label")
        for i in range(len(doc_labels)):
            if doc_labels[i].attributes["kind"].value == "synchronisation":
                self.synchronisations.append(doc_labels[i].firstChild.nodeValue)
            else:
                pass
        return self.synchronisations

    def gen_cta(self):
        self.cta = ''
        cta_builder = []
        cta_builder.append(("Cta " + self.get_cta_name() + 
        " = {Init " + self.get_init() + ";"))
        sources = self.get_sources()
        synchronisations = self.get_synchronisations()
        targets = self.get_targets()
        for i in range(len(synchronisations)):
            cta_builder.append(sources[i] + " ")
            cta_builder.append(synchronisations[i] + " ")
            cta_builder.append(targets[i] +";")
        cta_builder.append("};")
        return self.cta.join(cta_builder)


if __name__ == "__main__":
    parse = xmlParser('2doors.xml')
    print(parse.get_sources())
    print(parse.get_synchronisations())
    print(parse.get_targets())
    print(parse.gen_cta())
