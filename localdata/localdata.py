import json
import logging
from typing import Optional, List, Dict


class LocalData:

    def __init__(self, local_data='crypex/localdata/localdata.json'):
        self.local_data: str = local_data
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.info('Loaded LocalData object.')

    def get(self, key):
        """Deep search local data for a key's value.

            Parameters
            ----------
                key: (str)
                    The key to search for.

            Return Type
            -----------
                List[str]
        """
        res: List[str] = []

        def _get_results(_d: dict) -> List[str]:
            try:
                res.append(str(_d[key]))
            except KeyError:
                pass

        with open(self.local_data, mode='r+') as file:
            json.load(file, object_hook=_get_results)

        return res

    def add(self, _d, add_to=None):
        """Add a new JSON object to local data.

            Parameters
            ----------
                add_to: (Optional[str])
                    The name of the key to add _d too. Must be a first-level key.
                _d: (dict)
                    Python dictionary containing unsterilized JSON objects.
        """
        with open(self.local_data, mode='r+') as file:
            data: Dict[str] = json.load(file)
            try:
                if add_to:
                    data[add_to].update(_d)
                else:
                    data.update(_d)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
            except KeyError:  # If add_to does not exist, create it.
                data[add_to] = {}
                data[add_to].update(_d)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
            except Exception as other_excep:
                raise Exception(other_excep)

    def edit(self, key, new_value, delete=False):
        """Edit a key from the local data.

            Parameters
            ----------
                key: (str)
                    The key to edit, or delete.
                new_value: (str)
                    The new value of the key.
                delete: (bool)
                    Whether to delete or edit the key.
        """
        key_exists: List[str] = self.get(key)
        if key_exists:
            with open(self.local_data, mode='r+') as file:
                data: Dict[str] = json.load(file)

                def nested_recursion(_d: dict) -> None:
                    for k, v in _d.items():
                        if isinstance(v, dict):
                            nested_recursion(v)
                        else:
                            if k == key:
                                if delete:
                                    del _d[key]
                                else:
                                    _d[key] = new_value

                nested_recursion(data)
                data.update(data)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=True)
        else:
            raise KeyError(f'Local data has no key named {key}.')
