# Copyright (c) 2017 Zoff
# https://github.com/zoff99/ElectricPrintCostCalculator

# Copyright (c) 2015 Jaime van Kessel
# PluginCostCalculator is released under the terms of the AGPLv3 or higher.

from PyQt5.QtCore import  QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
from UM.Extension import Extension
from UM.PluginRegistry import PluginRegistry
import os.path
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlComponent, QQmlContext
from UM.Application import Application
from UM.Preferences import Preferences

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("ElectricPrintCostCalculator")


class ElectricPrintCostCalculator(QObject,  Extension):
    def __init__(self, parent = None):
        super().__init__(parent)
        # Python has a very agressive garbage collector, so we need to keep a reference of the qtcomponent.
        self._cost_view = None 
       
        self.addMenuItem(i18n_catalog.i18n("Calculate"), self.showPopup)

        self._engine_created = False
        # We need to listen for active machine changed, as this might change the material _material_diameter
        Application.getInstance().engineCreatedSignal.connect(self._onEngineCreated)
        # Application.getInstance().getMachineManager().activeMachineInstanceChanged.connect(self._onActiveMachineChanged)

        self._print_information = None
        self._material_diameter = 1.75
        
        # This adds the preferences if they aren't already there with default values. 
        # if they already exist (not the first time this plugin runs, the saved value is used)
        Preferences.getInstance().addPreference("electric_print_cost_calculator/price_per_kg", "30")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/density", "1240")

        Preferences.getInstance().addPreference("electric_print_cost_calculator/price_kwh_cent", "25")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/power_consumtion_printer_watt", "200")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/printer_cost", "400")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/printer_lasting_hours", "1000")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/printing_time_h", "2")
        Preferences.getInstance().addPreference("electric_print_cost_calculator/printing_time_m", "0")
        
        # Load the values again (so the values are read from file if not first run).
        # We do need to force them to float, else the display can give errors.
        self._price_per_kg = float(Preferences.getInstance().getValue("electric_print_cost_calculator/price_per_kg"))
        self._density = float(Preferences.getInstance().getValue("electric_print_cost_calculator/density"))

        self._price_kwh_cent = float(Preferences.getInstance().getValue("electric_print_cost_calculator/price_kwh_cent"))
        self._power_consumtion_printer_watt = float(Preferences.getInstance().getValue("electric_print_cost_calculator/power_consumtion_printer_watt"))
        self._printer_cost = float(Preferences.getInstance().getValue("electric_print_cost_calculator/printer_cost"))
        self._printer_lasting_hours = float(Preferences.getInstance().getValue("electric_print_cost_calculator/printer_lasting_hours"))
        self._printing_time_h = float(Preferences.getInstance().getValue("electric_print_cost_calculator/printing_time_h"))
        self._printing_time_m = float(Preferences.getInstance().getValue("electric_print_cost_calculator/printing_time_m"))


    # Events to notify the qml 
    materialAmountChanged = pyqtSignal()
    materialDiameterChanged = pyqtSignal()
    densityChanged = pyqtSignal()
    pricePerKgChanged = pyqtSignal()
    PricePKWHChanged = pyqtSignal()
    PowerConsumpChanged = pyqtSignal()
    PrinterCostChanged = pyqtSignal()
    PrinterLastingHoursChanged = pyqtSignal()
    PrintingTimeHChanged = pyqtSignal()
    PrintingTimeMChanged = pyqtSignal()
    
    def _onEngineCreated(self):
        self._engine_created = True
        self._onActiveMachineChanged()

    ##  Private function to sit in between uranium signal and pyqt signal.
    def _onMaterialDiameterChanged(self, value):
        self._material_diameter = value 
        self.materialDiameterChanged.emit()

    def _onActiveMachineChanged(self):
        if self._engine_created:
            self._print_information = Application.getInstance().getPrintInformation()
    
    @pyqtProperty(float, notify = materialDiameterChanged)
    def materialDiameter(self):
        return self._material_diameter
    
    @pyqtProperty(float, notify = pricePerKgChanged)
    def pricePerKg(self):
        return self._price_per_kg
    
    @pyqtProperty(float, notify = densityChanged)
    def density(self):
        return self._density



    @pyqtProperty(float, notify = PricePKWHChanged)
    def price_kwh_cent(self):
        return self._price_kwh_cent

    @pyqtProperty(float, notify = PowerConsumpChanged)
    def power_consumtion_printer_watt(self):
        return self._power_consumtion_printer_watt

    @pyqtProperty(float, notify = PrinterCostChanged)
    def printer_cost(self):
        return self._printer_cost

    @pyqtProperty(float)
    def material_cost(self):
        materialcost = Application.getInstance().getPrintInformation().materialCosts
        cost_sum = 0
        for i in materialcost:
            cost_sum = (float)(cost_sum) + (float)(i)
        return (float)(cost_sum)


    @pyqtProperty(float, notify = PrinterLastingHoursChanged)
    def printer_lasting_hours(self):
        return self._printer_lasting_hours


    @pyqtProperty(float, notify = PrintingTimeHChanged)
    def printing_time_h(self):
        # return self._printing_time_h
        _printtime_ = Application.getInstance().getPrintInformation().currentPrintTime
        return (_printtime_.hours + (_printtime_.days * 24.0) * 1.0)

    @pyqtProperty(float, notify = PrintingTimeMChanged)
    def printing_time_m(self):
        # return self._printing_time_m
        _printtime_ = Application.getInstance().getPrintInformation().currentPrintTime
        return (_printtime_.minutes * 1.0)



    
    @pyqtSlot(float)
    def setPricePerKG(self, price):
        self._price_per_kg = float(price)
        self.pricePerKgChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/price_per_kg", price);
    
    @pyqtSlot(float)    
    def setDensity(self, density):
        self._density = float(density)
        self.densityChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/density", density);

    @pyqtSlot(float)
    def setPricePKWH(self, price_kwh_cent):
        self._price_kwh_cent = float(price_kwh_cent)
        self.PricePKWHChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/price_kwh_cent", price_kwh_cent);

    @pyqtSlot(float)
    def setPowerConsump(self, power_consumtion_printer_watt):
        self._power_consumtion_printer_watt = float(power_consumtion_printer_watt)
        self.PowerConsumpChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/power_consumtion_printer_watt", power_consumtion_printer_watt);

    @pyqtSlot(float)
    def setPrinterCost(self, printer_cost):
        self._printer_cost = float(printer_cost)
        self.PrinterCostChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/printer_cost", printer_cost);

    @pyqtSlot(float)
    def setPrinterLastingHours(self, printer_lasting_hours):
        self._printer_lasting_hours = float(printer_lasting_hours)
        self.PrinterLastingHoursChanged.emit()
        Preferences.getInstance().setValue("electric_print_cost_calculator/printer_lasting_hours", printer_lasting_hours);


    def _createCostView(self):
        path = QUrl.fromLocalFile(os.path.join(PluginRegistry.getInstance().getPluginPath("ElectricPrintCostCalculator"), "ElectricPrintCostCalculator.qml"))
        self._component = QQmlComponent(Application.getInstance()._engine, path)

        self._context = QQmlContext(Application.getInstance()._engine.rootContext())
        self._context.setContextProperty("manager", self)
        self._cost_view = self._component.create(self._context)
    
    def showPopup(self):
        if self._cost_view is None:
            self._createCostView()
        self._cost_view.show()

