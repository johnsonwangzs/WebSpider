# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-07
# @file    : lxml_usage.py
# @function: xpath操作和lxml库的使用。


from lxml import etree


text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''


html = etree.HTML(text)
# html = etree.parse('./test.html', etree.HTMLParser())  # 也可从文件读
result = etree.tostring(html)
print(result)
print(result.decode('utf-8'))
print('='*16)

result = html.xpath('//*')
print(result)
print('-'*16)
result = html.xpath('//li')
print(result)
print('-'*16)
result = html.xpath('//li/a')  # 所有li节点的所有直接子节点a
print(result)
print('-'*16)
result = html.xpath('//ul//a')  # ul节点的所有子孙节点a
print(result)
print('-'*16)
result = html.xpath('//a[@href="link4.html"]/../@class')  # @符号实现属性过滤；获取父节点class属性
print(result)
print('-'*16)
result = html.xpath('//a[@href="link4.html"]/parent::*/@class')
print(result)
print('='*16)

result = html.xpath('//li[@class="item-0"]//text()')  # 文本获取
print(result)
print('-'*16)
result = html.xpath('//li[@class="item-0"]/a/text()')
print(result)
print('='*16)

result = html.xpath('//li/a/@href')  # 属性获取
print(result)
print('='*16)

text1 = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html1 = etree.HTML(text1)
result1 = html1.xpath('//li[contains(@class, "li")]/a/text()')  # 属性多值匹配
print(result1)
print('='*16)

text2 = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
html2 = etree.HTML(text2)
result2 = html2.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')  # 多属性匹配，使用and等运算符
print(result2)
print('='*16)

text3 = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html3 = etree.HTML(text3)
result3 = html3.xpath('//li[1]/a/text()')  # 按序选择。注意序号从1而不是0开始
print(result3)
print('-'*16)
result3 = html3.xpath('//li[last()]/a/text()')
print(result3)
print('-'*16)
result3 = html3.xpath('//li[position()<3]/a/text()')
print(result3)
print('-'*16)
result3 = html3.xpath('//li[last()-2]/a/text()')
print(result3)
print('='*16)

text4 = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html"><span>first item</span></a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html4 = etree.HTML(text4)
result4 = html4.xpath('//li[1]/ancestor::*')
print(result4)
print('-'*16)
result4 = html4.xpath('//li[1]/ancestor::div')
print(result4)
print('-'*16)
result4 = html4.xpath('//li[1]/attribute::*')
print(result4)
print('-'*16)
result4 = html4.xpath('//li[1]/descendant::span')
print(result4)
print('-'*16)
result4 = html4.xpath('//li[1]/following::*[2]')
print(result4)
print('-'*16)
result4 = html4.xpath('//li[1]/following-sibling::*')
print(result4)
print('='*16)
