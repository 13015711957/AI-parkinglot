from aip import AipOcr
import re

APP_ID="********"
API_KEY="**********"
SECRET_KEY="******"
#这里根据百度申请的接口秘钥填写


client=AipOcr(APP_ID,API_KEY,SECRET_KEY)

def get_file_content(filepath):
    with open(filepath,'rb')as fp:
        return fp.read()

def getch(type):
    if type==0:
        image=get_file_content('img/img_in.jpg')
    else:
        image = get_file_content('img/img_out.jpg')
    try:
        results=client.licensePlate(image)['words_result']['number']
    except:
        return None
    #车牌号校验
    pattern = '([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}(([A-HJ-NP-Z0-9]{5}[DF]{1})|([DF]{1}[A-HJ-NP-Z0-9]{5})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})'
    if not re.match(pattern,results):
        return None

    results=results[:2]+'·'+results[2:]
    print(results)
    return results