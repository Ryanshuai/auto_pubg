
import xml.etree.ElementTree as ElementTree


class XmlListConfig(list):
    def __init__(self, aList):
        super().__init__()
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):

    def __init__(self, parent_element):
        super().__init__()
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


def xml_2_dict(path):
    tree = ElementTree.parse(path)
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    return xmldict


def xml_2_xywh(path):
    xmldict = xml_2_dict(path)
    # relative_path = xmldict['folder']
    xmax = int(xmldict['object']['bndbox']['xmax'])
    xmin = int(xmldict['object']['bndbox']['xmin'])
    ymax = int(xmldict['object']['bndbox']['ymax'])
    ymin = int(xmldict['object']['bndbox']['ymin'])
    x, y, w, h = xmin, ymin, xmax-xmin, ymax-ymin
    return x, y, w, h


if __name__ == '__main__':
    xmldict = xml_2_dict('000000.xml')
    print(0)
