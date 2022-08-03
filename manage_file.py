import requests
import pandas as pd


def insert_excel_data(path):
    data = pd.read_excel(path)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_excel_pipe_settings(path):
    data = pd.read_excel(path)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_csv_data(path):
    data = pd.read_csv(path, encoding='unicode_escape')
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_excel_pipe_settings_from_cloud(path):
    response = requests.get(path)
    local_pipe_settings = 'pipe_settings.xlsx'
    with open(local_pipe_settings, 'wb') as file:
        file.write(response.content)
    data = pd.read_excel(local_pipe_settings)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_csv_pipe_settings(path):
    data = pd.read_csv(path, encoding='unicode_escape')
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df

