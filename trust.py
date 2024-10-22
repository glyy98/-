import pandas as pd
#这个会模拟页面新增后的排布，不要用
# 参数表，假设表格包含 'menu_level1', 'menu_level2', 'menu_level3' 和 'agents'，agents 的数据是点位名称
df = pd.read_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\canshu_table.xlsx')


# 读取数据库中点位表的 ID 和点位名称生成表格
mapping_df = pd.read_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\crane_agent.xlsx')  

# 创建点位名称到 ID 的映射字典，确保去除空格
point_mapping = dict(zip(mapping_df['agents'].str.strip(), mapping_df['id']))

# 将参数表的点位名称换成点位 ID，没找到的赋值为 "unknown"
df['agents'] = df['agents'].apply(lambda x: point_mapping.get(x.strip(), "unknown"))

# 按三级菜单进行分组，并将 agents 列转换为带双引号的 JSON 格式
df_grouped_level3 = df.groupby(['menu_level1', 'menu_level2', 'menu_level3'])['agents'].apply(
    lambda ids: '[' + ','.join([f'"{str(id)}"' for id in ids]) + ']'
)

# 构建一级菜单的数据，'menu_level2', 'menu_level3', 'agents' 为空
df_level1 = df.drop_duplicates(subset=['menu_level1']).copy()
df_level1['menu_level2'] = ''
df_level1['menu_level3'] = ''
df_level1['agents'] = ''

# 构建一二级菜单的数据，'menu_level3', 'agents' 为空
df_level2 = df.drop_duplicates(subset=['menu_level1', 'menu_level2']).copy()
df_level2['menu_level3'] = ''
df_level2['agents'] = ''

# 构建一二三级菜单的数据，'agents' 为合并后的 JSON 格式
df_level3 = df.drop_duplicates(subset=['menu_level1', 'menu_level2', 'menu_level3']).copy()
df_level3 = df_level3[df_level3['menu_level3'].notna()]  # 去除 menu_level3 为空的记录
df_level3['agents'] = df_level3.apply(
    lambda row: df_grouped_level3.loc[(row['menu_level1'], row['menu_level2'], row['menu_level3'])],
    axis=1
)

# 合并一级、二级、三级菜单的数据
df_final = pd.concat([df_level1, df_level2, df_level3], ignore_index=True)

# 保存结果到 CSV 文件
df_final.to_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\6号测.xlsx', index=False)

# 打印前几行的结果以检查
print(df_final[['menu_level1', 'menu_level2', 'menu_level3', 'agents']].head())
