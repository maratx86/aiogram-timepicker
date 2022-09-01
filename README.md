# Time Selection tool for Aiogram Telegram Bots

## Description
A simple inline time selection tool for [aiogram](https://github.com/aiogram/aiogram) telegram bots written in Python.

Offers 6 types of time picker:
* Full Time Picker - user can select a time with hours, minutes and seconds.
* Minute & Second Picker - user can select a time with minutes and seconds.
* Single Hour Picker - user can select a hour.
* Single Minute Picker - user can select a minute.
* Single Second Picker - user can select a second.
* Carousel Full Time Picker - user can select a time with hours, minutes and seconds with carousel.

## Usage
Install package with pip

        pip install aiogram_timepicker

A full working example on how to use aiogram-timepicker is provided in *bot_example.py*. 
You create a timepicker panel and add it to a message with a *reply_markup* parameter, and then you can process it in a `callbackqueyhandler` method using the *process_selection* method.

## Demo
Demonstration of this tool with [**bot_example.py**](./bot_example.py).


![demo](https://s6.gifyu.com/images/bot.gif)

## Licence
Read more about licence [here](./LICENSE.txt).