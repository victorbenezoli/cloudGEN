import numpy as np
import json
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--isleap", nargs=1, type=int, default=0, help="Type 1 to leap year or 0 to non-leap year")
    args = parser.parse_args()

    isleap = args.isleap[0]

    if (isleap != 0 and isleap != 1):
        print("Option --isleap needs to be 0 (non-leap year) or 1 (leap year).")
        exit()

    with open('conf/params.conf') as f:
        params = json.load(f)

    res = params['gridprop']['res']
    lat1 = params['gridprop']['lat1'] + (res / 2.0)
    lat2 = params['gridprop']['lat2']
    lon1 = params['gridprop']['lon1'] + (res / 2.0)
    lon2 = params['gridprop']['lon2']

    lat = np.arange(lat1, lat2, res)
    lon = np.arange(lon1, lon2, res)


if __name__ == '__main__':
    main()
