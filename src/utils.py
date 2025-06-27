import csv
import json
from io import StringIO


def load_parser_config_example() -> dict:
    with open("parser_config.json") as f:
        return json.load(f)

def generate_csv(headers: list[str], data: list[list]) -> str:
    """Сгенерировать .csv таблицу из заголовков и матрицы с данными"""
    output = StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(headers)

    for row in data:
        writer.writerow(row)

    output.seek(0)

    return output.getvalue()
