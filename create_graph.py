import json
import sys
import logging

import networkx as nx

logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler('graph.log', 'w'),
                                                   logging.StreamHandler(sys.stdout)])

TEMP_RESULTS_PATH = 'temp_result.json'
RESULT_GEPHI = 'gephi.gexf'
RESULT_CSV = 'result.csv'


def get_raw_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def main():
    raw_data = get_raw_data(TEMP_RESULTS_PATH)

    graph = nx.Graph()

    already_added = set()
    total_count = len(raw_data)
    current_count = 1
    for user_key in raw_data:
        int_user_id = int(user_key)
        graph.add_node(int_user_id, label=raw_data[user_key]['name'], name=raw_data[user_key]['name'])
        already_added.add(int_user_id)

        for friend_id in raw_data[user_key]['friends']:
            if friend_id['id'] in already_added:
                continue
            graph.add_node(friend_id['id'], label=friend_id['name'], name=friend_id['name'])
            graph.add_edge(int_user_id, friend_id['id'])

        logging.info('added new edge. current progress %.2f', (current_count / total_count * 100))
        current_count += 1

    save_as_gephi_format(graph, RESULT_GEPHI)
    save_as_csv(graph, RESULT_CSV)


def save_as_csv(G, path):
    nx.write_adjlist(G, path)


def save_as_gephi_format(G, path):
    nx.write_gexf(G, path)


if __name__ == '__main__':
    main()
