from locale import normalize
import re

from format_text import from_yaml, to_yaml
from pathlib import Path

PANTIDAS = [
    "ཀླུ་སྒྲུབ",
    "འཕགས་པ་ལྷ",
    "སངས་རྒྱས་བསྐྱངས",
    "ལེགས་ལྡན་འབྱེད",
    "ཟླ་བ་གྲགས་པ",
    "ཐོགས་མེད",
    "དབྱིག་གཉེན",
    "ཕྱོགས་གླང་",
    "ཡོན་ཏན་འོད",
    "ཤཱཀྱ་འོད",
    "ཆོས་གྲགས",
    "ཞི་བ་འཚོ",
    "སེང་གེ་བཟང་པོ",
    "ཞི་བ་ལྷ",
    "པདྨའི་ངང་ཚུལ",
    "ཨ་ཏི་ཤ",
    "མར་མེ་མཛད"
]

def get_clean_text(collated_text):
    clean_collated_text = collated_text
    noises = ["\n", ":", "\(\d+\) <.+?>", "\d+-\d+"]
    for noise in noises:
        clean_collated_text = re.sub(noise, "", clean_collated_text)
    return clean_collated_text

def get_clean_author_text(author):
    clean_author_text = author
    noises = ["མཛད་པ་", "ཞེས་བྱ་བ", "ཀྱི་ཞལ་སྔ་ནས་", "ཀྱིས་", "གྱིས་", "ཞབས་ལས་བྱུང་བ་", "ཞལ་སྔ་ནས་\S+", "མཛད་པའི་\S+"]
    for noise in noises:
        clean_author_text = re.sub(noise, "", clean_author_text)
    return clean_author_text

def get_normalize_author(author):
    normalize_author = author
    for padita in PANTIDAS:
        if padita in author:
            normalize_author = padita
    return normalize_author

def parse_author(collated_text):
    author = ""
    clean_text = get_clean_text(collated_text)
    if re.search("(སློབ་དཔོན་\S+)རྫོགས་", clean_text):
        author = re.search("(སློབ་དཔོན་\S+)རྫོགས་", clean_text).group(1)
        author = get_clean_author_text(author)
        author = get_normalize_author(author)
    return author


if __name__ == "__main__":
    text_author_mapping = {}
    text_with_ending_issue = []
    collated_text_paths = list(Path('./data/collated_text').iterdir())
    collated_text_paths.sort()
    for collated_text_path in collated_text_paths:
        collated_text = collated_text_path.read_text(encoding='utf-8')
        author = parse_author(collated_text)
        if not author:
            text_with_ending_issue.append(text_id)
        text_id = collated_text_path.stem[:-5]
        text_author_mapping[text_id] = author
    Path('./text_author_mapping.yml').write_text(to_yaml(text_author_mapping), encoding='utf-8')
    Path('./text_with_ending_issue.txt').write_text("\n".join(text_with_ending_issue), encoding='utf-8')
    


    