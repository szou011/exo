import os
import shutil
import configparser

from .clarity_export_config import AU_CLARITY_REPORT_PATH, NZ_CLARITY_REPORT_PATH


def update_cls(template_file_path, country, params):
    template_config = configparser.ConfigParser()
    template_config.read(template_file_path)

    target_config = configparser.ConfigParser()

    for param in params:
        if template_config.has_section(param):
            target_config.add_section(param)

            for key, item in template_config[param].items():
                target_config[param][key] = item

    if country == "NZ":
        clarity_report_path = NZ_CLARITY_REPORT_PATH
    elif country == "AU":
        clarity_report_path = AU_CLARITY_REPORT_PATH

    with open(
        clarity_report_path + os.path.basename(template_file_path), "w"
    ) as new_configfile:
        target_config.write(new_configfile)

    return None


def delete_cls(template_file_path, country):

    if country == "NZ":
        clarity_report_path = NZ_CLARITY_REPORT_PATH
    elif country == "AU":
        clarity_report_path = AU_CLARITY_REPORT_PATH

    os.remove(clarity_report_path + os.path.basename(template_file_path))

    return None


def copy_clr(template_file_path, country):

    if country == "NZ":
        clarity_report_path = NZ_CLARITY_REPORT_PATH
    elif country == "AU":
        clarity_report_path = AU_CLARITY_REPORT_PATH

    shutil.copyfile(
        template_file_path, clarity_report_path + os.path.basename(template_file_path)
    )

    return None


def delete_clr(template_file_path, country):

    if country == "NZ":
        clarity_report_path = NZ_CLARITY_REPORT_PATH
    elif country == "AU":
        clarity_report_path = AU_CLARITY_REPORT_PATH

    os.remove(clarity_report_path + os.path.basename(template_file_path))

    return None


def parse_clr_header(clr_file_path):
    """Read clr header as per the DataFiled name property and order by mmLeft property"""
    
    header_order= {}
    
    with open(clr_file_path, 'r') as clr_file:
        for line in clr_file:
            if 'DataField' in line:
                current_header = line[19:-2]
            elif 'mmLeft' in line:
                header_order[current_header] = int(line[15:-1])
                
    header = [k for k, _ in sorted(header_order.items(), key=lambda item: item[1])]

    return header