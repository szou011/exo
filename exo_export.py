from exo import ExoReport
from exo.clarity import config

done = ['BRANCHES', 'CREDIT_STATUS', 'CURRENCIES', 
        'DR_ACCGROUP2S', 'DR_ACCGROUPS', 'DR_ACCS', 
        'DR_ALLOCATIONS', 'DR_INVLINES', 'DR_TRANS', 
        'NARRATIVES', 'PERIOD_STATUS', 'SALESORD_HDR', 'SALESORD_LINES', 'STAFF', 'STOCK_GROUPS',
        'STOCK_ITEMS', 'X_DR_ACCGROUP3S', 'X_RETAILGROUP']

reports = ['Z_GLTRANS']

for report in reports:
    ExoReport("NZ", params=None, report_type=report).save_csv()

#print(config)
