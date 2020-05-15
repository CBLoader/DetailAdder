# uncompyle6 version 3.6.5
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Steve\workspace\DnD_Add_Detail\src\sare\DnD_Main\CharacterFile.py
# Compiled at: 2014-01-10 02:44:47
__doc__ = '\nCreated on Dec 6, 2013\n\n@author: Steve Sare\n'
import os

class CharacterFile(object):

    def __init__(self):
        """
        Constructor
        """
        pass

    def mainExists(self):
        import os.path
        fname = self.getCBLoaderMain()
        return os.path.isfile(fname)

    def getCBLoaderMain(self):
        if not os.path.exists('app.cfg'):
            with open('app.cfg', 'w') as f:
                f.write("""#Note: CBLoader 1.3.x and earlier used "combined.dnd40"
mainFile.Location=%appdata%\CBLoader\Cache\combined.dnd40.merged.xml""")
        config = open('app.cfg', 'r')
        contents = config.readline()
        while not contents.startswith('mainFile.Location'):
            contents = config.readline()

        valuePointer = contents.index('=')
        fname = contents[valuePointer + 1:len(contents)].strip()
        config.close()
        fname = os.path.expandvars(fname)
        return fname

    def process(self, fname, output):
        import codecs
        from sare.DnD_Main.Power import Power
        from sare.DnD_Main.Loot import Loot
        from sare.DnD_Main.Rule import Rule
        import xml.etree.ElementTree as ET
        output.emit('Processing file: ' + fname)
        output.emit('Loading character and reference files...')
        referenceFileName = self.getCBLoaderMain()
        oldChar = codecs.open(fname, 'r', 'utf-8-sig')
        charString = oldChar.read()
        oldChar.close()
        newCharRoot = ET.fromstring(charString)
        newChar = ET.ElementTree(newCharRoot)
        mainfile = codecs.open(referenceFileName, 'r', 'utf-8-sig')
        mainString = mainfile.read()
        refRoot = ET.fromstring(mainString)
        ref = ET.ElementTree(refRoot)
        rule = Rule()
        loot = Loot()
        power = Power()
        rule.writeRules(output, ref, newChar)
        loot.writeLoots(output, ref, newChar)
        power.writePowers(output, ref, newChar)
        newfile = fname[0:len(fname) - 6] + 'Detail.dnd4e'
        newChar.write(newfile, encoding='UTF-8-sig', xml_declaration=False)

    def writeFlavor(self, flavor, parent):
        import xml.etree.ElementTree as ET
        newFlavor = ET.Element('specific', dict([('name', 'Flavor')]))
        newFlavor.text = flavor.text
        parent.insert(0, newFlavor)
