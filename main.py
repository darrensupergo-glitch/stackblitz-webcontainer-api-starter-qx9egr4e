import re
from collections import defaultdict

def process_and_sort_wallets(file_path):
    """
    读取钱包地址文件，根据规则处理并排序。

    规则:
    1. 合并重复地址的备注，按备注后的数字排序，并根据备注数量添加'✅'标识。
    2. 最终结果排序：'✅'数量多的优先，无'✅'的按备注字母升序。
    """
    wallet_remarks = defaultdict(list)

    # --- 步骤 1: 读取文件并按地址分组备注 ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '\t' in line:
                    address, remark = line.split('\t', 1)
                    wallet_remarks[address].append(remark)
    except FileNotFoundError:
        return f"错误: 文件 '{file_path}' 未找到。"
    except Exception as e:
        return f"读取文件时发生错误: {e}"

    processed_lines = []

    # --- 步骤 2: 处理每个地址的备注信息 ---
    for address, remarks in wallet_remarks.items():
        if len(remarks) > 1:
            # 规则 1: 地址有多个备注
            # 定义一个函数，用于提取备注末尾的数字以进行排序
            def get_remark_number(remark):
                match = re.search(r'(\d+)$', remark)
                # 如果找不到数字，则返回一个极大值，使其排在最后
                return int(match.group(1)) if match else float('inf')

            # 按备注后的数字升序排列
            remarks.sort(key=get_remark_number)
            
            # 根据备注数量添加✅标识
            checkmarks = '✅' * len(remarks)
            
            # 合并所有备注为一个字符串
            combined_remarks = f"{checkmarks}{' '.join(remarks)}"
            
            processed_lines.append(f"{address}\t{combined_remarks}")
        elif len(remarks) == 1:
            # 地址只有一个备注，保持原样
            processed_lines.append(f"{address}\t{remarks[0]}")

    # --- 步骤 3: 按权重对所有处理过的行进行排序 ---
    def sort_key(line):
        remark_part = line.split('\t', 1)[1]
        
        # 主要排序依据：✅ 的数量（降序）
        check_count = remark_part.count('✅')
        
        # 次要排序依据：备注的字母顺序（升序）
        # 我们去掉✅来获取纯备注内容进行比较
        remark_text = remark_part.lstrip('✅')
        
        # 返回一个元组，sort会依次比较元组中的元素
        # -check_count 实现降序效果
        return (-check_count, remark_text)

    processed_lines.sort(key=sort_key)

    return "\n".join(processed_lines)

# --- 主程序入口 ---
if __name__ == "__main__":
    # 指定你的文本文件路径
    file_to_process = 'wallets.txt'
    
    # 执行处理和排序
    result = process_and_sort_wallets(file_to_process)
    
    # 打印最终结果
    print(result)
