from pathlib import Path

import re
import yaml

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def get_pedurma_title(text_id, outline):
    text_title = ''
    for _, text in outline.items():
        if text['rkts_id'] == text_id:
            text_title = f"{text['pedurma_title']} {text['text_title']}"
    return text_title

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(r"([0-9]+\-[0-9]+)", vol_text)
    for i, page in enumerate(pages[0:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result


def get_title_in_text(text_path):
    title = ''
    text= text_path.read_text(encoding="utf-8")
    pages = get_pages(text)
    first_page = pages[0]
    first_page = first_page.replace("\n", "")
    if re.search("༄(.+?)༄", first_page):
        title = re.search("༄(.+?)༄", first_page).group(1)
        title = re.sub('\(\d+\) <.+?>', "", title)
    return title

def get_collated_text_titles():
    collated_text_titles = {}
    pedurma_outline = from_yaml(Path('./data/pedurma_outline.yml'))
    collated_text_paths = list(Path('./data/collated_text/').iterdir())
    collated_text_paths.sort()
    for collated_text_path in collated_text_paths:
        text_id = collated_text_path.stem[:-5]
        cur_text = {
            "pedurma_title": "",
            "title_in_text": ""
        }
        cur_text['pedurma_title'] = get_pedurma_title(text_id, pedurma_outline)
        cur_text['title_in_text'] = get_title_in_text(collated_text_path)
        collated_text_titles[text_id] = cur_text

    return collated_text_titles


if __name__ == "__main__":
    collated_text_titles = get_collated_text_titles()
    Path('./collated_text_titles.yml').write_text(to_yaml(collated_text_titles), encoding='utf-8')