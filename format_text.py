import re
import yaml

from pathlib import Path

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def get_sub_sections(work_text):
    sub_sections = {}
    work_parts = re.split(r'(<.+>)', work_text)
    for work_part in work_parts[1:]:
        if "<" in work_part:
            sub_section_name = work_part[1:-1].strip()
        else:
            sub_sections[sub_section_name] = work_part.strip()
    return sub_sections

def get_pedurma_text_info(text_title, text_id_title_mapping):
    for pedurma_title, text_id in text_id_title_mapping.items():
        if text_title.strip() == pedurma_title:
            return text_id, pedurma_title
    return "", ""

def get_text_detail(text_title, text_id_title_mapping):
    text_detail = {
        'title': text_title.strip(),
        'Id': None,
        'pedurma_title': None
    }
    id, pedurma_title = get_pedurma_text_info(text_title, text_id_title_mapping)
    text_detail['Id'] = id
    text_detail['pedurma_title'] = pedurma_title
    return text_detail

def parse_text(sub_section_text, text_id_title_mapping):
    text_list = {}
    texts = sub_section_text.splitlines()
    for text_num, text in enumerate(texts,1):
        text_title = re.sub('\d+', "", text)
        text_title = text_title.replace('\n',"")
        text_list[text_num] = get_text_detail(text_title, text_id_title_mapping)
    return text_list

def parse_works(work_text, text_id_title_mapping):
    works = {}
    sub_sections = get_sub_sections(work_text)
    for sub_section_name, sub_section_text in sub_sections.items():
        works[sub_section_name] = parse_text(sub_section_text, text_id_title_mapping)
    return works

if __name__ == "__main__":
    work_text = Path('./data/nalanda_work/སློབ་དཔོན་ཀླུ་སྒྲུབ་ཀྱི་གསུང་གི་མཚན་བྱང་།.txt').read_text(encoding='utf-8')
    text_id_title_mapping = from_yaml(Path('./data/text_Id_title_mapping.yml'))
    works = parse_works(work_text,text_id_title_mapping )

    works_yaml = to_yaml(works)
    Path('./data/nalanda_work_yaml/lodrup_work.yml').write_text(works_yaml, encoding='utf-8')