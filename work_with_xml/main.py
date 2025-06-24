import xml.etree.ElementTree as ET


def read_xml(file_path, word_min_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    # Ваш алгоритм

    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(file_path, parser)
    root = tree.getroot()

    texts = [item.find("description").text for item in root.findall("channel/item")]

    result = dict()

    for text in texts:
        for word in text.split():
            if len(word) > word_min_len:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1

    return sorted(result.keys(), key=lambda x: result[x], reverse=True)[:top_words_amt]


if __name__ == "__main__":
    print(read_xml(r"work_with_xml\text.xml"))
