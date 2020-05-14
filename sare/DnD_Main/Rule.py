# uncompyle6 version 3.6.5
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Steve\workspace\DnD_Add_Detail\src\sare\DnD_Main\Rule.py
# Compiled at: 2013-12-21 06:38:20
__doc__ = '\nCreated on Dec 17, 2013\n\n@author: Steve Sare\n'

class Rule(object):
    """Rule"""

    def __init__(self):
        """
        Constructor
        """
        pass

    def writeRules(self, output, ref, newChar):
        output.emit('Processing Rules...')
        root = newChar.getroot()
        charSheet = root.find('CharacterSheet')
        tally = charSheet.find('RulesElementTally')
        for rule in tally.iter('RulesElement'):
            self.writeRule(ref, rule)

        output.emit('Rules written')

    def writeRule(self, ref, ruleElement):
        charFile = CharacterFile()
        refroot = ref.getroot()
        for rule in refroot.iter('RulesElement'):
            if rule.get('internal-id') == ruleElement.get('internal-id'):
                for specific in ruleElement:
                    ruleElement.remove(specific)

                for flavor in rule.findall('Flavor'):
                    charFile.writeFlavor(flavor, ruleElement)

                index = 1
                for specificref in rule:
                    ruleElement.insert(index, specificref)
                    index = index + 1

                continue

from sare.DnD_Main.CharacterFile import CharacterFile
