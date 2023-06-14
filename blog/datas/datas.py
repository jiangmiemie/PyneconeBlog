import pandas as pd
import os
import pynecone as pc


def travellast():
    filename = os.path.join("data", "travellast.csv")
    travel = pd.read_csv(filename, header=None)
    return pc.center(
        pc.data_table(
            data=travel,
            pagination=True,
            search=True,
            sort=True,
            resizable=True,
        ),
        padding_top="6em",
        width="100%",
    )
