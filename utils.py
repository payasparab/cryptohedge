
def convert_pd_to_unix(pd_timestamp):
    # https://stackoverflow.com/questions/54313463/pandas-datetime-to-unix-timestamp-seconds
    import pandas as pd
    return (pd_timestamp - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')