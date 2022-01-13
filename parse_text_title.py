from pathlib import Path


from format_text import from_yaml, to_yaml

def parse_text_title(pedurma_text_title):
    text_title = {}
    for text_info in pedurma_text_title:
        text_title[text_info[2]] = text_info[1]
    return text_title


if __name__ == "__main__":
    pedurma_text_title = from_yaml(Path('./pedurma_text_titles.yml'))
    text_title = parse_text_title(pedurma_text_title)
    Path('./text_Id_title_mapping.yml').write_text(to_yaml(text_title), encoding='utf-8')