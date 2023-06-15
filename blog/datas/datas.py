import pandas as pd
import os
import pynecone as pc


def read_data(filename):
    if filename[-4:] == "xlsx":
        return pd.read_excel(filename, header=None)
    elif filename[-3:] == "csv":
        return pd.read_csv(filename, header=None, low_memory=False)


def kickstarter():
    filename = os.path.join("data", "kickstarter.xlsx")
    return pc.center(
        pc.data_table(
            data=read_data(filename),
            pagination=True,
            search=True,
            sort=True,
            resizable=True,
        ),
        width="100%",
    )


def lianjia():
    filename = os.path.join("data", "lianjia.csv")
    return pc.center(
        pc.data_table(
            data=read_data(filename),
            pagination=True,
            search=True,
            sort=True,
            resizable=True,
        ),
        width="100%",
    )
