import re
import numpy as np
import io
import json
import plotly


try:
    open_file = open('//Users/jbd/PycharmProjects/dataset/data/voting_data_eng.csv','r+',encoding='ISO-8859-1')
    keys = tuple(open_file.readline().strip().split(','))
    keys = [key.title() for key in keys]

    df = open_file.read().splitlines()


except EOFError as fille_open_error:
    print("Check filepath or file: ", fille_open_error)

finally:
    open_file.close()


def get_region(s,i):
    st = re.split(r',', s, maxsplit=i+1)
    st = st[i]

    return st


def candidat_name(keys):
    names = []
    for key in keys:
        try:
            st = re.search(r'^((\w+)\s(\w+)\s(\w+))$', key).group(0)
            if st is not None:
                names.append(st)
        except:
            continue
    names.append('Number Of Valid Ballot Papers')

    return names


def get_votes(row, index_candidats):
    ls = re.split(r',', row)
    ls = ls[min(index_candidats):]
    return ls

candidat_names = candidat_name(keys)


def read_data():
    """
    Baburin Sergei Nikolaevich,
    Grudinin Pavel Nikolaevich,
    Zhirinovskiy Vladimir Volfovich,
    Putin Vladimir Vladimirovich,
    Sobchak Ksenia Anatolyevna,
    Suraikin Maksim Aleksandrovich,
    Titov Boris Yurievich,
    Yavlinskiy Gregory Alekseivich
    """

    data_set = {key: {} for key in candidat_names}
    index_candidats = [keys.index(key) for key in candidat_names]
    for i in range(len(df)):
        row = df[i].rstrip()
        if not row:
            print("emplty row: ", i)
            continue
        region = get_region(row, list(keys).index('Region_Name'))
        city = get_region(row, list(keys).index('Subregion_Name'))
        votes = get_votes(row, index_candidats)

        for key, item in data_set.items():
            if region in list(item.keys()):
                try:
                    data_set[key][region][city] += int(votes[candidat_names.index(key)])
                except:
                    data_set[key][region][city] = int(votes[candidat_names.index(key)])
            else:
                data_set[key][region] = {
                    city:int(votes[candidat_names.index(key)])
                }

    return data_set


def dataset_to_json(data_):
    with io.open('data_.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_, ensure_ascii=False))


def quant_voice(data):

    quantity = {}
    for kand,regs in data.items():
        quantity[kand] = sum(sum(q.values()) for q in regs.values())

    return quantity


def graph_show(scatter_,bar_,pie_,pie2):

    figure = {"data": [
        {
            "x": np.array(list(scatter_.keys())),
            "y": np.array(list(scatter_.values())),
            "type": "scatter",


        },
        {
            "x": np.array(list(bar_.keys())),
            "y": np.array(list(bar_.values())),
            "type": "bar",
            "xaxis": "x2",
            "yaxis": "y2"

        },
        {
            "labels": np.array(list(pie_.keys())),
            "values": np.array(list(pie_.values())),
            "type": "pie",
            "name": "P2",
            'domain': {'x': [0, 0.45], 'y': [0.55, 1]},
        },
        {
            "labels": np.array(list(pie2.keys())),
            "values": np.array(list(pie2.values())),
            "type": "pie",
            "name": "P3",
            'domain': {'x': [0.55, 1], 'y': [0.55, 1]},
        }
    ],
        "layout":
            {'xaxis': {'domain': [0, 0.45]},
             'xaxis2': {'domain': [0.55, 1]},
             'yaxis': {'domain': [0, 0.45]},
             'yaxis2': {'anchor': 'x2', 'domain': [0, 0.45]}
             }
    }
    plotly.offline.plot(figure, filename="plot.html")


if __name__ == '__main__':

    data_s_ = read_data()

    city_of_region = {k:len(list(v)) for k,v in data_s_[list(data_s_.keys())[0]].items()}

    quant_voices = quant_voice(data_s_)

    quant_voices_pie = quant_voices.copy()
    quant_voices_pie['Not voice total'] = sum(quant_voices_pie.values())-2*(quant_voices_pie['Number Of Valid Ballot Papers'])

    del quant_voices_pie['Number Of Valid Ballot Papers']

    quant_voices_ =quant_voices.copy()
    del quant_voices_['Number Of Valid Ballot Papers']

    graph_show(city_of_region,quant_voices,quant_voices_pie,quant_voices_)


