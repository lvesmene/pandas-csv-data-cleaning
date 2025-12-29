import pandas as pd
import numpy as np

def standardize_time_format(input_path, output_path):
    """
    时间戳转换为标志格式,拆分时间维度
    """
    df = pd.read_csv(input_path, encoding='gb18030', low_memory=False)
    print("开始时间字段标准化...")
    
    # 1. 时间戳转换（秒级→标准datetime格式）
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    # 删除时间戳异常的记录（非数值、0、未来时间）
    current_time = pd.Timestamp.now()
    df = df[(df['timestamp'] > 0) & (df['timestamp'].notnull())]
    # 转换为datetime
    df['behavior_time'] = pd.to_datetime(df['timestamp'], unit='s')
    # 过滤未来时间的记录
    future_count = df[df['behavior_time'] > current_time].shape[0]
    df = df[df['behavior_time'] <= current_time]
    if future_count > 0:
        print(f"过滤未来时间记录:{future_count}条")

    # 2. 拆分时间维度（便于后续分析）
    df['date'] = df['behavior_time'].dt.date  # 日期（2024-05-29）
    df['hour'] = df['behavior_time'].dt.hour  # 小时（0-23）
    df['weekday'] = df['behavior_time'].dt.weekday  # 星期（0=周一，6=周日）

    # 3. 删除原始timestamp字段（保留标准化后的时间字段）
    df = df.drop('timestamp', axis=1)

    # 保存结果
    df.to_csv(output_path, index=False, encoding='gb18030')
    print(f"\n时间字段标准化完成!")
    print(f"时间范围:{df['behavior_time'].min()} ~ {df['behavior_time'].max()}")
    print(f"新增时间字段:behavior_time(标准时间)、date(日期)、hour(小时)、weekday(星期)")
    print(f"清洗后的数据保存至:{output_path}")

if __name__ == "__main__":
    standardize_time_format(
        input_path="data/cleaned_numeric_fixed.csv",
        output_path="data/cleaned_time_standardized.csv"
    )