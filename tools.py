import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def translate_excel(input_file, output_file, progress_callback=None):
    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    # 创建翻译模型
    translator = pipeline("translation", model='E:/opus-mt-en-zh')

    # 逐行翻译并显示进度
    for index, row in tqdm(df.iterrows(), total=len(df), desc="翻译进度"):
        original_text = row.get('原文', '')  # 假设原文在 '原文' 列，处理可能的空值
        if original_text:
            try:
                translated_text = translator(original_text)[0]['translation_text']
                df.at[index, '翻译'] = translated_text  # 将翻译结果保存到 '翻译' 列
            except Exception as e:
                print(f"翻译失败: {original_text}, 错误: {e}")
                df.at[index, '翻译'] = f"翻译失败: {e}"  # 记录翻译失败的信息
        else:
            df.at[index, '翻译'] = ''  # 空值处理

        # 调用进度回调函数
        if progress_callback:
            progress_callback((index + 1) / len(df) * 100)

    # 保存更新后的 Excel 文件
    df.to_excel(output_file, index=False)

    print(f"翻译完成，结果已保存到: {output_file}")
    # 返回翻译后的文件名
    return os.path.basename(output_file)


