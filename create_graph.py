import json
import sys
import logging

import networkx as nx

logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler('graph.log', 'w'),
                                                   logging.StreamHandler(sys.stdout)])

TEMP_RESULTS_PATH = 'temp_result.json'
RESULT_GEPHI = 'gephi.gexf'
RESULT_CSV = 'result.csv'

def get_raw_data():
    with open(TEMP_RESULTS_PATH, 'r') as f:
        return json.load(f)


def main():
    raw_data = get_raw_data()

    graph = nx.Graph()
    already_added_nodes = set()

    total_count = len(raw_data)
    current_count = 1
    for user_key in raw_data:
        int_user_id = user_key
        graph.add_node(int_user_id, name=raw_data[user_key]['name'])

        for friend_id in raw_data[user_key]['friends']:
            if friend_id['id'] in already_added_nodes:
                continue
            graph.add_node(friend_id['id'], name=friend_id['name'])
            already_added_nodes.add(friend_id['id'])

        logging.info('added new edge. current progress %.2f', (current_count / total_count * 100))
        graph.add_edges_from([(int_user_id, friend_id['id']) for friend_id in raw_data[user_key]['friends']])
        current_count += 1

    save_as_gephi_format(graph)
    save_as_csv(graph)


def save_as_csv(G):
    nx.write_adjlist(G, RESULT_CSV)


def save_as_gephi_format(G):
    nx.write_gexf(G, RESULT_GEPHI)


if __name__ == '__main__':
    main()
