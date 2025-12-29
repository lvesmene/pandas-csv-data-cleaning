# pandas-csv-data-cleaning
基于Pandas实现电商用户行为数据（CSV/Excel）的基础清洗，包含缺失值处理、时间格式转换、编码映射、业务逻辑校验等核心功能。

## 项目结构

pandas-csv-data-cleaning/
├── data/ # 数据目录
│ ├── UserBehavior--1.csv # 原始电商用户行为数据（76 万 + 条）
│ ├── cleaned_missing_handled.csv # 缺失值处理后的数据
│ ├── cleaned_duplicates_removed.csv # 重复值处理后的数据
│ ├── cleaned_numeric_fixed.csv # 数值字段清洗后的数据
│ ├── cleaned_time_standardized.csv # 时间格式标准化后的数据
│ └── cleaned_user_behavior_final.csv # 最终综合清洗后的数据
├── scripts/ # 清洗脚本目录
│ ├── handle_missing_values.py # 缺失值处理脚本
│ ├── remove_duplicates.py # 重复值处理脚本
│ ├── clean_numeric_fields.py # 数值字段清洗脚本
│ ├── standardize_time_format.py # 时间格式标准化脚本
│ └── comprehensive_cleaning.py # 综合清洗脚本（一键完成所有步骤）
└── README.md # 项目说明文档


## 📋 数据说明
原始数据`UserBehavior--1.csv`是电商用户行为数据，包含11个字段：
| 字段名       | 含义               | 数据类型   |
|--------------|--------------------|------------|
| user_id      | 用户唯一ID         | 整数       |
| goods_id     | 商品唯一ID         | 整数       |
| category_id  | 商品分类ID         | 整数       |
| behavior     | 用户行为（PV/BUY）  | 字符串     |
| timestamp    | 行为时间戳（秒级）   | 整数       |
| sex          | 用户性别（0/1）     | 整数       |
| address      | 用户所在城市        | 字符串     |
| device       | 访问设备           | 字符串     |
| price        | 商品单价           | 浮点数     |
| amount       | 购买数量           | 整数       |
| comment      | 用户评论           | 字符串     |


## 🛠️ 环境依赖
需要安装Python 3.7+及以下库：
```bash
pip install pandas numpy


使用方法
方式 1：分步清洗（适合调试）
先将原始数据UserBehavior--1.csv放入data/目录
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

每一步的结果会保存在data/目录下（以cleaned_开头）

方式 2：一键综合清洗（适合直接使用）
执行综合脚本，自动完成所有清洗步骤：
cd scripts
python comprehensive_cleaning.py

清洗核心功能
缺失值处理：
核心字段（user_id/goods_id 等）缺失的记录直接删除
数值字段（price/amount）缺失用 0 填充，category_id 缺失用 0 标记
字符字段（address/device）缺失用 “未知” 填充
重复值处理：
删除完全重复的记录
基于 “用户 ID + 商品 ID + 行为 + 时间戳” 删除逻辑重复记录
数值字段清洗：
ID 字段保留正整数，过滤异常值
价格 / 数量字段过滤负数，异常大值用 99 分位数截断
时间格式标准化：
秒级时间戳转为YYYY-MM-DD HH:MM:SS格式
拆分出日期、小时、星期字段，便于后续分析