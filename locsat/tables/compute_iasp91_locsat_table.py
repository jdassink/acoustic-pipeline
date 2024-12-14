"""
Script to generate an iasp91-style table for LOCSAT

.. module:: compute_locsat_table

:author:
    Jelle Assink (jelle.assink@knmi.nl)

:copyright:
    2021, Jelle Assink

:license:
    This code is distributed under the terms of the
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.en.html)

To compute an example table, assuming a constant sound speed of 0.34 km/s

python compute_iasp91_locsat_table.py -p Is -c 0.34
"""

import argparse
import numpy as np
from obspy.geodetics import kilometer2degrees, degrees2kilometers

# Define depth and distance samples
z_samples = np.array([0.0])
d_samples = np.array([0.0, 0.1, 0.5, 1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0])
r_samples = degrees2kilometers(d_samples)

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate IASP91 travel-time tables.")
    parser.add_argument(
        "-p", "--phase",
        type=str,
        metavar="LOCSAT phase name",
        required=True,
        help="Specify the phase name for the travel-time table."
    )
    parser.add_argument(
        "-c", "--group_speed",
        type=float,
        metavar="Group speed",
        required=True,
        help="Specify the group speed for the calculations."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    return parser.parse_args()

# Generate travel-time table
def generate_travel_time_table(phase, group_speed, verbose=False):
    file_name = f"iasp91.{phase}"
    if verbose:
        print(f"Generating travel-time table for phase: {phase}")
        print(f"Output file: {file_name}")
        print(f"Group speed: {group_speed}")

    with open(file_name, "w") as f:
        # Header
        f.write(f"n # {phase} travel-time tables\n")
        f.write(f"{len(z_samples)} # number of depth samples\n")

        # Write depth samples
        for i, z in enumerate(z_samples, 1):
            f.write(f"{z:8.2f}")
            if i % 10 == 0 or i == len(z_samples):
                f.write("\n")

        # Write distance samples
        f.write(f"{len(d_samples)} # number of distance samples\n")
        for i, d in enumerate(d_samples, 1):
            f.write(f"{d:8.2f}")
            if i % 10 == 0 or i == len(d_samples):
                f.write("\n")

        # Write travel-time and amplitude
        for i, z in enumerate(z_samples):
            f.write(f"# Travel-time/amplitude for z = {z:8.2f}\n")
            for r in r_samples:
                travel_time = np.sqrt(z**2 + r**2) / group_speed
                f.write(f"{travel_time:12.3f}\n")

    if verbose:
        print(f"Travel-time table successfully written to {file_name}")

# Main execution
if __name__ == "__main__":
    args = parse_arguments()
    generate_travel_time_table(args.phase, args.group_speed, args.verbose)
