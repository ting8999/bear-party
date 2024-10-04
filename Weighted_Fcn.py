def Weighted_Fcn(data, weights):
    results = []
    
    for entry in data:
        # 取得該時間段的數據
        binary_data = entry['value']
        
        # 計算加權和
        weighted_sum = sum(w * d for w, d in zip(weights, binary_data))
        
        # 根據加權和決定結果
        if weighted_sum >= sum(weights) / 2:
            decision = 1
        else:
            decision = 0
        
        # 儲存結果，確保正確使用 entry 中的值
        results.append({
            "filename": entry['filename'],  # 使用 entry 中的 filename
            "time_abs": entry['time_abs'],  # 使用 entry 中的 time_abs
            "time_rel": entry['time_rel'],   # 使用 entry 中的 time_rel
            "decision": decision              # 儲存決策
        })
    
    return results
