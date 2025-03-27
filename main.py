import re
import csv
import os
import dotenv
from pprint import pprint


class OpenDataFix:
    def __init__(self, source_file_path: str, result_file_path: str, config_path: str = None):
        if config_path:
            dotenv_path = config_path
        else:
            dotenv_path = os.path.join(os.getcwd(), '.env')
        dotenv.load_dotenv(dotenv_path)
        self.pattern = os.getenv('PATTERN')
        self.substitution = os.getenv('SUBSTITUTION')
        self.source_file_path = source_file_path
        self.result_file_path = result_file_path

    def fix_data(self):
        self._get_rows_list()
        self._fix_names()
        self._fix_phones()
        self._fix_repeatings()
        self._write_fixed_data()

    def show_data(self):
        if self.fixed_data:
            pprint(self.fixed_data)

    def _get_rows_list(self):
        with open(self.source_file_path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',')
            self.rows_list = list(reader)

    def _write_fixed_data(self):
        with open(self.result_file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.fixed_data)

    def _fix_names(self):
        for item in self.rows_list:
            last_name = item[0].split(' ')
            item[0] = last_name[0]
            if len(last_name) > 1:
                if last_name[1][-4:] not in ('овна', 'евна', 'ович', 'евич'):
                    item[1] = last_name[1]
                else:
                    item[2] = last_name[1]
            if len(last_name) > 2:
                item[2] = last_name[2]
            first_name = item[1].split(' ')
            item[1] = first_name[0]
            if len(first_name) > 1:
                item[2] = first_name[1]

    def _fix_phones(self):
        for item in self.rows_list:
            item[5] = re.sub(self.pattern, self.substitution, item[5]).strip()

    def _add_data(self, name: tuple, source: list):
        for item in self.fixed_data:
            if item[0] == name[0] and item[1] == name[1]:
                for index, element in enumerate(item):
                    if item[index] == '':
                        item[index] = source[index]

    def _fix_repeatings(self):
        records = set()
        self.fixed_data = []
        for item in self.rows_list:
            name = (item[0], item[1])
            if name not in records:
                self.fixed_data.append(item)
                records.add(name)
            else:
                self._add_data(name, item)


if __name__ == '__main__':
    open_data_fix = OpenDataFix('phonebook_raw.csv', 'phonebook.csv')
    open_data_fix.fix_data()
    open_data_fix.show_data()
    