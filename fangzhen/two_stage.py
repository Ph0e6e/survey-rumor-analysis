import numpy as np  
import matplotlib.pyplot as plt  
import logging  
import time  
from datetime import datetime  

# 设置中文字体（解决Matplotlib绘图中文乱码问题）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def setup_logger():  
    """设置日志处理器"""
    logger = logging.getLogger('RumorModel')  
    logger.setLevel(logging.INFO)  
    
    console_handler = logging.StreamHandler()  
    console_handler.setLevel(logging.INFO)  
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  
    console_handler.setFormatter(formatter)  
    
    if logger.handlers:  
        logger.handlers = []  
    
    logger.addHandler(console_handler)  
    return logger

def generate_scalefree_network(N, m, logger):  
    """生成无标度网络 (BA模型)"""
    logger.info(f"开始生成无标度网络 (N={N}, m={m})")  
    start_time = time.time()  
    
    A = np.zeros((N, N), dtype=int)  
    
    # 初始完全图  
    for i in range(m + 1):  
        for j in range(i + 1, m + 1):  
            A[i, j] = A[j, i] = 1  
    
    # 添加剩余节点  
    for i in range(m + 1, N):  
        if i % 500 == 0:  
            logger.info(f"网络生成进度: {i}/{N} 节点 ({(i/N*100):.1f}%)")  
        
        degrees = np.sum(A, axis=0)  
        probs = degrees / np.sum(degrees)  
        
        connected = 0  
        while connected < m:  
            potential_nodes = np.arange(i)  
            chosen_node = np.random.choice(potential_nodes, p=probs[:i])  
            if A[i, chosen_node] == 0:  
                A[i, chosen_node] = A[chosen_node, i] = 1  
                connected += 1  
    
    elapsed_time = time.time() - start_time  
    logger.info(f"无标度网络生成完成，耗时: {elapsed_time:.2f}秒")  
    return A

def get_influence_range(A, source, layers, logger):  
    """计算特定节点在网络中的多层影响范围"""
    N = A.shape[0]  
    is_influenced = np.zeros(N, dtype=bool)  
    is_influenced[source] = True  
    current_layer = [source]  
    
    for layer in range(layers):  
        next_layer_mask = np.zeros(N, dtype=bool)  
        for node in current_layer:  
            next_layer_mask |= (A[node] > 0)  
        
        next_layer_mask &= ~is_influenced  
        is_influenced |= next_layer_mask  
        current_layer = np.where(next_layer_mask)[0]  
        
    return np.where(is_influenced)[0]

