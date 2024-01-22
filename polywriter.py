#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polysolver_naive_loic import naive_approach_loic
from polysolver_amedeo import naive_approach_amedeo
import sys


def Writer(challenge: str, method: str) -> None:
    if method == "naive_loic":
        Solution = naive_approach_loic(challenge)
    elif method == "naive_theo":
        raise "not implemented"
    elif method == "naive_amedeo":
        Solution = naive_approach_amedeo(challenge)
    else:
        print("La solution n'existe pas")
        return

    # basename the challenge name and add .out at the end.
    output_name = (
            "solutions/" + str(str(challenge.split("/")
                                   [-1]).split(".")[0]) + ".out"
    )

    with open(output_name, "w") as f:
        # Write the number of line at the begining.
        f.write(str(len(Solution)) + "\n")
        for line in Solution:
            f.write(line + "\n")

    print("Done Writing to : " + str(output_name))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "usage: python polywriter.py naive_loic|naive_theo|naive_amedeo challenges/ma_map.in"
        )
    else:
        Writer(sys.argv[2], sys.argv[1])
