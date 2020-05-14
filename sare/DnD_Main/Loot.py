# uncompyle6 version 3.6.5
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Steve\workspace\DnD_Add_Detail\src\sare\DnD_Main\Loot.py
# Compiled at: 2013-12-21 06:38:22
__doc__ = '\nCreated on Dec 17, 2013\n\n@author: Steve Sare\n'

class Loot(object):
    """Loot"""

    def __init__(self):
        """
        Constructor
        """
        pass

    def writeLoots(self, output, ref, newChar):
        output.emit('Processing L00t...')
        root = newChar.getroot()
        for loot in root.iter('loot'):
            self.writeLoot(ref, loot)

        output.emit('L00t written')

    def writeLoot(self, ref, loot):
        rule = Rule()
        for loot in loot.iter('RulesElement'):
            rule.writeRule(ref, loot)

from sare.DnD_Main.Rule import Rule
