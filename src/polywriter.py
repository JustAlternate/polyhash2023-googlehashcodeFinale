#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from polysolvers.polysolver_autre import naive_approach_autre
from polysolvers.polysolver_naive_loic import naive_approach_loic
from polysolvers.polysolver_naive_theo import naive_approach_theo


def Writer(challenge: str, method: str) -> None:
    if method == "loic":
        solution = naive_approach_loic(challenge)
    elif method == "theo":
        solution = naive_approach_theo(challenge)
    elif method == "amedeo":
        solution = naive_approach_autre(challenge)
    else:
        print("Cette algorithme n'existe pas")
        return

    # basename the challenge name and add .out at the end.
    output_name = (
            "solutions/" + "solutions_"
            + str(method)
            + "/"
            + str(str(challenge.split("/")[-1]).split(".")[0]) + ".out"
    )

    with open(output_name, "w") as f:
        # Write the number of line at the begining.
        f.write(str(len(solution)) + "\n")
        for line in solution:
            f.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python polywriter.py \
        loic | theo | amedeo challenges/ma_map.in ")
    else:
        Writer(sys.argv[2], sys.argv[1])
