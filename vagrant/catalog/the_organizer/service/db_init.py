from the_organizer.models import Item, ItemAttribute, ItemImage, Group, GroupMap, AttributeMap
from datetime import datetime
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from ..webapp import database as db
from sqlalchemy import and_
import re

import csv
import requests
import json
from time import sleep



"""
Create Inital Items for Testing
"""
def init_db():

    electronics = Group.add(None, 'Electronics', '0', 1).insert()
    electronics = Group.add(electronics, 'Microcontrollers', '0', 1).insert()
    electronics = Group.add(electronics, 'Arduino', '0', 1).insert()
    uno_id = 'c1a82ce5-ce04-4529-ba08-f25c7044262c'

    a1=AttributeMap.add(uno_id, 'Microcontroller', '0', 1).insert()
    a2=AttributeMap.add(uno_id, 'Operating Voltage', '0', 1).insert()
    a3=AttributeMap.add(uno_id, 'Input Voltage (recommended)', '0', 1).insert()
    a4=AttributeMap.add(uno_id, 'Input Voltage (limit)', '0', 1).insert()
    a5=AttributeMap.add(uno_id, 'Digital I/O Pins', '0', 1).insert()
    a6=AttributeMap.add(uno_id, 'PWM Digital I/O Pins', '0', 1).insert()



    arduino_uno = Item.add(
        'Arduino Uno',
        'Arduino Uno R3 Microcontroller',
        'Arduino/Genuino Uno is a microcontroller board based on the ATmega328P (datasheet). It has 14 digital input/output pins (of which 6 can be used as PWM outputs), 6 analog inputs, a 16 MHz quartz crystal, a USB connection, a power jack, an ICSP header and a reset button. It contains everything needed to support the microcontroller; simply connect it to a computer with a USB cable or power it with a AC-to-DC adapter or battery to get started.. You can tinker with your UNO without worring too much about doing something wrong, worst case scenario you can replace the chip for a few dollars and start over again.', 
        'A000066', 
        'https://www.arduino.cc/en/main/arduinoBoardUno', 
        'https://www.amazon.com/Arduino-Uno-R3-Microcontroller-A000066/dp/B008GRTSV6/ref=sr_1_3?ie=UTF8&qid=1490503039&sr=8-3&keywords=arduino+uno',
        'https://www.arduino.cc/en/uploads/Main/A000066_iso_both.jpg'
        )
    uno_id = arduino_uno.insert()
    ItemAttribute.add(uno_id, a1, 'Microcontroller', 'ATmega328P', 1).insert()
    ItemAttribute.add(uno_id, a2, 'Operating Voltage', '5V', 1).insert()
    ItemAttribute.add(uno_id, a3, 'Input Voltage (recommended)', '7-12V', 1).insert()
    ItemAttribute.add(uno_id, a4, 'Input Voltage (limit)', '6-20V', 1).insert()
    ItemAttribute.add(uno_id, a5, 'Digital I/O Pins', '14 (of which 6 provide PWM output)', 1).insert()
    ItemAttribute.add(uno_id, a6, 'PWM Digital I/O Pins', '6', 1).insert()

    GroupMap.add(uno_id, electronics, 'Arduino', '0', 1).insert()

    ItemImage.add(uno_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000066_featured_1024x1024.jpg?v=1460564034').insert()
    ItemImage.add(uno_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000066_back_1024x1024.jpg?v=1460564047').insert()
    ItemImage.add(uno_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000066_iso_1024x1024.jpg?v=1460564060').insert()
    ItemImage.add(uno_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000066_unbox_1024x1024.jpg?v=1460564075').insert()






    arduino_mega = Item.add(
        'Arduino MEGA 2560',
        'ARDUINO A000067 DEV BRD, ATMEGA2560, ARDUINO MEGA 2560 R3',
        'Dont limit your projects, think big, think MEGA! The Arduino Mega 2560 has been designed with bigger and more ambitious projects in mind. The large number of analog and digital pins, together with a larger memory makes it ideal for devices like 3D printers and other demanding applications. Backward compatibility with existing shields and sketches is provided, but other shields target the Mega specifically, exploiting the full potential of this board.', 
        'A000067', 
        'https://www.arduino.cc/en/Main/ArduinoBoardMega2560', 
        'https://www.amazon.com/ARDUINO-A000067-ATMEGA2560-2560-R3/dp/B0046AMGW0/ref=sr_1_5?s=electronics&ie=UTF8&qid=1490503308&sr=1-5&keywords=arduino+mega',
        'https://www.arduino.cc/en/uploads/Main/AG_Mega.jpg'
        )
    mega_id = arduino_mega.insert()
    ItemAttribute.add(mega_id, a1, 'Microcontroller', 'ATmega328P', 1).insert()
    ItemAttribute.add(mega_id, a2, 'Operating Voltage', '5V', 1).insert()
    ItemAttribute.add(mega_id, a3, 'Input Voltage (recommended)', '7-12V', 1).insert()
    ItemAttribute.add(mega_id, a4, 'Input Voltage (limit)', '6-20V', 1).insert()
    ItemAttribute.add(mega_id, a5, 'Digital I/O Pins', '14 (of which 6 provide PWM output)', 1).insert()
    ItemAttribute.add(mega_id, a6, 'PWM Digital I/O Pins', '6', 1).insert()

    GroupMap.add(mega_id, electronics, 'Arduino', '0', 1).insert()

    ItemImage.add(mega_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000067_featured_1024x1024.jpg?v=1462970806').insert()
    ItemImage.add(mega_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000067_back_1024x1024.jpg?v=1462970821').insert()
    ItemImage.add(mega_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000067_iso_1024x1024.jpg?v=1462970835').insert()
    ItemImage.add(mega_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000067_unbox_1024x1024.jpg?v=1462970860').insert()


    arduino_nano = Item.add(
        'Arduino Nano',
        'OSOYOO Mini USB Nano V3.0 ATMEGA328P',
        'The Arduino Nano is a small, complete, and breadboard-friendly board based on the ATmega328 (Arduino Nano 3.x). It has more or less the same functionality of the Arduino Duemilanove, but in a different package. It lacks only a DC power jack, and works with a Mini-B USB cable instead of a standard one', 
        'A000066', 
        'https://www.arduino.cc/en/Main/ArduinoBoardNano', 
        'https://www.amazon.com/OSOYOO-ATMEGA328P-Module-Micro-controller-Arduino/dp/B00UACD13Q/ref=sr_1_5?s=electronics&ie=UTF8&qid=1490503461&sr=1-5&keywords=arduino+nano',
        'https://www.arduino.cc/en/uploads/Main/Nano.jpg'
        )
    nano_id = arduino_nano.insert()

    ItemAttribute.add(nano_id, a1, 'Microcontroller', 'ATmega328P', 1).insert()
    ItemAttribute.add(nano_id, a2, 'Operating Voltage', '5V', 1).insert()
    ItemAttribute.add(nano_id, a3, 'Input Voltage (recommended)', '7-12V', 1).insert()
    ItemAttribute.add(nano_id, a4, 'Input Voltage (limit)', '6-20V', 1).insert()
    ItemAttribute.add(nano_id, a5, 'Digital I/O Pins', '14 (of which 6 provide PWM output)', 1).insert()
    ItemAttribute.add(nano_id, a6, 'PWM Digital I/O Pins', '6', 1).insert()

    GroupMap.add(nano_id, electronics, 'Arduino', '0', 1).insert()

    ItemImage.add(nano_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000005_Featured_1024x1024.jpg?v=1484911884').insert()
    ItemImage.add(nano_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000005_iso_1024x1024.jpg?v=1484911887').insert()
    ItemImage.add(nano_id, 'https://cdn.shopify.com/s/files/1/0775/1525/products/A000005_back_1024x1024.jpg?v=1484911891').insert()
    # ItemImage.add(nano_id, 'xxxx').insert()





