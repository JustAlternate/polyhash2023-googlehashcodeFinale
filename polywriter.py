#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polysolvers.polysolver_naive_loic import *
import sys


def Writer(challenge: str, method: str) -> None:

    if method == "naive_loic":
        Solution = naive_approach_loic(challenge)
    if method == "naive_AmeTheo":
        Solution = naive_approach_AmeTheo(challenge)

    # basename the challenge name and add .out at the end.
    output_name = "solutions/" + \
        str(str(challenge.split("/")[-1]).split(".")[0])+".out"

    with open(output_name, 'w') as f:
        # Write the number of line at the begining.
        f.write(str(len(Solution)) + '\n')
        for line in Solution:
            f.write(line + '\n')

    print("Done Writing to : "+str(output_name))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python polywriter.py naive_loic|naive_AmeTheo challenges/ma_map.in")
    else:
        Writer(sys.argv[2], sys.argv[1])
