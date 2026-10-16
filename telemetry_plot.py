#!/usr/bin/env python3
"""
Drone Telemetry Lab
Reads CSV telemetry with:
timestamp, latitude, longitude, altitude_m, speed_mps, battery_v

Produces:
- basic flight stats
- altitude plot
- speed plot
"""

import argparse
import csv
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt

def load_csv(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "timestamp": r["timestamp"],
                "latitude": float(r["latitude"]),
                "longitude": float(r["longitude"]),
                "altitude_m": float(r["altitude_m"]),
                "speed_mps": float(r["speed_mps"]),
                "battery_v": float(r["battery_v"]),
            })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvfile")
    ap.add_argument("--outdir", default="plots")
    args = ap.parse_args()

    rows = load_csv(args.csvfile)
    if not rows:
        raise SystemExit("No telemetry rows found.")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    alt = [r["altitude_m"] for r in rows]
    speed = [r["speed_mps"] for r in rows]
    batt = [r["battery_v"] for r in rows]

    print(f"Samples: {len(rows)}")
    print(f"Max altitude: {max(alt):.2f} m")
    print(f"Max speed: {max(speed):.2f} m/s")
    print(f"Average speed: {mean(speed):.2f} m/s")
    print(f"Battery range: {max(batt):.2f} V -> {min(batt):.2f} V")

    x = list(range(len(rows)))

    plt.figure()
    plt.plot(x, alt)
    plt.xlabel("Sample")
    plt.ylabel("Altitude (m)")
    plt.title("Flight Altitude")
    plt.tight_layout()
    plt.savefig(outdir / "altitude.png", dpi=160)
    plt.close()

    plt.figure()
    plt.plot(x, speed)
    plt.xlabel("Sample")
    plt.ylabel("Speed (m/s)")
    plt.title("Flight Speed")
    plt.tight_layout()
    plt.savefig(outdir / "speed.png", dpi=160)
    plt.close()

    print(f"Plots written to {outdir}")

if __name__ == "__main__":
    main()
