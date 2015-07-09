from PyQt5.QtCore import  QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
from UM.Extension import Extension
from UM.PluginRegistry import PluginRegistry
import os.path
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlComponent, QQmlContext
from UM.Application import Application
from UM.Preferences import Preferences

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("PrintCostCalculator")


class PrintCostCalculator(QObject,  Extension):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._cost_view = None
        self.addMenuItem(i18n_catalog.i18n("Calculate"), self.showPopup)
        Application.getInstance().activeMachineChanged.connect(self._onActiveMachineChanged)
        self._print_information = None
        self._material_diameter = 2.85
        Preferences.getInstance().addPreference("print_cost_calculator/price_per_kg", "30")
        Preferences.getInstance().addPreference("print_cost_calculator/density", "1240")
        
        self._price_per_kg = float(Preferences.getInstance().getValue("print_cost_calculator/price_per_kg"))
        self._density = float(Preferences.getInstance().getValue("print_cost_calculator/density"))
        print(self._price_per_kg)
        
    materialAmountChanged = pyqtSignal()
    materialDiameterChanged = pyqtSignal()
    densityChanged = pyqtSignal()
    pricePerKgChanged = pyqtSignal()
    
    def _onMaterialDiameterChanged(self, value):
        self._material_diameter = value
        self.materialDiameterChanged.emit()
    
    def _onActiveMachineChanged(self):
        self._settings = Application.getInstance().getActiveMachine()
        if self._settings:
            material_diameter = self._settings.getSettingByKey("material_diameter")
            if material_diameter:
                material_diameter.valueChanged.connect(self._onMaterialDiameterChanged)

    def _onActiveMachineChanged(self):
        self._print_information = Application.getInstance()._print_information  #Yes, this is bad. Theres no getter/setter :(
        self._print_information.materialAmountChanged.connect(self.materialAmountChanged)

    @pyqtProperty(float, notify = materialAmountChanged)
    def materialAmountLength(self):
        return self._print_information.materialAmount
    
    @pyqtProperty(float, notify = materialDiameterChanged)
    def materialDiameter(self):
        return self._material_diameter
    
    @pyqtProperty(float, notify = pricePerKgChanged)
    def pricePerKg(self):
        return self._price_per_kg
    
    @pyqtProperty(float, notify = densityChanged)
    def density(self):
        return self._density
    
    @pyqtSlot(float)
    def setPricePerKG(self, price):
        self._price_per_kg = float(price)
        self.pricePerKgChanged.emit()
        Preferences.getInstance().setValue("print_cost_calculator/price_per_kg", price);
    
    @pyqtSlot(float)    
    def setDensity(self, density):
        self._density = float(density)
        self.densityChanged.emit()
        Preferences.getInstance().setValue("print_cost_calculator/density", density);
    
    def showPopup(self):
        if self._cost_view is None:
            path = QUrl.fromLocalFile(os.path.join(PluginRegistry.getInstance().getPluginPath("PrintCostCalculator"), "PrintCostCalculator.qml"))
            self._component = QQmlComponent(Application.getInstance()._engine, path)

            self._context = QQmlContext(Application.getInstance()._engine.rootContext())
            self._context.setContextProperty("manager", self)
            self._cost_view = self._component.create(self._context)
            
        if self._cost_view:    
            self._cost_view.show()