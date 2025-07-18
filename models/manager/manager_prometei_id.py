from models.manager.prometei_id import PrometeiId


class ManagerPrometeiId:

    def __init__(self):
        self._counters = {
            "contacts": 0,
            "notes": 0
        }
        self._free_indices ={
            "contacts": set(),
            "notes": set()
        }

    def get_new_id(self, category: str) -> PrometeiId:
        self._counters[category] += 1
        if len(self._free_indices[category]) > 0:
            promid = self._free_indices[category].pop()
            return PrometeiId(promid)
        else:
            return PrometeiId(self._counters[category])

    def delete_item(self, category: str, prid: int):
        self._counters[category] -= 1
        self._free_indices[category].add(prid)




