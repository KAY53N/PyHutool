from datetime import datetime, timedelta
from decimal import Decimal
from math import ceil, floor
from .client import Client
from .consts import GET, POST

HOURS8 = 8


class okxApiV5(Client):
    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, test=False, first=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, test, first)

    def accountGetBalance(self, ccy=None):
        params = {}
        if ccy:
            params['ccy'] = ccy
        return self._request_with_params(GET, '/api/v5/account/balance', params)

    def accountGetPosition(self, instType=None, instId=None, posId=None):
        params = {}
        if instType:
            params['instType'] = instType
        if instId:
            params['instId'] = instId
        if posId:
            params['posId'] = posId
        return self._request_with_params(GET, '/api/v5/account/positions', params)

    def accountPositionRisk(self, instType=None):
        params = {}
        if instType:
            params['instType'] = instType
        return self._request_with_params(GET, '/api/v5/account/account-position-risk', params)

    def accountGetBills(self, instType=None, ccy=None, mgnMode=None, before='', after=''):
        params = {}
        if instType:
            params['instType'] = instType
        if ccy:
            params['ccy'] = ccy
        if mgnMode:
            params['mgnMode'] = mgnMode
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        return self._request_with_params(GET, '/api/v5/account/bills', params)

    def accountGetBillsarchive(self, before='', after='', instType='', ccy='', type_=''):
            params = {}
            if instType:
                params['instType'] = instType
            if ccy:
                params['ccy'] = ccy
            if type_:
                params['type'] = type_
            if before:
                params['before'] = before
            if after:
                params['after'] = after
            return self._request_with_params(GET, '/api/v5/account/bills-archive', params)

    def accountGetConfig(self):
        return self._request_without_params(GET, '/api/v5/account/config')

    def accountSetPositionMode(self, params: dict):
        if not params:
            params['posMode'] = 'long_short_mode'
        else:
            params = dict
        return self._request_with_params(POST, '/api/v5/account/set-position-mode', params)

    def accountSetLeverage(self, lever, mgnMode, instId=None, ccy=None, posSide=None):
        params = {}
        params['lever'] = lever
        params['mgnMode'] = mgnMode
        if instId:
            params['instId'] = instId
        if ccy:
            params['ccy'] = instId
        if posSide:
            params['posSide'] = instId
        return self._request_with_params(POST, '/api/v5/account/set-leverage', params)

    def accountGetMaxSize(self, instId, tdMode='cross'):
        params = {}
        params['instId'] = instId
        params['tdMode'] = tdMode
        return self._request_with_params(GET, '/api/v5/account/max-size', params)

