from ast import Tuple
import pprint
import csv
import re
import os
from typing import Optional

PHONE_PATTERN = re.compile(
    r"(?:\+7|8)\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})"
    r"(?:\s*(?:доб\.?)\s*(?P<ext>\d{2,5}))?",
    flags=re.IGNORECASE,
)


def normalize_phone(text: str) -> str:
    def _repl(m: re.Match) -> str:
        area = m.group(1)
        p1 = m.group(2)
        p2 = m.group(3)
        p3 = m.group(4)
        ext = m.group("ext")
        base = f"+7({area}){p1}-{p2}-{p3}"
        return f"{base} доб.{ext}" if ext else base

    return PHONE_PATTERN.sub(_repl, text)


with open(r"regular_expression\phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def process_name_fields(contract_row: list) -> list:
    all_names = []
    for field in contract_row[:3]:
        if field.strip():
            all_names.extend(field.split())

    all_names.extend([""] * (3 - len(all_names)))
    return all_names


def checking_duplicates(
    data_for_checking: list, checking_user: str
) -> Optional(Tuple(bool, int)):
    for pos, row_names in enumerate(data_for_checking[1:], 1):
        full_name = f"{row_names[0]}_{row_names[1]}"
        if full_name == checking_user:
            return (True, pos)
    return None


def combine_dossiers(processed_row: list, current_dossiers: list) -> None:
    for index, data in enumerate(processed_row, 0):
        if (data.strip() == "") and current_dossiers[index].strip():
            processed_row[index] = current_dossiers[index]


def contract_formater():
    formater_list = [contacts_list[0]]
    for contact_row in contacts_list[1:]:
        processed_row = process_name_fields(contact_row)
        processed_row.extend(contact_row[3:])

        if len(formater_list) > 1 and (
            res := checking_duplicates(
                formater_list, f"{processed_row[0]}_{processed_row[1]}"
            )
        ):
            _, position = res
            combine_dossiers(formater_list[position], processed_row)
            formater_list[position][5] = normalize_phone(formater_list[position][5])
        else:
            processed_row[5] = normalize_phone(processed_row[5])
            formater_list.append(processed_row)

    return formater_list


def main() -> None:
    data = contract_formater()

    script_dir = os.path.dirname(__file__)
    output_path = os.path.join(script_dir, "phonebook.csv")

    with open(output_path, "w", encoding="utf-8") as f:
        datawrite = csv.writer(f, delimiter=",")
        datawrite.writerows(data)


if __name__ == "__main__":
    main()
