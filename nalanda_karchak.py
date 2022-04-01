import csv
import re
import yaml
from fuzzy_match import algorithims

from pathlib import Path

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def preprocess_title(title):
    title = title.strip()
    noises = ['\(.+?\)', '༼.+?༽', '\d+', '\n']
    for noise in noises:
        title = re.sub(noise, '', title)
    title = re.sub("པའམ.+", "", title)
    return title

def get_similarity(title1, title2):
    similarity = algorithims.cosine(title1,title2)
    return similarity

def get_text_id(text_title, text_title_id_mapping):
    text_id = ""
    std_title = ""
    max_similarity = 0
    text_title = preprocess_title(text_title)
    for _, text_info in text_title_id_mapping.items():
        if get_similarity(text_title, text_info['title']) > 0.9 and get_similarity(text_title, text_info['title']) > max_similarity:
            text_id = text_info['work_id']
            std_title = text_info['title']
            max_similarity = get_similarity(text_title, text_info['title'])
    return [text_id, std_title]
        

def put_sec_texts(pandita_code, sec_texts, sec_code, nalanda_karchak):
    text_title_id_mapping = from_yaml(Path('./data/nalanda_text_title_id_mapping.yml'))
    text_titles = sec_texts.splitlines()
    for text_code, text_title in enumerate(text_titles, 1):
        if text_title:
            cur_text = []
            text_id, std_title = get_text_id(text_title, text_title_id_mapping)
            text_code = f"{int(pandita_code):02}-{int(sec_code):02}-{int(text_code):02}-"
            cur_text.append(text_id)
            cur_text.append(text_code)
            cur_text.append(text_title)
            cur_text.append(std_title)
            nalanda_karchak.append(cur_text)
    return nalanda_karchak


def get_sub_sections(work_text):
    sub_sections = {}
    work_parts = re.split(r'(<.+>)', work_text)
    for work_part in work_parts[1:]:
        if "<" in work_part:
            sub_section_name = work_part[1:-1].strip()
        else:
            sub_sections[sub_section_name] = work_part.strip()
    return sub_sections

def parse_works(pandita_code, work_text, nalanda_karchak):
    sub_sections = get_sub_sections(work_text)
    for sec_code, (sec_name, sec_texts) in enumerate(sub_sections.items(),1):
        nalanda_karchak = put_sec_texts(pandita_code, sec_texts, sec_code, nalanda_karchak)
    return nalanda_karchak

def get_nalanda_karchak():
    nalanda_karchak = []
    nalanda_pandita_paths = list(Path('./data/nalanda_work').iterdir())
    nalanda_pandita_paths.sort()
    for pan_code, nalanda_pandita_path in enumerate(nalanda_pandita_paths,1):
        pandita_works = nalanda_pandita_path.read_text(encoding='utf-8')
        nalanda_karchak = parse_works(pan_code, pandita_works, nalanda_karchak)
    return nalanda_karchak


if __name__ == "__main__":
    output_path =f"./data/nalanda_karchak.xlsx"
    header = ["Text Id", "Text Code", "Text Title(TY)", "Text Title(ESU)",]
    with open(output_path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        nalanda_karchak = get_nalanda_karchak()
        writer.writerows(nalanda_karchak)
