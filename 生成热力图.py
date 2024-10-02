from Program.Function import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

def find_files_with_pattern(directory, pattern):
    matched_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if '_' in file and '&' in file:
                prefix = file.split('_', 1)[1]  # 从第一个下划线后开始
                name_part = prefix.split('&', 1)[0]  # 从第一个&前结束
                if name_part == pattern:
                    matched_files.append(os.path.join(root, file))
    return matched_files


# 设置文件夹路径和模式
folder_path = r''
pattern = 'simple_bolling'

# 找到匹配的文件
matched_files = find_files_with_pattern(folder_path, pattern)

# 输出匹配文件的路径列表


# 创建图表
fig, axs = plt.subplots(1, len(matched_files), figsize=(20, 6), sharex=True, sharey=True)

# 读取每个文件并绘制热力图
for i, file in enumerate(matched_files):
    # 读取CSV文件
    df = pd.read_csv(file, encoding='gbk')

    # 分解参数
    df['Para_1'], df['Para_2'] = zip(*df['para'].apply(eval))

    # 创建透视表
    pivot_table = df.pivot(index='Para_1', columns='Para_2', values='累积净值')

    # 绘制热力图
    sns.heatmap(pivot_table, annot=False, cmap='viridis', ax=axs[i])

    # 设置标题和标签
    axs[i].set_title(f'{os.path.basename(file)}', fontsize=14)
    axs[i].set_xlabel('Para_2', fontsize=12)
    axs[i].set_ylabel('Para_1', fontsize=12)

# 调整布局
plt.tight_layout()
plt.show()