from datetime import datetime
from conf.config import *
import xlrd, openpyxl, os, re, json


class Excel:
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

    def __init__(self, file_rule=None, title_ch=None, title=None):
        self.download_path = os.path.join(BROWSER.get('google').get('download'), CURRENT_DATE)
        self.file_rule = file_rule
        self.title_ch = title_ch
        self.title = title

    def combination_files(self,target_file_name):
        files = self.get_files(self.file_rule)
        for f in files:
            self.combination_xlsx(f,target_file_name)

    def combination_xlsx(self, source_file_name, target_file_name):
        source_file_path = os.path.join(self.download_path, source_file_name)
        source_workbook = xlrd.open_workbook(source_file_path)
        source_sheet = source_workbook.sheet_by_index(0)

        # judge  the extention of target file is exists
        self.target_filename_path = os.path.join(self.download_path,target_file_name)

        if not os.path.isfile(self.target_filename_path):
            self.create_xlsx(self.title_ch)

        wb = openpyxl.load_workbook(self.target_filename_path)
        target_sheet = wb.worksheets[0]

        for row_index in range(1, source_sheet.nrows):
            target_sheet.append(
                self.set_unicode(source_sheet.row_values(row_index))
            )
        wb.save(self.target_filename_path)
        wb.close()

    def create_xlsx(self, title):
        create_wb = openpyxl.Workbook()
        create_sheet = create_wb.worksheets[0]
        create_sheet.append(title)
        create_wb.save(self.target_filename_path)
        create_wb.close()

    def set_unicode(self, list_data):
        if isinstance(list_data, list):
            for k, v in enumerate(list_data):
                list_data[k] = Excel.ILLEGAL_CHARACTERS_RE.sub(r'', v)
        else:
            return None
        return list_data

    def get_files(self, pattern=None):
        files = []

        for f in os.listdir(self.download_path):
            if pattern is not None:
                result = re.search(r'' + pattern, os.path.splitext(f)[0])
                if result:
                    files.append(os.path.basename(f))
            else:
                files.append(os.path.basename(f))
        return files

    def read_excel(self, filename, date, start=1, length=5000):
        file_path = os.path.join(BROWSER.get('google').get('download'), date, filename)
        list_values = []
        end = int(start + length - 1)
        if not os.path.isfile(file_path):
            return False

        wb = openpyxl.load_workbook(file_path,read_only=True)
        active_sheet = wb.worksheets[0]
        max_row = int(active_sheet.max_row)

        if end > max_row:
            end = max_row
        if isinstance(start, int):
            for row in active_sheet.iter_rows(min_row=start, max_row=end):
                row_value = []
                for col in row:
                    row_value.append(col.value)
                list_values.append(dict(zip(self.title, row_value)))

        return json.dumps({'totalnum': max_row, 'data': list_values})
