#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.polywriter import Writer
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python polyhash.py naive_loic|naive_theo")
    else:
        print("Generating solutions using " + str(sys.argv[1]))

        for file in os.listdir("challenges/"):
            Writer("challenges/" + str(file), sys.argv[1])
