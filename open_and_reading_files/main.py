import os


def line_counting(data: str):
    return data.count("\n")


def parese():
    files_data = dict()
    for i in range(1, 4):
        name_file = f"{i}.txt"
        file_path = os.path.join(os.getcwd(), "open_and_reading_files", name_file)
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        lines = line_counting(data) + 1
        files_data[name_file] = {
            "path": file_path,
            "line_counting": lines,
            "file_number": i,
            "proprietary_information": [
                f"Строка номер {index} файла номер {i}" for index in range(1, lines + 1)
            ],
        }

    return files_data


def write_data(data: dict):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]["line_counting"]))

    for name_file, info in sorted_data.items():
        rd_inf = (
            f"{name_file}\n"
            f"{info['line_counting']}\n"
            f'{'\n'.join(info['proprietary_information'])} \n\n'
        )

        with open("service_information", "a", encoding="utf-8") as file:
            file.write(rd_inf)


def main():
    data_for_write = parese()
    write_data(data_for_write)


if __name__ == "__main__":
    main()
