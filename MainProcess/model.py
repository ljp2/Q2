import os
from PySide6.QtWidgets import(QMessageBox)

import alpacaAPI as api

class Model:
    current_file_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(current_file_path)
    main_directory = os.path.dirname(parent_directory)
    TICKERS_FILE_NAME = f'{main_directory}/tickers.txt'
    ACCOUNT_VALUE_FILE_NAME = f'{main_directory}/account-value.txt'
    
    favorite_period_intervals = ['1Day - 5Min', '1Week - 1Hr',
                            '1Month - 4Hr', '3Months - 4Hr', '1Year - 1Day', '1Year - 1Week']

    initial_duration = '1Month'
    initial_interval = '4Hr'

    charttypes = ['Line', 'Candle', 'HA']
    preselect_charttype = 'HA'

    def __init__(self) -> None:
        if os.path.exists(self.ACCOUNT_VALUE_FILE_NAME):
            with open(self.ACCOUNT_VALUE_FILE_NAME, 'r') as file:
                self.account_value = int(file.readline().strip())
        else:
            print("The file does not exist.")
        
        with open(self.TICKERS_FILE_NAME, 'r') as file:
            self.tickers = [x.strip() for x in file.readlines()]
        self.current_duration = self.initial_duration
        self.current_interval = self.initial_interval
        self.current_charttype = self.preselect_charttype

    def getAccountValue(self) -> int:
        return self.account_value
    
    def getTickers(self) -> list[str]:
        return self.tickers
    
    def get_favorite_period_intervals(self) -> list[str]:
        return self.favorite_period_intervals
    
    def get_all_durations(self) -> list[str]:
        return( list(api.duration_dict.keys()) )
    
    def get_all_intervals(self) -> list[str]:
        return( list(api.interval_dict.keys()) )
    
    def get_initial_duration_interval(self) -> tuple[str]:
        return (self.initial_duration, self.initial_interval)
    
    def get_current_duration_interval(self) -> tuple[str]:
        return (self.current_duration, self.current_interval)
    
    def get_current_charttype(self):
        return(self.current_charttype)
    
    def set_current_duration(self, duration):
        self.current_duration = duration
 
    def set_current_interval(self, interval):
        self.current_interval = interval   

    def set_current_charttype(self, charttype:str):
        self.current_charttype = charttype

    
    def setAccountValue(self, value):
        ok = True
        value_int = None
        try:
            if type(value) == str:
                value_int = round(float(value))
            elif type(value) == float:
                value_int = round(float(value))
            elif type(value) == int:
                value_int = value
            else:
                ok = False
                QMessageBox.critical(None, "Error", f'{"Invalid Account Value."} {type(value)}')
        except:
            ok = False
        if ok:
            txt = f'$ {value_int:.0f}'
            self.account_value = value_int
            with open(self.ACCOUNT_VALUE_FILE_NAME, 'w') as file:
                file.write(str(value_int))
        return ok, value_int
