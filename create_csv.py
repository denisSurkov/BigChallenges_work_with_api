

def get_base_dict(raw_data: dict):
    total_set = set()

    for key in raw_data:
        total_set.add(key)
        total_set.update([i['id'] for i in raw_data[key]['friends']])

    return {key: set() for key in total_set}
