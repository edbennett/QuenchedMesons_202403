#!/usr/bin/env python3

import csv
import itertools


def get_args():
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("--output_csv", required=True, type=FileType("w"))
    return parser.parse_args()


def get_file_data(representation, Nc, channel, observable):
    plurals = {"mass": "masses", "decayconst": "decayconsts"}
    filename = (
        f"processed_data/Sp{Nc}/continuum/{representation}/"
        f"{channel}_{plurals[observable]}_{representation}_Sp{Nc}.dat"
    )
    datum = {
        "Nc": Nc,
        "representation": representation,
        "observable": observable,
        "channel": channel,
    }
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return

    if len(lines) != 4:
        raise ValueError("Wrong length data.")

    for label, line in zip(["chiral_limit", "L0", "W0"], lines):
        datum[f"{label}_value"], datum[f"{label}_uncertainty"] = map(
            float, line.split()
        )
    datum["chisquare"] = float(lines[3].split()[0])
    return datum


def get_all_data():
    representations = "F", "AS", "S"
    Ncs = 4, 6, 8
    all_channels = {
        "mass": ["vector", "axialvector", "scalar", "tensor", "axialtensor"],
        "decayconst": ["pseudoscalar", "vector", "axialvector"],
    }
    channel_observables = [
        (channel, observable)
        for observable, channels in all_channels.items()
        for channel in channels
    ]
    return [
        get_file_data(representation, Nc, channel, observable)
        for representation, Nc, (channel, observable) in itertools.product(
            representations, Ncs, channel_observables
        )
    ]


def write_csv(data, output_file):
    writer = csv.DictWriter(
        output_file,
        [
            "Nc",
            "representation",
            "observable",
            "channel",
            "chiral_limit_value",
            "chiral_limit_uncertainty",
            "L0_value",
            "L0_uncertainty",
            "W0_value",
            "W0_uncertainty",
            "chisquare",
        ],
    )
    writer.writeheader()
    for datum in data:
        if datum:
            writer.writerow(datum)


def main():
    args = get_args()
    data = get_all_data()
    write_csv(data, args.output_csv)


if __name__ == "__main__":
    main()