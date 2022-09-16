import argparse
import os

import cdsapi


def download_era5(root, year, variable, pressure=False):
    months = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
    ]
    days = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
    ]
    times = [
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    c = cdsapi.Client()
    print(f"Downloading {variable} data for year {year}, pressure={pressure}")
    fn = os.path.join(root, variable, f"{variable}_{year}_0.25deg.nc")
    if os.path.exists(fn):
        return
    os.makedirs(os.path.join(root, variable), exist_ok=True)
    download_args = {
        "product_type": "reanalysis",
        "format": "netcdf",
        "variable": variable,
        "year": str(year),
        "month": months,
        "day": days,
        "time": times,
    }
    if not pressure:
        c.retrieve(
            "reanalysis-era5-single-levels",
            download_args,
            fn,
        )
    else:
        download_args["pressure_level"] = [1000, 850, 500, 50]
        c.retrieve(
            "reanalysis-era5-pressure-levels",
            download_args,
            fn,
        )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--root", type=str, default="")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--variable", type=str, required=True)
    parser.add_argument("--pressure", action="store_true", default=False)

    args = parser.parse_args()

    download_era5(args.root, args.year, args.variable, args.pressure)


if __name__ == "__main__":
    main()
