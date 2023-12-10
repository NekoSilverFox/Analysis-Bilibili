# Use python to request https://api.bilibili.com/x/web-interface/card
import requests

"""
# 修改前的代码示例
# original code
url = "https://api.bilibili.com/x/web-interface/card"
response = requests.request("GET", url)
print(response.text)
print(response.status_code,response.reason)
# (403, 'Forbidden')
"""

# 使用 穿云API 请求示例
# Use Cloudbyapss API to request
url = "https://api.cloudbypass.com/category/memberships"

headers = {
    'x-cb-apikey': 'YOUR_API_KEY',
    'x-cb-host': 'https://t.bilibili.com',
}

response = requests.request("GET", url, headers=headers)

print(response.text)