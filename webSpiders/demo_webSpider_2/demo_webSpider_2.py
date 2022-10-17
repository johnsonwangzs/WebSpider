# -*- encoding: utf-8 -*-
# @auther  : 你好哇
# @time    : 2022-10-10
# @file    : demo_webSpider_2.py
# @function: 自动销假（仅对新版出入校有效）
# 在浏览器里打开下面的URL，F12复制request headers里的cookie，替换掉HEADERS常量里的。然后运行程序


import json
import requests
import logging

# 设置日志输出级别和输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
URL = 'https://n.buaa.edu.cn/site/my-task/todo?p=1&page_size=50&app_id=&keyword=&keyword_type=user&time_type=0' \
      '&time_lower=&time_upper=&y=&department_id=&flags=&orderby=createdDesc&class_name= '
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36',
    'Cookie': 'Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1664376534,1664766551,1664779939,1664883302; '
              'insert_cookie=12091892; PHPSESSID=ST-2901882-tWV-hlPeL1oeawgtcHT69EMSNcof23d5167ee9d; '
              'yzs_vjuid=258863; yzs_vjvd=dfd7d3847579b240f4d073d571c41926; yzs_vt=181116971 '
}


def scrape_page(url):
    """
    使用requests模块实现页面（通用）爬取。
    :param url:
    :return:
    """
    global HEADERS
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        # 将logging库中的error方法里的exc_info参数设置为True，可以打印出Traceback错误堆栈信息
        logging.error('error occurred while scraping %s', url, exc_info=True)


if __name__ == '__main__':
    res = scrape_page(URL)
    print(res)
    print('\n\n\n')
    data = json.loads(res)

    num = len(data['d']['list'])
    print('待销假项目数：', num)
    print('\n\n')
    for i in range(num):
        print('开始进行新的销假...')
        task_id = data['d']['list'][i]['task_id']
        form_data = {
            'task_id': task_id,
            'form_data': '{"1594":{"Input_436":"","Region_14":{"address":"北京市/海淀区","details":"","province":{'
                         '"label":"北京市","value":"110000"},"city":{"label":"海淀区","value":"110108"},"area":{"label":"",'
                         '"value":""}},"Calendar_433":null,"SelectV2_358":[{"name":"副书记","value":"3","default":1,'
                         '"imgdata":""}],"SelectV2_434":[],"SelectV2_435":[],"ShowHide_361":"","ShowHide_362":"",'
                         '"ShowHide_369":"","ShowHide_370":"","ShowHide_422":"","ShowHide_437":"","ShowHide_447":"",'
                         '"Validate_103":"","Validate_105":"","Validate_175":"","Validate_176":"","Validate_272":""}}',
            'deal_data': '{"require_claim":0,"comment":"","attachment":[],"reader":[],"operation":{"name":"提交",'
                         '"value":3},"deal_depart_id":246537,"oversee":"no"}',
            'deal_depart_id': '246537'
        }

        r = requests.post('https://n.buaa.edu.cn/site/task/deal', data=form_data, headers=HEADERS)
        print(r)
        print('已销假！\n\n')

    print('祝您生活愉快！')
