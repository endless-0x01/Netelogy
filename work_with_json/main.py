import json


def read_json(file_path, word_min_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    with open(file_path, encoding="utf-8") as f:
        json_data = json.load(f)

    text = [item["description"] for item in json_data["rss"]["channel"]["items"]]

    result = dict()
    for words in text:
        for word in words.split():
            if len(word) > word_min_len:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

    sorted_keys = sorted(result.keys(), key=lambda x: result[x], reverse=True)
    return sorted_keys[:top_words_amt]


def main():
    result = read_json(r"work_with_json\text.json")
    print(result)


if __name__ == "__main__":
    main()
