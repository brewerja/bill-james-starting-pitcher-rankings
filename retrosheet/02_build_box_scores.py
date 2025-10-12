#!/usr/bin/env python

import os
import subprocess


def build_box_scores(base):
    input_path = base + "/" + "events"
    output_path = "../" + "box_scores"
    os.chdir(input_path)

    years = set()
    for file in os.listdir("."):
        if file.endswith(".EVN") or file.endswith(".EVA") or file.endswith(".EVE"):
            years.add(int(file[:4]))

    for year in sorted(years):
        command = f"cwbox -X -y {year} {year}*.EV* > {output_path}/{year}.xml"
        print(command)
        subprocess.call(command, shell=True)

    os.chdir("../..")


if __name__ == "__main__":
    build_box_scores("regular_season")
    build_box_scores("postseason")
