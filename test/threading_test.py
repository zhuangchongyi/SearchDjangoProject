import threading


def process_data(data):
    # 处理数据的逻辑
    print("Processing data:", data)


# 假设有一组数据需要处理
data_list = [1, 2, 3, 4, 5]

# 创建线程列表
threads = []

# 遍历数据列表，在每个数据上启动一个线程进行处理
for data in data_list:
    # 创建线程，并将要处理的数据作为参数传递给线程函数
    thread = threading.Thread(target=process_data, args=(data,))
    thread.start()  # 启动线程
    threads.append(thread)  # 将线程添加到列表中

# 等待所有线程完成
for thread in threads:
    thread.join()
