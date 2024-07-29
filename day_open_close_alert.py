from AuthUpstox.authentication import authenticate
from SendAlert.email_alert import send_email

import json

def day_init():
    login_flag, profile_det, fund_margin_det= authenticate()

    if login_flag == True:
        message = 'Login Successful!' + '\n\n'

        message += json.dumps(profile_det, indent=4)
        message += '\n\n'
        message += json.dumps(fund_margin_det, indent=4)
        message += '\n\n'
        message += 'Regards, \nAlgo SM'

        send_email(message)

if __name__ == "__main__":
    day_init()