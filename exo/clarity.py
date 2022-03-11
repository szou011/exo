"""MYOB EXO Data Export

This module allows the user to extract date indirectly from Myob EXO database (usually a MS SQL database) using EXO's own clarity module.

Instead of connecting to the MS SQL server direclty, EXO allows user to build SQL query through its clarity.exe command line tool and save data into files that can be used later.

A simple clarity command line could be like:
Clarity.exe EXONET_DEMO ExoAdmin ExoAdmin MyReport.clr /d=File /f=c:\test.pdf /m=PDFFile

The command line parameters can be found:
https://help.myob.com.au/exo/help/exo2020/mergedProjects/myob%20exo%20clarity/desktop/Available_Parameters.htm

"""

import os
from datetime import datetime
import logging

from dotenv import dotenv_values
config = dotenv_values()


from exo.cls import update_cls, delete_cls, copy_clr, delete_clr, parse_clr_header
from exo.fileprocess import append_csv_header

logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


class ExoReport:
    """Initiate an ExoReport object that generate csv file from the corresponding Exo database table"""
    
    # define default clarity output format - text file
    EXO_EXPORT_TYPE = "/d=File"
    EXO_EXPORT_FILE_MODE = "/m=TextFile"
    EXO_NO_ASK_PARAM = "/a=N"
    EXO_NO_SPLASH_SCREEN = "/l=N"

    def __init__(self, country, params, report_type):

        self.country = country
        self.params = params
        self.report_type = report_type
        self.clarity_report_clr_file = self.report_type + ".clr"

        # validate country input
        if country == "NZ":
            self.exo_alias_name = config['EXO_NZ_ALIAS_NAME']
        elif country == "AU":
            self.exo_alias_name = config['EXO_AU_ALIAS_NAME']
        else:
            raise ValueError(
                "No such country has been defined, please use NZ for New Zealand or AU for Australia."
            )

        self.csv_file_name = None

    @property
    def exo_report_file_name(self):
        """ Return the csv report file name when the clarifty command executes """
        
        time_now = datetime.now()
        datetime_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
        return datetime_string + "_" + self.country + "_" + self.report_type + ".csv"

    @property
    def flatten_params(self):
        """flatten dictionary params to a string

        If the parameter is a set of values then you must enclose the set with parenthesis eg.
        /s=Param1=3,{Param2=86,99,55}

        """

        if not self.params:
            return ""

        params_list = []

        assert isinstance(self.params, dict)
        for key, value in self.params.items():
            if isinstance(value, list):
                if isinstance(value[0], str):
                    params_list.append(
                        "{"
                        + key
                        + "="
                        + ",".join(['"' + str(elem) + '"' for elem in value])
                        + "}"
                    )
                elif isinstance(value[0], int):
                    params_list.append(
                        "{" + key + "=" + ",".join([str(elem) for elem in value]) + "}"
                    )
            elif isinstance(value, str):
                params_list.append(key + '="' + str(value) + '"')
            elif isinstance(value, int):
                params_list.append(key + "=" + str(value))

        return "/s=" + ",".join(params_list)

    @property
    def command_line(self):
        """ construct the command line string """

        self.csv_file_name = self.exo_report_file_name

        export_file_name_param = "/f=" + config['EXO_EXPORT_FILE_PATH'] + self.csv_file_name

        return " ".join(
            [
                config['CLARITY_EXE_PATH'] + "clarity.exe",
                self.exo_alias_name,  # first param
                config['EXO_USER_NAME'],  # second param
                config['EXO_PASSWORD'],  # third param
                self.clarity_report_clr_file,
                self.EXO_EXPORT_TYPE,
                self.EXO_EXPORT_FILE_MODE,
                self.EXO_NO_ASK_PARAM,
                self.EXO_NO_SPLASH_SCREEN,
                export_file_name_param,
                self.flatten_params,
            ]
        )

    
    @property
    def clr_header(self):
        return parse_clr_header(config['EXO_CLS_TEMPLATE_PATH'] + self.clarity_report_clr_file)

    def _export_csv(self):
        """ save the clarity exported csv file when the cmd is excuted.
        NOTE: the csv file has no header. """

        # preparation by copying clr and cls files into exo folder
        cls_file = None

        if self.params:
            cls_file = config['EXO_CLS_TEMPLATE_PATH'] + self.clarity_report_clr_file[:-1] + "s"

            logging.info("Updating cls file...")
            update_cls(
                cls_file,
                self.country,
                self.params,
            )

        logging.info("Updating clr file...")
        copy_clr(config['EXO_CLS_TEMPLATE_PATH'] + self.clarity_report_clr_file, self.country)

        logging.info("Executing clarity report...")
        logging.debug(f"Executing {self.command_line}")
        os.system(self.command_line)

        
        if cls_file:
            delete_cls(cls_file, self.country)
            logging.info(f"{os.path.basename(cls_file)} was deleted.")

        delete_clr(config['EXO_CLS_TEMPLATE_PATH'] + self.clarity_report_clr_file, self.country)
        logging.info(f"{self.clarity_report_clr_file} was deleted.")
        
        return None
    
    def save_csv(self):
        
        self._export_csv()
        
        append_csv_header(config['EXO_EXPORT_FILE_PATH'] + self.csv_file_name, self.clr_header)
        logging.info(f"{self.csv_file_name} was saved in {config['EXO_EXPORT_FILE_PATH']}.")

        return None