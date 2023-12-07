#!/bin/bash

pyinstaller --onefile --add-data "venv/lib/python3.11/site-packages/pyautogui:pyautogui" --add-data "venv/lib/python3.11/site-packages/pyautogui/*:pyautogui" main.py
