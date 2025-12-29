import pandas as pd
import numpy as np

def handle_missing_values(input_path, output_path):
    """
    处理电商用户行为数据的缺失值
    input_path:原始csv文件路径
    output_path:清洗后文件路径
    """
    # 关键：使用gb18030编码读取，low_memory=False避免混合类型警告
    df = pd.read_csv(input_path, encoding='gb18030', low_memory=False)
    print(f"原始数据行数：{len(df)}")
    print("原始缺失值统计：")
    missing_stats = pd.DataFrame({
        '缺失数量': df.isnull().sum(),
        '缺失占比(%)': (df.isnull().sum() / len(df) * 100).round(4)
    })
    print(missing_stats[missing_stats['缺失数量'] > 0])

    # 1.核心字段(user_id/goods_id/behavior/timetamp):缺失值直接删除
    core_cols = ['user_id', 'goods_id', 'behavior', 'timestamp']
    df = df.dropna(subset=core_cols)
    print(f"\n删除核心字段缺失记录,剩余行数:{len(df)}")

    # 2.数值型数据（price/amount/sex）: 用0或均值填充
    numeric_cols = ['price', 'amount', 'sex', 'category_id']
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            fill_value = 0 if col in ['price', 'amount', 'category_id'] else df[col].median()
            df[col] = df[col].fillna(fill_value)
            print(f"[{col}字段缺失值用{fill_value}填充")

    # 3.字符型字段（address/device/comment）: 用“未知”填充
    str_cols = ['address', 'device', 'comment']
    for col in str_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna('未知')
            print(f"{col}字段缺失值用‘未知’填充")

    # 保存结果
    df.to_csv(output_path, index=False, encoding='gb18030')
    print(f"\n缺失值处理完成!清洗后数据保存至: {output_path}")
    print(f"最终数据行数：{len(df)},剩余缺失值数量：{df.isnull().sum().sum()}")

if __name__ == '__main__':
    #适配Github仓库目录结构
    handle_missing_values(
        input_path="data/UserBehavior--1.csv",
        output_path="data/cleaned_missing_handled.csv"
    )


