from io import BytesIO, StringIO

import pandas as pd

WIN_ENCODING = "cp932"


def obj2df(obj, ext="csv") -> pd.core.frame.DataFrame:
    if ext == "xlsx":
        return load_df(BytesIO(obj), ext)

    if ext == "csv":
        try:
            decoding = obj.decode()
        except Exception:
            decoding = obj.decode(WIN_ENCODING)

        return load_df(StringIO(decoding))


def load_df(filename_or_buffer, ext="csv") -> pd.core.frame.DataFrame:
    if ext == "xlsx":
        return pd.read_excel(filename_or_buffer)

    if ext == "csv":
        try:
            return pd.read_csv(filename_or_buffer)
        except Exception:
            # windowsから作成されたもの用の処理
            return pd.read_csv(filename_or_buffer, encoding=WIN_ENCODING)

    return pd.DataFrame()
