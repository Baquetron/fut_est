import csv
import pandas
import numpy

PATH_TRANSFER_HISTORY = "../data/transfer_history.csv"
def table_cleaner(dir):
    p_transfer_table = pandas.read_csv(filepath_or_buffer=dir, index_col= 0)
    # enumerate members
    list_members = list(pandas.unique(p_transfer_table['Buyer']))
    members_t = {}
    for i, name in enumerate(list_members):
        members_t[name] = i
    # save csv table
    pandas.DataFrame.from_dict(members_t, orient='index', columns=['id']).reset_index(level=0).to_csv("../data/members_enum.csv", index=False)
    # apply to table
    p_transfer_table['Seller'] = p_transfer_table['Seller'].apply(lambda x: str(members_t[x]))
    p_transfer_table['Buyer'] = p_transfer_table['Buyer'].apply(lambda x: str(members_t[x]))
    # clean columns
    p_transfer_table.reset_index(level=0 ,inplace=True)
    p_transfer_table['Date'] = p_transfer_table['Transfer Time'].apply(lambda x: x.split(' ')[0])
    p_transfer_table['Time'] = p_transfer_table['Transfer Time'].apply(lambda x: x.split(' ')[2])
    p_transfer_table['Transfer'] = p_transfer_table['Transfer amount'].apply(lambda x: int(x.replace('.','').split(' ')[0]))
    p_transfer_table.drop(columns=['Transfer Time','Transfer amount'], inplace=True)

    print(p_transfer_table)
    p_transfer_table.to_csv("../data/transfer_history_clean.csv", index=False)


if __name__ == "__main__":
    table_cleaner(PATH_TRANSFER_HISTORY)