def rumor_spreading_model(N, m, I0, T, Td, D0, official_ratio, official_layers, opinion_layers,   
                         alpha_i, alpha_r, alpha_d, beta_d, delta):  
    """两阶段谣言传播主模型"""
    logger = setup_logger()  
    logger.info("开始运行谣言传播模型")  
    logger.info(f"参数: N={N}, I0={I0}, T={T}, Td={Td}, D0={D0}")  
    
    # 生成网络  
    A = generate_scalefree_network(N, m, logger)  
    
    # 初始化状态: 1=S, 2=I, 3=D, 4=R
    states = np.ones(N, dtype=int)  
    initial_spreaders = np.random.choice(N, I0, replace=False)  
    states[initial_spreaders] = 2  
    
    # 辟谣者类型: 1=官方, 2=意见领袖, 3=被转化者
    debunker_types = np.zeros(N, dtype=int)  
    
    St, It, Dt, Rt = np.zeros(T + 1), np.zeros(T + 1), np.zeros(T + 1), np.zeros(T + 1)  
    
    # 初始比例
    St[0], It[0], Dt[0], Rt[0] = np.sum(states==1)/N, np.sum(states==2)/N, np.sum(states==3)/N, np.sum(states==4)/N  
    
    D0_official = round(D0 * official_ratio)  
    D0_opinion = D0 - D0_official  
    
    simulation_start_time = time.time()  
    for t in range(1, T + 1):  
        iteration_start_time = time.time()  
        
        # Td时刻加入初始辟谣者 (选择度高的节点作为媒体/领袖)
        if t == Td:  
            degrees = np.sum(A, axis=1)  
            sorted_indices = np.argsort(-degrees)  
            available_nodes = sorted_indices[states[sorted_indices] == 1]  
            
            off_deb = available_nodes[:min(D0_official, len(available_nodes))]  
            states[off_deb] = 3  
            debunker_types[off_deb] = 1  
            
            rem_nodes = available_nodes[D0_official:]  
            opi_deb = rem_nodes[:min(D0_opinion, len(rem_nodes))]  
            states[opi_deb] = 3  
            debunker_types[opi_deb] = 2  
            logger.info(f"时间步 {t}: 辟谣者进入 (官方:{len(off_deb)}, 领袖:{len(opi_deb)})")  
        
        new_states = np.copy(states)  
        
        # 状态更新逻辑
        for i in range(N):  
            neighbors = np.where(A[i])[0]  
            
            if t < Td:  # 第一阶段：仅谣言传播
                if states[i] == 1:  # S -> I or R
                    for j in neighbors:  
                        if states[j] == 2:  
                            r = np.random.rand()  
                            if r <= alpha_r: new_states[i] = 4; break  
                            elif r <= alpha_r + alpha_i: new_states[i] = 2; break  
                elif states[i] == 2:  # I -> R
                    for j in neighbors:  
                        if states[j] in [2, 4]:  
                            if np.random.rand() <= delta: new_states[i] = 4; break  
            
            else:  # 第二阶段：加入辟谣干预
                if states[i] == 1:  
                    under_off = any(i in get_influence_range(A, od, official_layers, logger) for od in np.where(debunker_types == 1)[0])
                    under_opi = False
                    if not under_off:
                        under_opi = any(i in get_influence_range(A, ol, opinion_layers, logger) for ol in np.where(debunker_types == 2)[0])
                    
                    l_alpha_r, l_alpha_d = alpha_r, alpha_d  
                    if under_off: l_alpha_r *= 1.5; l_alpha_d *= 1.3  
                    elif under_opi: l_alpha_r *= 1.3; l_alpha_d *= 1.2  
                    
                    for j in neighbors:  
                        if states[j] in [2, 3]:  
                            r = np.random.rand()  
                            if r <= l_alpha_r: new_states[i] = 4; break  
                            elif r <= l_alpha_r + alpha_i: new_states[i] = 2; break  
                            elif r <= l_alpha_r + alpha_i + l_alpha_d: 
                                new_states[i] = 3; debunker_types[i] = 3; break  
                
                elif states[i] == 2:  
                    # 检查是否在干预范围内并调整转化概率 (逻辑同上)
                    under_off = any(i in get_influence_range(A, od, official_layers, logger) for od in np.where(debunker_types == 1)[0])
                    under_opi = False if under_off else any(i in get_influence_range(A, ol, opinion_layers, logger) for ol in np.where(debunker_types == 2)[0])
                    
                    l_beta_d, l_delta = beta_d, delta  
                    if under_off: l_beta_d *= 1.5; l_delta *= 1.3  
                    elif under_opi: l_beta_d *= 1.3; l_delta *= 1.2  
                    
                    for j in neighbors:  
                        if states[j] == 3:  
                            if np.random.rand() <= l_beta_d: new_states[i] = 3; debunker_types[i] = 3; break  
                        elif states[j] in [2, 3, 4]:  
                            if np.random.rand() <= l_delta: new_states[i] = 4; break  
                
                elif states[i] == 3:  
                    if debunker_types[i] > 0:  
                        for j in neighbors:  
                            if states[j] in [2, 3, 4]:  
                                prob = delta if debunker_types[i] == 3 else delta * 0.3
                                if np.random.rand() <= prob: new_states[i] = 4; break  
        
        states = new_states  
        St[t], It[t], Dt[t], Rt[t] = np.sum(states==1)/N, np.sum(states==2)/N, np.sum(states==3)/N, np.sum(states==4)/N  
        
        if t % 5 == 0:
            logger.info(f"时间步 {t}/{T} 完成 | S:{St[t]:.3f} I:{It[t]:.3f} D:{Dt[t]:.3f} R:{Rt[t]:.3f}")  
    
    logger.info(f"模拟完成，总耗时: {time.time() - simulation_start_time:.2f}秒")  
    return St, It, Dt, Rt

def plot_results(St, It, Dt, Rt, T, Td, official_ratio):  
    """绘制传播趋势图"""
    plt.figure(figsize=(10, 6))  
    plt.plot(range(T + 1), St, '-*', label='易感者(S)')  
    plt.plot(range(T + 1), It, '-d', label='谣言传播者(I)')  
    plt.plot(range(T + 1), Dt, '-^', label=f'辟谣者(D)\n官方:{100*official_ratio:.0f}% 领袖:{100*(1-official_ratio):.0f}%')  
    plt.plot(range(T + 1), Rt, '-p', label='已恢复者(R)')  
    plt.axvline(x=Td, color='r', linestyle='--', label='辟谣者进入时间')  
    plt.xlabel('时间')  
    plt.ylabel('比例')  
    plt.title('两阶段谣言传播模型模拟结果')  
    plt.legend(loc='best')  
    plt.grid(True)  
    plt.tight_layout()  
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  
    filename = f'rumor_model_result_{timestamp}.png'
    plt.savefig(filename)  
    print(f"图表已保存为: {filename}")
    plt.show()

if __name__ == "__main__":
    # --- 参数配置 ---
    config = {
        "N": 5000,              # 网络规模
        "m": 2,                 # BA模型参数
        "I0": 10,               # 初始传播者
        "T": 50,                # 总时长
        "Td": 10,               # 辟谣介入时间
        "D0": 10,               # 初始辟谣者数量
        "official_ratio": 0.1,  # 官方媒体占比
        "official_layers": 3,   # 官方影响层数
        "opinion_layers": 2,    # 意见领袖影响层数
        "alpha_i": 0.1,         # S->I 概率
        "alpha_r": 0.8,         # S->R 概率
        "alpha_d": 0.1,         # S->D 概率
        "beta_d": 0.6,          # I->D 概率
        "delta": 0.5            # 恢复概率
    }

    # --- 运行模拟 ---
    S, I, D, R = rumor_spreading_model(**config)

    # --- 绘图 ---
    plot_results(S, I, D, R, config["T"], config["Td"], config["official_ratio"])