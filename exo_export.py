from exo import ExoReport
from exo.clarity import config


rebate = ExoReport("NZ", params=None, report_type='DR_ACCS')

print(config)

rebate.save_csv()