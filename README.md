<!-- -*- coding: utf-8 -*- -->
# pandas-csv-data-cleaning
基于Pandas实现电商用户行为数据（CSV/Excel）的基础清洗，包含缺失值处理、时间格式转换、编码映射、业务逻辑校验等核心功能。


## 项目结构

<details>
<summary>点击展开/折叠环境依赖信息</summary>

```text
pandas-csv-data-cleaning/
├── data/
│ ├── cleaned_duplicates_removed.csv
│ ├── cleaned_missing_handled.csv
│ ├── cleaned_numeric_fixed.csv
│ ├── cleaned_time_standardized.csv
│ ├── cleaned_user_behavior_final.csv
│ └── UserBehavior--1.csv
├── scripts/
│ ├── clean_numeric_fields.py
│ ├── comprehensive_cleaning.py
│ ├── handle_missing_values.py
│ ├── remove_duplicates.py
│ └── standardize_time_format.py
└── README.md
```

<details>

## 📋 数据说明

<details>
<summary>点击展开/折叠环境依赖信息</summary>

原始数据`UserBehavior--1.csv`是电商用户行为数据，包含11个字段：

| 字段名        | 含义                   | 数据类型  |
|--------------|-----------------------|----------|
| user_id      | 用户唯一ID             | 整数      |
| goods_id     | 商品唯一ID             | 整数      |
| category_id  | 商品分类ID（0表示无分类）| 整数      |
| behavior     | 用户行为（PV/BUY）     | 字符串     |
| timestamp    | 行为时间戳（秒级）      | 整数       |
| sex          | 用户性别（0/1）        | 整数       |
| address      | 用户所在城市           | 字符串     |
| device       | 访问设备              | 字符串     |
| price        | 商品单价              | 浮点数     |
| amount       | 购买数量              | 整数       |
| comment      | 用户评论              | 字符串     |

</details>

## 🛠️ 环境依赖

<details>
<summary>点击展开/折叠环境依赖信息</summary>

需要安装Python 3.7+及以下库：
```bash
pip install pandas numpy
```

</details>


## 🚀 使用方法

<details>
<summary>点击展开/折叠使用方法</summary>

### 方式 1：分步清洗（适合调试）
先将原始数据UserBehavior--1.csv放入data/目录
```bash
# 进入scripts目录
cd scripts
# 1. 处理缺失值
python handle_missing_values.py
# 2. 处理重复值
python remove_duplicates.py
# 3. 清洗数值字段
python clean_numeric_fields.py
# 4. 标准化时间格式
python standardize_time_format.py
```
每一步的结果会保存在data/目录下（以cleaned_开头）

### 方式 2：一键综合清洗（适合直接使用）
执行综合脚本，自动完成所有清洗步骤：
```bash
cd scripts
python comprehensive_cleaning.py
```

</details>

## ⚙️ 清洗核心功能

<details>
<summary>点击展开/折叠清洗功能说明</summary>

### 缺失值处理
- 核心字段（user_id/goods_id 等）缺失的记录直接删除
- 数值字段（price/amount）缺失用 0 填充，category_id 缺失用 0 标记
- 字符字段（address/device）缺失用 "未知" 填充

### 重复值处理
- 删除完全重复的记录
- 基于 "用户 ID + 商品 ID + 行为 + 时间戳" 删除逻辑重复记录

### 数值字段清洗
- ID 字段保留正整数，过滤异常值
- 价格 / 数量字段过滤负数，异常大值用 99 分位数截断

### 时间格式标准化
- 秒级时间戳转为YYYY-MM-DD HH:MM:SS格式
- 拆分出日期、小时、星期字段，便于后续分析

</details>