#!/usr/bin/env python
# -*- coding: utf-8 -*-
from polysolvers import (naive_approach_loic,
                         naive_approach_theo,
                         naive_approach_amedeo)
import sys


def Writer(challenge: str, method: str) -> None:
    if method == "naive_loic":
        solution = naive_approach_loic(challenge)
    elif method == "naive_theo":
        solution = naive_approach_theo(challenge)
    elif method == "naive_amedeo":
        solution = naive_approach_amedeo(challenge)
    else:
        print("La solution n'existe pas")
        return

    # basename the challenge name and add .out at the end.
    output_name = ("solutions/" + str(str(challenge.split("/")[-1])
                                      .split(".")[0]) + ".out"
                   )

    with open(output_name, "w") as f:
        # Write the number of line at the begining.
        f.write(str(len(solution)) + "\n")
        for line in solution:
            f.write(line + "\n")

    print("Done Writing to : " + str(output_name))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python polywriter.py \
        naive_loic | naive_theo ../challenges/ma_map. in ")
    else:
        Writer(sys.argv[2], sys.argv[1])
