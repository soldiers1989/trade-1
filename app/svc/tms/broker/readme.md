# 模块说明
    模拟经纪商服务，提供模拟交易服务和仿真交易服务
    模拟服务：
        7*24小时，以一定的概率成交，不涉及当前的市场行情
    仿真服务
        交易时间、行情同真实市场行情

# 服务启动
## 模拟服务模式
    命令：
        broker.service.start(<port>, mode=mock)
    示例：
        broker.service.start(8080, mode=mock)
    
## 仿真服务模式
    命令：
        broker.service.start(<port>, mode=simulation)
    示例：
        broker.service.start(8080, mode=simulation)
