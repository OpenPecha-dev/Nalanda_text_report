import csv

import re

from pathlib import Path

from format_text import from_yaml


def get_sections(section):
    sections = []
    for id, section_info in section.items():
        cur_section = ['', section_info['Id'], section_info['title'],  '', '', '']
        sections.append(cur_section)
    return sections


def make_report(works, philo):
    output_path =f"./data/nalanda_work_xcel/{philo}.xlsx"
    header = [" Section", "Text Id", "Text Title", "Note proofread", "Pedurma dip", "Proofread Base"]
    with open(output_path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for section_name, section in works.items():
            writer.writerow([section_name, '', '', '', '', ''])
            sections = get_sections(section)
            writer.writerows(sections)


if __name__ == "__main__":
    philo_work_paths = list(Path('./data/nalanda_work_yaml').iterdir())
    philo_work_paths.sort()
    for philo_work_path in philo_work_paths:
        philo_name = philo_work_path.stem
        philo_work = from_yaml(philo_work_path)
        make_report(philo_work, philo_name)



