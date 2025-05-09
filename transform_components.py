def dropna(df, subset=None):
    return df.dropna(subset=subset)

def lowercase_column(df, column):
    df[column] = df[column].str.lower()
    return df

def rename_column(df, old_name, new_name):
    return df.rename(columns={old_name: new_name})

def fillna(df, column, value):
    df[column] = df[column].fillna(value)
    return df

def filter_rows(df, query):
    return df.query(query) 