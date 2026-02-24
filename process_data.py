import pandas as pd
import os
import re
import numpy as np

# 创建输出目录
output_dir = 'processed_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取CSV文件
print("开始读取CSV文件...")
df = pd.read_csv('问卷数据原始.csv', encoding='utf-8')
print(f"成功读取数据，总行数: {len(df)}")

# 检查数据结构
rumor_col = df.columns[1]  # 谣言信息列（第2列）
debunk_col = df.columns[2]  # 辟谣信息列（第3列）
print(f"谣言列名: {rumor_col}")
print(f"辟谣列名: {debunk_col}")

# 定义匹配谣言和辟谣信息的正则表达式 - 增加对简短格式的支持
rumor_pattern = re.compile(r'谣言\s*信息\s*(\d+).*?')  # .*? 匹配任意字符
debunk_pattern = re.compile(r'辟谣\s*(?:信息\s*)?(\d+)\s*([a-d])')  # 让"信息"变成可选项

# 创建字典来存储不同组合的数据
data_dict = {}
skipped_rows = 0

# 遍历数据，按谣言-辟谣组合进行分组
for idx, row in df.iterrows():
    # 跳过标题行或空行
    if pd.isna(row[rumor_col]) or not isinstance(row[rumor_col], str):
        skipped_rows += 1
        continue
    
    # 提取谣言编号和辟谣编号 - 确保去除所有空格后再匹配
    rumor_match = rumor_pattern.search(''.join(str(row[rumor_col]).split()))
    debunk_match = debunk_pattern.search(''.join(str(row[debunk_col]).split()))
    
    if not rumor_match or not debunk_match:
        print(f"无法匹配行 {idx}: {row[rumor_col]} - {row[debunk_col]}")
        skipped_rows += 1
        continue
    
    rumor_num = rumor_match.group(1)
    debunk_num = debunk_match.group(1)
    debunk_type = debunk_match.group(2)
    
    # 验证谣言和辟谣的编号是否匹配
    if rumor_num != debunk_num:
        print(f"警告: 谣言和辟谣编号不匹配: {row[rumor_col]} - {row[debunk_col]}")
    
    # 创建组合键
    combo_key = f"谣言{rumor_num}_辟谣{debunk_type}"
    
    # 为这个组合添加数据
    if combo_key not in data_dict:
        data_dict[combo_key] = []
    
    # 添加行数据
    data_dict[combo_key].append(row)

print(f"跳过了 {skipped_rows} 行")
print(f"找到 {len(data_dict)} 种谣言-辟谣组合")

# 处理每个组合的数据并输出到CSV
for combo_key, rows in data_dict.items():
    print(f"处理组合: {combo_key}, 原始数据行数: {len(rows)}")
    
    # 创建该组合的数据框
    combo_df = pd.DataFrame(rows)
    
    # 替换空字符串为NaN（除了观点变化列）
    for col in combo_df.columns:
        mask = combo_df[col].astype(str).isin(['', 'nan', 'None', 'NaN'])
        combo_df.loc[mask, col] = np.nan
    
    # 查找全为空的列（除了观点变化列）
    empty_columns = []
    for col in combo_df.columns:
        if col not in [rumor_col, debunk_col]:  # 保留谣言和辟谣列
            if combo_df[col].isna().all():  # 如果列全是NaN
                empty_columns.append(col)
    
    # 删除全为空的列
    if empty_columns:
        print(f"删除 {len(empty_columns)} 个空列")
        combo_df = combo_df.drop(columns=empty_columns)
    
    # 输出到CSV，使用utf-8-sig编码以解决中文乱码
    output_file = os.path.join(output_dir, f"{combo_key}.csv")
    combo_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已保存到 {output_file}")

print("处理完成！") 