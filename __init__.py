# Copyright (c) 2017 Zoff
# https://github.com/zoff99/ElectricPrintCostCalculator

# Copyright (c) 2015 Jaime van Kessel
# PluginCostCalculator is released under the terms of the AGPLv3 or higher.

from . import ElectricPrintCostCalculator
from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("ElectricPrintCostCalculator")
def getMetaData():
    return {
        "type": "extension",
        "plugin": 
        {
            "name": "Electrical Print Cost Calculator",
            "author": "Zoff",
            "version": "0.99.0",
            "api": 3,
            "description": i18n_catalog.i18nc("Description of plugin","Extension to quickly calculate print costs")
        }
    }
        
def register(app):
    return { "extension": ElectricPrintCostCalculator.ElectricPrintCostCalculator()}
