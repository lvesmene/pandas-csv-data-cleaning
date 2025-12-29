import pandas as pd
 

def remove_duplicates(input_path, output_path):
    """
    处理重复记录（完全重复+逻辑重复）
    """
    df = pd.read_csv(input_path, encoding='gb18030', low_memory=False)
    original_rows = len(df)
    print(f"原始数据行数: {original_rows}")

    # 1.完全重复记录处理
    full_duplicates = df.duplicated().sum()
    if full_duplicates > 0:
        df = df.drop_duplicates(keep='first')
        print(f"删除完全重复记录:{full_duplicates}条")

    # 2.逻辑重复记录处理(用户+商品+行为+时间戳相同视为重复)
    logic_dup_cols = ['user_id', 'goods_id', 'behavior', 'timestamp']
    logic_duplicates = df.duplicated(subset=logic_dup_cols).sum()
    if logic_duplicates > 0:
        df = df.drop_duplicates(subset=logic_dup_cols, keep='first')
        print(f"删除逻辑重复记录:{logic_duplicates}条")

    # 保存结果
    df.to_csv(output_path, index=False, encoding='gb18030')
    final_rows = len(df)
    print(f"删除总记录数:{original_rows - final_rows}条({((original_rows - final_rows)/original_rows)*100:.4f}%)")
    print(f"清洗后的数据保存至：{output_path}")

if __name__ =="__main__":
    remove_duplicates(
        input_path="data/cleaned_missing_handled.csv",
        output_path="data/cleaned_duplicates_removed.csv"
    )
