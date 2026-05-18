      
import json
import os

DATA_FILE_PATH = "data/inquiries.json"


def load_all() -> list:
    """JSONファイルから全件読み込む。ファイルが存在しない場合は空リストを返す。"""
    if not os.path.exists(DATA_FILE_PATH):
        return []
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_all(records: list) -> None:
    """全件をJSONファイルに上書き保存する。dataフォルダがなければ作成する。"""
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def find_by_id(inquiry_id: int) -> dict | None:
    """指定IDのレコードを返す。存在しない場合はNoneを返す。"""
    records = load_all()
    for record in records:
        if record["id"] == inquiry_id:
            return record
    return None
