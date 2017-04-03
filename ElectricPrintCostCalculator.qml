// Copyright (c) 2017 Zoff
// https://github.com/zoff99/ElectricPrintCostCalculator

// Copyright (c) 2015 Jaime van Kessel.
// PrintCostCalculator is released under the terms of the AGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Window 2.2
import QtQuick.Controls 1.2

import UM 1.0 as UM

UM.Dialog
{
    modality: Qt.NonModal
    id: base;
    width: 480 * Screen.devicePixelRatio;
    height: 390 * Screen.devicePixelRatio;
    visible: true;
    title:  qsTr("Calculate electrical print cost")
    property real material_amount_length: manager.materialAmountLength == -1 ? 0 : manager.materialAmountLength
    property real pi: 3.1415 
    property real material_radius:  0.5 * manager.materialDiameter
    property real material_amount_volume:  pi * material_radius * material_radius * material_amount_length / 1000000 
    property real density: manager.density
    property real kg_material: material_amount_volume * density
    property real price_per_kg : manager.pricePerKg 

    property real price_kwh_cent: manager.price_kwh_cent
    property real power_consumtion_printer_watt: manager.power_consumtion_printer_watt
    property real printer_cost: manager.printer_cost
    property real printer_lasting_hours: manager.printer_lasting_hours
    property real printing_time_h: manager.printing_time_h
    property real printing_time_m: manager.printing_time_m
    property real printing_time_in_hours: (printing_time_h + (printing_time_m/60))
    property real material_cost: manager.material_cost
   
    Column
    {
        anchors.fill: parent;
        Row
        {
            Text 
            {
                text: "Price per Kwh in Euro Cent: "
            }
            TextField 
            { 
                id: price_kwh_cent_field
                text: price_kwh_cent
                Keys.onReleased:
                {
                    manager.setPricePKWH(price_kwh_cent_field.text)
                }
            }
        }
        Row 
        {
            Text 
            {
                text: "Power consumption in Watt: "
            }
            TextField 
            { 
                id: power_consumtion_printer_watt_field
                text: power_consumtion_printer_watt
                Keys.onReleased:
                {
                    manager.setPowerConsump(power_consumtion_printer_watt_field.text)
                }
            }
        }




        Row 
        {
            Text 
            {
                text: "Printer cost in Euro: "
            }
            TextField 
            { 
                id: printer_cost_field
                text: printer_cost
                Keys.onReleased:
                {
                    manager.setPrinterCost(printer_cost_field.text)
                }
            }
        }

        Row 
        {
            Text 
            {
                text: "Printer will last this many hours: "
            }
            TextField 
            { 
                id: printer_lasting_hours_field
                text: printer_lasting_hours
                Keys.onReleased:
                {
                    manager.setPrinterLastingHours(printer_lasting_hours_field.text)
                }
            }
        }

        Row 
        {
            Text 
            {
                text: " "
            }
        }

//        Row 
//        {
//            Text 
//            {
//                color: "green"
//                text: "fill these with your current model values:"
//            }
//        }

        Row 
        {
            Text 
            {
                color: "green"
                text: "Printing Time: [HH:MM]"
            }
            TextField
            {
                width: 36 * Screen.devicePixelRatio
                readOnly : true
                id: printing_time_h_field
                text: printing_time_h
                maximumLength: 4
            }
            TextField
            {
                width: 18 * Screen.devicePixelRatio
                id: printing_time_colon
                readOnly : true
                text: ":"
                maximumLength: 1
            }
            TextField
            {
                width: 36 * Screen.devicePixelRatio
                readOnly : true
                id: printing_time_m_field
                text: printing_time_m
                maximumLength: 2
            }
        }

        Row 
        {
            Text 
            {
                color: "green"
                text: "Material Cost in Euro: "
            }
            TextField 
            { 
                id: material_cost_field
                readOnly : true
                text: material_cost.toFixed(2)
            }
        }

        Row 
        {
			Text
			{
				text: " "
			}
		}


        Row 
        {
			Text
			{
				text: "Electrical Cost: " + ( (price_kwh_cent/100) * (power_consumtion_printer_watt/1000) * printing_time_in_hours ).toFixed(2) + " Euro"
			}
        }
        // ( (price_kwh_cent/100) * (power_consumtion_printer_watt/1000) * printing_time_in_hours )

        Row 
        {
			Text
			{
				text: "Material Cost: " + (material_cost_field.text * 1.0).toFixed(2) + " Euro"
			}
        }

        Row 
        {
			Text
			{
				text: "Printer Cost: " + ( (printer_cost/printer_lasting_hours) * printing_time_in_hours ).toFixed(2) + " Euro"
			}
		}
        // (printer_cost/printer_lasting_hours) * printing_time_in_hours

        Row 
        {
			Text
			{
				text: " "
			}
		}


        Row 
        {
			Text
			{
                color: "red"
				text: "TOTAL Cost: " + (1.0*(( (price_kwh_cent/100) * (power_consumtion_printer_watt/1000) * printing_time_in_hours )* 1.0 + ((printer_cost/printer_lasting_hours) * printing_time_in_hours)* 1.0 + (material_cost_field.text * 1.0))).toFixed(2) + " Euro"
			}
		}

        Row 
        {
            Text 
            {
                text: " "
            }
        }


        Button
        {
            
            text: qsTr("Cancel");
            onClicked: 
            {
                base.visible = false;
            }
        }
    }
}
