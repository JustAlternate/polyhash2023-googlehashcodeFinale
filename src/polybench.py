from polywriter import Writer
import resource
import sys
import time


def time_writer(file: str, method: str):
    t1 = time.perf_counter()
    d1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Writer(str(file), str(method))
    t2 = time.perf_counter()
    d2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(str(file) + " : " + " " * (40 - len(str(file)))
          + str(round(t2 - t1, 3)) + " seconds")
    print(" " * (43) + str((d2 - d1) / 1000) + " MB")


def bench(method: str = None, challenge: str = None):

    challenge_to_bench = [
        "challenges/a_example.in",
        "challenges/b_busy_day.in",
        "challenges/c_redudancy.in",
        "challenges/d_mother_of_all_warehouses.in",
    ]

    algos_to_bench = [
        "theo",
        "loic",
        "amedeo",
    ]

    if method is None and challenge is None:
        for algo in algos_to_bench:
            print("===========")
            print("Using " + str(algo) + " algorithm...")
            for file in challenge_to_bench:
                time_writer(file, algo)
        print("===========")

    if method is not None and challenge is None:
        print("===========")
        print("Using " + str(method) + " algorithm...")
        for file in challenge_to_bench:
            time_writer(file, method)
        print("===========")

    elif method is not None and challenge is not None:
        print("===========")
        print("Using " + str(method) + " algorithm...")
        time_writer(challenge, method)
        print("===========")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "usage: python polybench.py [theo|loic|amedeo] [challenges/map.in]"
        )
    if len(sys.argv) == 2:
        bench(sys.argv[1])
    elif len(sys.argv) >= 3:
        bench(sys.argv[1], sys.argv[2])
    else:
        bench()
