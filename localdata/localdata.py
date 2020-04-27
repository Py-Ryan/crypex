import json
from logging import getLogger
from typing import List, Dict, Any


class LocalData:

    def __init__(self, local_data='crypex/localdata/localdata.json'):
        self.local_data = local_data
        self.logger = getLogger(__name__)
        self.logger.info('Loaded LocalData object.')

    def get(self, key):
        res: List[Any] = list()

        def get_results(dictionary: Dict[str, Any]) -> None:
            try:
                res.append(str(dictionary[key]))
            except KeyError:
                pass

        with open(self.local_data, mode='r+') as file:
            json.load(file, object_hook=get_results)

        return res

    def add(self, dictionary, add_to=None):
        with open(self.local_data, mode='r+') as file:
            data: Dict[str, Any] = json.load(file)
            try:
                if add_to:
                    data[add_to].update(dictionary)
                else:
                    data.update(dictionary)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
            except KeyError:  # If add_to does not exist, create it.
                data[add_to]: Dict[str, Any] = {}
                data[add_to].update(dictionary)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
            except Exception as msg:
                raise Exception(msg)

    def edit(self, key, new_value, delete=False):
        key_exists: List[str] = self.get(key)
        if key_exists:
            with open(self.local_data, mode='r+') as file:
                data: Dict[str, Any] = json.load(file)

                def nested_recursion(dictionary: dict) -> None:
                    for k, v in dictionary.items():
                        if isinstance(v, dict):
                            nested_recursion(v)
                        else:
                            if k == key:
                                if delete:
                                    del dictionary[key]
                                else:
                                    dictionary[key] = new_value

                nested_recursion(data)
                data.update(data)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
        else:
            raise KeyError(f'Local data has no key named {key}.')
