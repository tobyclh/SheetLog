import pickle
import os.path
from oauth2client.service_account import ServiceAccountCredentials
from queue import Queue
from time import sleep
from .SheetLogHandler import SheetLogHandler
from threading import Thread
import logging
import gspread

_SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] #read and write access

class SheetLog:
    def __init__(self, cred_file, name='GoogleLogSheet', key=None, sheet_num=1, update_interval=5, new_sheet=False, attri=None, email=None, addi_attri={}):
        """Google Log allows easy logging to google sheet
        
        Parameters
        ----------
        cred_file : str
            path to the cred file
        name : str, optional
            name of the sheet (the default is 'GoogleLogSheet')
        key : [type], optional
            key of the sheet (the default is None, which uses name to access instead, overides name if provided)
        sheet_num : int, optional
            page number (the default is 1, which is the first page of the spreadsheet)
        update_interval : int, optional
            update to the google sheet once # seconds (the default is 5, which [default_description])
        new_sheet : bool, optional
            [description] (the default is False, which [default_description])
        attri : [type], optional
            [description] (the default is None, which [default_description])
        email : [type], optional
            [description] (the default is None, which [default_description])
        addi_attri : dict, optional
            [description] (the default is {}, which [default_description])
        
        """

        self.thread = None
        self.key = key
        self.sheet_name = name
        self.msg_queue = Queue()
        self.sheet_num = sheet_num
        self._handler = SheetLogHandler(self, attris=attri)
        self.attris = self._handler.attris
        self.addi_attris = addi_attri
        self._should_stop = False
        self.update_interval = update_interval
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, _SCOPES)
        self.gc = gspread.authorize(credentials)
        if not new_sheet:
            try:
                if self.key is None:
                    self.spreadsheet = self.gc.open(self.sheet_name)
                else:
                    self.key = key
                    self.spreadsheet = self.gc.open_by_key(self.key)
            except:
                print('Cannot open sheet, making one')
                self.spreadsheet = self.make_sheet()
        else:
            self.spreadsheet = self.make_sheet()
        if email is not None:
            self.spreadsheet.share(email, perm_type='user', role='writer', notify=True, email_message='Make you day @ Google Log')
        self.worksheet = getattr(self.spreadsheet, f'sheet{sheet_num}')
        self.thread = Thread(target=self._write_message)
        self.thread.daemon = True
        self.thread.start() # the thread dies with this program
        
        

    def make_sheet(self):
        # open sheet and setup headers if they don't exists already
        attris = list(self.attris)
        if self.handler.time:
            attris.insert(0, 'time')
        attri_names = list(self.addi_attris.keys()) + attris
        n_attri = len(attri_names)
        sheet = self.gc.create(self.sheet_name)
        worksheet = getattr(sheet, f'sheet{self.sheet_num}')
        start_ascii = ord('A')
        end = start_ascii + n_attri
        end_ascii = chr(end)
        cell_list = worksheet.range(f'A1:{end_ascii}1')
        for cell, attri_name in zip(cell_list, attri_names):
            cell.value = attri_name
        worksheet.update_cells(cell_list)
        return sheet

    @property
    def handler(self):
        return self._handler
    
    def _write_message(self):
        # print('thread started')
        while not self._should_stop:
            datum = []
            while not self.msg_queue.empty():
                record = self.msg_queue.get()
                data = dict(self.addi_attris)
                data.update(record)
                datum.append(list(data.values()))
            self.append_rows(datum, value_input_option='USER_ENTERED')
            sleep(self.update_interval)
    
    def __del__(self):
        if self.thread is None:
            return
        self._should_stop = True
        self.thread.join(timeout=self.update_interval+1)

    def append(self, msg):
        self.msg_queue.put(msg)
        return

    def append_rows(self, values, value_input_option='RAW'):
        params = {
            'valueInputOption': value_input_option
        }
        body = {
            'values': values
        }
        return self.worksheet.spreadsheet.values_append(self.worksheet.title, params, body)