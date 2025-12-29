import pandas as pd
import numpy as np

def comprehensive_cleaning(input_path, output_path):
    """
    整合所有清洗逻辑:缺失值→重复值→数值字段→时间格式
    """
    print("=" * 60)
    print("开始电商用户行为数据综合清洗")
    print("=" * 60)
    start_time = pd.Timestamp.now()

    # 步骤1：读取原始数据（指定gb18030编码）
    df = pd.read_csv(input_path, encoding='gb18030', low_memory=False)
    original_rows = len(df)
    print(f"1. 原始数据：{original_rows}行 × {len(df.columns)}列")

    # 步骤2：缺失值处理
    core_cols = ['user_id', 'goods_id', 'behavior', 'timestamp']
    df = df.dropna(subset=core_cols)
    # 数值型字段填充
    numeric_cols = ['price', 'amount', 'sex']
    for col in numeric_cols:
        fill_value = 0 if col in ['price', 'amount'] else df[col].median()
        df[col] = df[col].fillna(fill_value)
    # category_id字段特殊处理：缺失值填充0（表示未分类）
    if 'category_id' in df.columns:
        df['category_id'] = df['category_id'].fillna(0)
    # 字符型字段填充
    str_cols = ['address', 'device', 'comment']
    for col in str_cols:
        df[col] = df[col].fillna('未知')
    print(f"2. 缺失值处理后：{len(df)}行（删除{original_rows - len(df)}条核心字段缺失记录）")

    # 步骤3：重复值处理
    # 完全步骤
    # 在删除重复逻辑之前保存原始行数
    before_dup_rows = len(df)
    df = df.drop_duplicates(keep='first')
    # 逻辑重复
    logic_dup_cols = ['user_id', 'goods_id', 'behavior', 'timestamp']
    df = df.drop_duplicates(subset=logic_dup_cols, keep='first')
    after_dup_rows = len(df)
    print(f"3. 重复处理后的：{after_dup_rows}行（删除{before_dup_rows - after_dup_rows}条重复记录）")

    # 步骤4：数值型字段清洗
    # ID字段清洗
    # user_id和goods_id必须为正整数
    strict_id_cols = ['user_id', 'goods_id']
    for col in strict_id_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df[(df[col] > 0) & (df[col].notnull())]
    # category_id允许为0（表示未分类）
    if 'category_id' in df.columns:
        df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').fillna(0)
        df = df[(df['category_id'] >= 0) & (df['category_id'].notnull())]
    # 金额字段清洗
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df.loc[df['price'] < 0, 'price'] = 0
    price_99 = df['price'].quantile(0.99)
    df.loc[df['price'] > price_99, 'price'] = price_99
    # 数量字段清洗
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df.loc[df['amount'] < 0, 'amount'] = 0
    df['amount'] = df['amount'].round().astype(int)
    print(f"4. 数值字段清洗后：{len(df)}行")

    # 步骤5：时间字段标准化
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df = df[(df['timestamp'] > 0) & (df['timestamp'].notnull())]
    df['behavior_time'] = pd.to_datetime(df['timestamp'], unit='s') 
    current_time = pd.Timestamp.now()
    df = df[df['behavior_time'] <= current_time]
    #拆分时间维度
    df['date'] = df['behavior_time'].dt.date
    df['hour'] = df['behavior_time'].dt.hour
    df['weekday'] = df['behavior_time'].dt.weekday
    df = df.drop('timestamp', axis=1)
    print(f"5. 时间字段标准化后：{len(df)}行")

    # 步骤6：device字段大小写统一（额外优化）
    df['device'] = df['device'].str.upper() # 全部转为大写
    print(f"6. device字段大小写统一完成(全部转为大写)")

    #保存最终结果
    df.to_csv(output_path, index=False, encoding='gb18030')
    end_time = pd.Timestamp.now()
    duration = (end_time - start_time).total_seconds()

    # 输出清洗报告
    print("\n" + "=" * 60)
    print("综合清洗完成报告")
    print("=" * 60)
    print(f"原始数据行数：{original_rows}")
    print(f"最终数据行数：{len(df)}")
    print(f"删除数据行数：{original_rows - len(df)}({((original_rows - len(df))/original_rows)*100:.2f}%)")
    print(f"清洗耗时：{duration:.2f}秒")
    print(f"最终数据字段：{', '.join(df.columns)}")
    print(f"清洗后数据保存至：{output_path}")

if __name__ == "__main__":
    # 直接读取原始数据， 一键输出最终清洗结果
    comprehensive_cleaning(
        input_path="data/UserBehavior--1.csv",
        output_path="data/cleaned_user_behavior_final.csv"
    )
