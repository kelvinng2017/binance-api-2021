# 基本功能測試
import requests


def lineNotifyMessage(msg):
    token = 'YIyTmgfPel6YGLBau7S6a55VtcWzbopNAGy1zFbI9yR'
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code
