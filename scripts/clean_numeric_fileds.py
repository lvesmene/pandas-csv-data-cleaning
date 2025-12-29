import pandas as pd
import numpy as np

def clean_numeric_fileds(input_path, output_path):
    """
    清洗数值型字段:ID字段、金额字段、数量字段
    """

    df = pd.read_csv(input_path, encoding='gb18030', low_memory=False)
    print("开始数值型字段清洗...")

    # 1.ID字段清洗(user_id/goods_id):确保为正整数，category_id允许为0(未分类)
    id_cols = ['user_id', 'goods_id', 'category_id']
    for col in id_cols:
        # 转换为数值类型
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 根据字段类型设置不同的过滤条件
        if col == 'category_id':
            # category_id允许为0(未分类)，但不允许负数或空值
            abnormal_mask = (df[col] < 0) | (df[col].isnull())
            condition_desc = "负数或空值"
        else:
            # user_id和goods_id必须为正整数
            abnormal_mask = (df[col] <= 0) | (df[col].isnull())
            condition_desc = "非正整数"
        
        abnormal_count = df[abnormal_mask].shape[0]

        if abnormal_count > 0:
            # 删除ID异常的记录（核心字段不能异常）
            if col == 'category_id':
                df = df[(df[col] >= 0) & (df[col].notnull())]
            else:
                df = df[(df[col] > 0) & (df[col].notnull())]
            print(f"{col}字段：删除{abnormal_count}条异常记录({condition_desc})")

    # 2. 金额字段清洗（price）：非负，异常大值用99分位数截断
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    # 负值转为0
    # 对 DataFrame（df）的 “price” 列做条件判断，返回一个和 “price” 列长度相同的布尔数组（True 表示对应位置的值小于 0，False 表示不小于 0）。
    #df.loc [行条件，列名]：loc 是 Pandas 中按 “标签 / 条件” 索引数据的方法，这里的用法是 “筛选满足行条件的行，并定位到指定列”：行条件：就是第一步得到的布尔数组（只选 “price < 0” 的行）；列名：指定 “price” 列（只操作这一列，不影响其他列）。
    df.loc[df['price'] < 0, 'price'] = 0
    # 异常大值处理（用99分位数截断）
    price_99 = df['price'].quantile(0.99)
    price_abnormal = df[df['price'] > price_99].shape[0]
    df.loc[df['price'] > price_99, 'price'] = price_99
    print(f"price字段:{price_abnormal}条异常大值用{price_99:.2f}截断,负数转为0")

    # 3. 数量字段清洗（amount）：非负整数
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df.loc[df['amount'] < 0, 'amount'] = 0
    # 确保为整数（四舍五入）:.round()：对 'amount' 列的每个数值进行「四舍五入」取整（默认保留 0 位小数，即精确到整数位）。例：3.2 → 3，4.7 → 5，6.5 → 6（Python 中四舍五入遵循「银行家舍入法」，偶数位逢 5 舍，奇数位逢 5 入）。.astype(int)：将四舍五入后的数值（原本可能是 float 类型，如 3.0、5.0）强制转换为整数类型（int），最终 'amount' 列的 dtype 变为 int。
    df['amount'] = df['amount'].round().astype(int)
    print(f"amount字段:负数转为0, 非整数四舍五入")

    # 保存结果
    df.to_csv(output_path, index=False, encoding='gb18030')
    print(f"\n数值型字段清洗完成!最终数据行数:{len(df)}")
    print(f"清洗后数据保存至：{output_path}")

if __name__ == "__main__":
    clean_numeric_fileds(
        input_path="data/cleaned_duplicates_removed.csv",
        output_path="data/cleaned_numeric_fixed.csv"
    )