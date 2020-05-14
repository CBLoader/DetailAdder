# uncompyle6 version 3.6.5
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Steve\workspace\DnD_Add_Detail\src\sare\DnD_Main\Power.py
# Compiled at: 2013-12-21 06:38:22
__doc__ = '\nCreated on Dec 17, 2013\n\n@author: Steve Sare\n'

class Power(object):
    """Power"""

    def __init__(self):
        """
        Constructor
        """
        pass

    def writePowers(self, output, ref, newChar):
        output.emit('Processing Powers...')
        root = newChar.getroot()
        for power in root.iter('Power'):
            self.writePower(ref, power)

        output.emit('Powers written')

    def writePower(self, ref, power):
        from sare.DnD_Main.CharacterFile import CharacterFile
        charFile = CharacterFile()
        refroot = ref.getroot()
        for rule in refroot.iter('RulesElement'):
            if rule.get('name') == power.get('name') and rule.get('type') == 'Power':
                for specific in power.findall('specific'):
                    power.remove(specific)

                for flavor in rule.findall('Flavor'):
                    charFile.writeFlavor(flavor, power)

                index = 1
                for specificref in rule.findall('specific'):
                    power.insert(index, specificref)
                    index = index + 1

                continue
