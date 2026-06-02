# -*- coding: utf-8 -*-
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# 读取修复后的MD文件
md_path = r'C:\Users\Administrator\Desktop\moxie-main\一年级下册生字组词造句 - 副本.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 解析结构
result = {
    'title': '一年级下册 生字组词与造句',
    'units': []
}
current_unit = None
current_lesson = None
current_type = None  # 'shizi' or 'xiezhi'

lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # 匹配单元 ## 第一单元·识字
    if line.startswith('## '):
        if current_unit and current_lesson:
            current_unit['lessons'].append(current_lesson)
            current_lesson = None
        if current_unit:
            result['units'].append(current_unit)
        current_unit = {'name': line[3:].strip(), 'lessons': []}
    
    # 匹配课程 ### 识字1：春夏秋冬
    elif line.startswith('### '):
        if current_unit and current_lesson:
            current_unit['lessons'].append(current_lesson)
        current_lesson = {'name': line[4:].strip(), 'shizi': [], 'xiezhi': []}
        current_type = None
    
    # 匹配类型 #### 识字（会认）或 #### 写字（会写）
    elif line.startswith('#### '):
        type_name = line[5:].strip()
        if '识字' in type_name and '写' not in type_name:
            current_type = 'shizi'
        elif '写字' in type_name:
            current_type = 'xiezhi'
        else:
            current_type = None
    
    # 匹配表格行 | 霜 | 霜雪 | 冰霜 | 妈妈买了霜雪。 |
    elif line.startswith('|') and not line.startswith('|------'):
        # 跳过表头
        if '生字' in line or '----' in line:
            i += 1
            continue
        
        # 解析表格行
        parts = [p.strip() for p in line.split('|')]
        # parts = ['', '霜', '霜雪', '冰霜', '妈妈买了霜雪。', '']
        if len(parts) >= 5 and current_lesson and current_type:
            char = parts[1]
            word1 = parts[2]
            word2 = parts[3]
            sentence = parts[4]
            
            # 跳过空行或无效行
            if char and char != '生字' and len(char) == 1:
                entry = {
                    'char': char,
                    'word1': word1,
                    'word2': word2,
                    'sentence': sentence
                }
                current_lesson[current_type].append(entry)
    
    i += 1

# 追加最后一个lesson和unit
if current_unit and current_lesson:
    current_unit['lessons'].append(current_lesson)
if current_unit:
    result['units'].append(current_unit)

# 保存为JSON
output_path = r'C:\Users\Administrator\Desktop\moxie-main\一年级下册生字组词造句.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('✅ JSON文件已生成！')
print('文件路径:', output_path)
print('单元数:', len(result['units']))

# 统计
total_shizi = 0
total_xiezhi = 0
for unit in result['units']:
    for lesson in unit['lessons']:
        total_shizi += len(lesson['shizi'])
        total_xiezhi += len(lesson['xiezhi'])

print('\n统计信息:')
print('  识字表（会认）:', total_shizi, '字')
print('  写字表（会写）:', total_xiezhi, '字')
print('  总计:', total_shizi + total_xiezhi, '字')

# 显示前3个示例
print('\n示例数据（前3个）:')
count = 0
for unit in result['units']:
    for lesson in unit['lessons']:
        for item in lesson['shizi'][:1] + lesson['xiezhi'][:1]:
            if count < 3:
                print(f'  {item["char"]}: {item["word1"]}、{item["word2"]} → {item["sentence"]}')
                count += 1
    if count >= 3:
        break
