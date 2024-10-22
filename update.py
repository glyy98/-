import pandas as pd
#这个是可以直接用的，导入
# 参数表，假设表格包含 'menu_level1', 'menu_level2', 'menu_level3' 和 'agents' ,所含字段都是可以导入数据库，此时agents的数据是点位名称
df = pd.read_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\canshu_table.xlsx')

# df = pd.read_excel(r'C:\Users\Administrator\AquaProjects\aqua_test\TTTTTTT\zhongyuan.xlsx')


# 将数据库中点位表的id和点位名称生成表格，读取
mapping_df = pd.read_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\crane_agent.xlsx')  
# mapping_df = pd.read_excel(r'C:\Users\Administrator\AquaProjects\aqua_test\TTTTTTT\7#3265.xlsx')


# 把点位表转成字典；创建点位名称到 ID 的映射字典，确保去除空格
point_mapping = dict(zip(mapping_df['agents'].str.strip(), mapping_df['id']))

# 将参数表的点位名称换成点位id
# 遍历参数表中agents列的所有点位名称='x'，在点位表字典中查找，名称转换为ID，如果没找到就赋值unknown
df['agents'] = df['agents'].apply(lambda x: point_mapping.get(x.strip(), "unknown")) 

# 检查转换是否成功
print("转换后的 agents 列：")
print(df[['agents']].head(10))

# 根据一级、二级、三级菜单分组，将每组中的 'agents' 合并为逗号分隔的字符串，确保 agents 是字符串
# 将参数表分组，
df_grouped = df.groupby(['menu_level1', 'menu_level2', 'menu_level3'])['agents'].apply(
    lambda ids: '[' + ','.join([f'"{str(id)}"' for id in ids]) + ']')


# 选择每个分组的第一条记录
df_final = df.drop_duplicates(subset=['menu_level1', 'menu_level2', 'menu_level3']).copy()
df_final['agents'] = df_final.apply(lambda row: df_grouped.loc[(row['menu_level1'], row['menu_level2'], row['menu_level3'])], axis=1)


# 保存结果到新的 Excel 文件
# df_final.to_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\hebing.xlsx', index=False)
df_final.to_excel(r'C:\Users\Administrator\Desktop\dev导入参数配置\6号测.xlsx', index=False)

# df_final.to_excel(r'C:\Users\Administrator\AquaProjects\aqua_test\TTTTTTT\66.xlsx', index=False)

# 打印前几行的结果以检查
print(df_final[['menu_level1', 'menu_level2', 'menu_level3', 'agents']].head())

