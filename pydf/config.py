import json


class Config:
    def __init__(self, store_dir: str, with_watermark: bool):
        self.store_dir = store_dir
        self.with_watermark = with_watermark

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, path: str):
        with open(path) as f:
            loaded = json.load(f)
            return cls(
                store_dir=loaded.get('store_dir', 'store'),
                with_watermark=loaded.get('with_watermark', False)
            )
