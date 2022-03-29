import re
import yaml
from fuzzy_match import algorithims

from pathlib import Path

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def preprocess_title(title):
    initials = ['དཔལ་', 'འཕགས་པ་']
    for initial in initials:
        title = title.replace(initial, '')
    return title

def get_similarity(title1, title2):
    title1 = preprocess_title(title1)
    title2 = preprocess_title(title2)
    similarity = algorithims.cosine(title1,title2)
    return similarity

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
        if get_similarity(text_title.strip(),pedurma_title) >= 0.97:
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
    text_id_title_mapping = from_yaml(Path('./data/text_Id_title_mapping.yml'))
    philo_work_paths = list(Path('./data/nalanda_work').iterdir())
    philo_work_paths.sort()
    for philo_work_path in philo_work_paths:
        philo_name = philo_work_path.stem
        philo_work_text = philo_work_path.read_text(encoding='utf-8')
        works = parse_works(philo_work_text,text_id_title_mapping )

        works_yaml = to_yaml(works)
        Path(f'./data/nalanda_work_yaml/{philo_name}.yml').write_text(works_yaml, encoding='utf-8')