from logging import StreamHandler
import datetime
import logging
import datetime
_default_attri = ['levelname', 'name', 'filename', 'module']
class SheetLogHandler(StreamHandler):
    def __init__(self, gLog, attris, time=True):
        StreamHandler.__init__(self)
        self.gLog = gLog
        self.attris = _default_attri if attris is None else attris
        self.nattri = len(self.attris)
        if time:
            self.nattri += 1
        self.time = time

    def emit(self, record):
        data = {}
        if self.time:
            data['time'] = str(datetime.datetime.now())
        for attr in self.attris:
            data[attr] = getattr(record, attr)
        if isinstance(record.msg, str):
            data['message'] = record.msg
        elif isinstance(record.msg, dict):
            # print(f'record.msg : {record.msg}')
            data.update(record.msg)
            # print(f'data : {data}')
        self.gLog.append(data)
        return