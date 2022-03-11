import os
import shutil
import configparser

from dotenv import dotenv_values
config = dotenv_values()

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
        clarity_report_path = config['NZ_CLARITY_REPORT_PATH']
    elif country == "AU":
        clarity_report_path = config['AU_CLARITY_REPORT_PATH']

    with open(
        clarity_report_path + os.path.basename(template_file_path), "w"
    ) as new_configfile:
        target_config.write(new_configfile)

    return None


def delete_cls(template_file_path, country):

    if country == "NZ":
        clarity_report_path = config['NZ_CLARITY_REPORT_PATH']
    elif country == "AU":
        clarity_report_path = config['AU_CLARITY_REPORT_PATH']

    os.remove(clarity_report_path + os.path.basename(template_file_path))

    return None


def copy_clr(template_file_path, country):

    if country == "NZ":
        clarity_report_path = config['NZ_CLARITY_REPORT_PATH']
    elif country == "AU":
        clarity_report_path = config['AU_CLARITY_REPORT_PATH']

    shutil.copyfile(
        template_file_path, clarity_report_path + os.path.basename(template_file_path)
    )

    return None


def delete_clr(template_file_path, country):

    if country == "NZ":
        clarity_report_path = config['NZ_CLARITY_REPORT_PATH']
    elif country == "AU":
        clarity_report_path = config['AU_CLARITY_REPORT_PATH']

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

def append_csv_header(csv_file_path, header):
    
    with open(csv_file_path, 'r', newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
    with open('file.csv','w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['ColA','ColB'])
        w.writerows(data)