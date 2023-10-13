# Об'єкт, який необхідно знайти
# Вводити в наступному форматі: TIC XX...X
# Наприклад: TIC 141809359
OBJECT: str = "TIC 141809359"
# Сектори
# Вводити в форматі списку чисел
# Наприклад: [1, 3, 66]
# Якщо необхідно всі сектори, то достатньо ввести пустий список - []
SECTORS: list = [1, 3, 66]

# -----------------DOWNLOAD DATA FROM MATS----------------------#
from astroquery.mast import Observations
from astropy.table import Table
import numpy as np


def get_filtered_obs_table(obs_table: Table, column: str) -> Table:
    if len(SECTORS) == 0:
        return obs_table
    return obs_table[np.isin(obs_table[column], SECTORS)]


def download_data() -> list:
    obs_table = Observations.query_criteria(
        objectname=OBJECT,
        target_name=OBJECT.split(" ")[1],
        project="TESS",
        obs_collection="TESS",
    )

    product_list = Observations.get_product_list(
        get_filtered_obs_table(obs_table, "sequence_number")
    )
    selected_products = Observations.filter_products(
        product_list, productSubGroupDescription="LC"
    )
    downloaded_files = Observations.download_products(
        selected_products, download_dir=".", extension="fits"
    )["Local Path"].tolist()
    return downloaded_files


# -----------------DATA PROCESSING-------------------#
import os
import matplotlib
from astropy.io import fits
import matplotlib.pyplot as plt
import math


def save_data(JD, mag, star_name: str, sector: int, dir: str):
    X = [[JD[j], mag[j]] for j in range(len(JD))]
    X = np.array(X)
    fig = plt.figure(1)
    fig.set_size_inches(15, 8)
    plt.plot(JD, mag, ".k", markersize=2)
    plt.gca().invert_yaxis()
    plt.title(f"TIC {star_name} sector {sector}", fontsize=20)
    plt.xlabel("JD - 2 457 000", fontsize=16)
    plt.ylabel("magnitude, mmag", fontsize=16)
    matplotlib.rc("xtick", labelsize=16)
    matplotlib.rc("ytick", labelsize=16)
    plt.savefig(f"{dir}\TIC_{star_name}__mag.png", dpi=100)
    plt.close()

    fname = f"{dir}\TIC_{star_name}__mag.tess"
    np.savetxt(fname, X)


def handle_data(files: list):
    def get_star_name(file: str) -> str:
        file_name = os.path.splitext(os.path.basename(file))[0]
        name_parts = file_name.split("-")
        star_name = str(int(name_parts[-3]))
        return star_name

    def get_sector(file: str) -> int:
        file_name = os.path.splitext(os.path.basename(file))[0]
        name_parts = file_name.split("-")
        sector = int(name_parts[-4][1:])
        return sector

    for f in files:
        try:
            with fits.open(f, mode="readonly") as hdulist:
                JD = hdulist[1].data["TIME"]
                flux = hdulist[1].data["PDCSAP_FLUX"]

            JD = list(JD)
            flux = list(flux)
            tf = [math.isnan(flux[j]) for j in range(len(flux))]
            j = 0
            while j < len(flux):
                if tf[j] == True:
                    del tf[j]
                    del flux[j]
                    del JD[j]
                else:
                    j += 1

            JD, flux = np.array(JD), np.array(flux)
            mag = -2.5 * np.log10(flux)
            mag -= np.average(mag)
            mag *= 1000

            abspath_to_file = os.path.abspath(f)
            dir = os.path.dirname(abspath_to_file)

            save_data(JD, mag, get_star_name(f), get_sector(f), dir)

        except Exception as e:
            print(f"ERROR - {e}")

print("Getting data from MAST. This may take up to 2 minutes...")
files = download_data()
handle_data(files)
