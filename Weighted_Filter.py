# 假設準確率
accuracy_A = 0.9  # 演算法 A 的準確率
accuracy_B = 0.8  # 演算法 B 的準確率
accuracy_C = 0.7  # 演算法 C 的準確率

# 在"這個時間點附近"(or 任何其他判斷依據)，有算出發生地震的演算法
EventTriggerTime = "filename, time"

# 在這個時間點有一筆還是多筆資料
D = '在這個時間點只有一筆資料'
E = '在這個時間點有多筆資料'

# 假設當前的資料狀態
current_data_status = D  # 可以更改為 E 來測試

# 判斷有一筆還是多筆資料
if current_data_status == D:
    # 只有一筆資料的處理
    EventCombination = "A"  # 假設這是當前的事件組合

    if EventCombination == "A":
        print(f"只能相信 A")
    elif EventCombination == "B":
        print(f"只能相信 B")
    elif EventCombination == "C":
        print(f"只能相信 C")
    elif EventCombination == "AB":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    elif EventCombination == "AC":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    elif EventCombination == "BC":
        print(f"相信 B 因為 B 準確率最高 or 其他判斷標準")
    elif EventCombination == "ABC":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    else:
        print(f"error")

elif current_data_status == E:
    # 多筆資料的處理
    EventCombination = "AB"  # 假設這是當前的事件組合

    if EventCombination == "A":
        print(f"只能相信 A")
    elif EventCombination == "B":
        print(f"只能相信 B")
    elif EventCombination == "C":
        print(f"只能相信 C")
    elif EventCombination == "AB":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    elif EventCombination == "AC":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    elif EventCombination == "BC":
        print(f"相信 B 因為 B 準確率最高 or 其他判斷標準")
    elif EventCombination == "ABC":
        print(f"相信 A 因為 A 準確率最高 or 其他判斷標準")
    else:
        print(f"error")

else:
    print("沒有任何地震資料")
