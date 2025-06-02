# Node-Monitor
Скрипт для мониторинга состояния нод, отправляющий состояние на сервер


Удобно, если управляете кластерами серверов/нодов

NODA_CFG = {
    'Region': 'RU',
    'id': '0',
} -> кфг ноды
SERVER_URL = "" -> адрес куда мы отправляем 

С помощью библиотеки psutil мониторит состояние, отправляет вот такие метрики:
        "Noda_RG": NODA_CFG['Region'],
        "Noda_id": NODA_CFG['id'],
        "cpu_percent": cpu,
        "memory_used": mem.used,
        "memory_total": mem.total,
        "disk_used": disk.used,
        "disk_total": disk.total,
        "timestamp": int(time.time())


Частота отправки:
        if cpu > 75:
            send_metrics(metrics)
            time.sleep(30)
        elif cpu > 50:
            send_metrics(metrics)
            time.sleep(60)
        else:
            send_metrics(metrics)
            time.sleep(300)



Как получаем данные на вход?

Разворачиваем на мейн машине сервер (fast api, django, flask) и делаем эндпоинт SERVER_URL

Как вариант определяем класс
from pydantic import BaseModel

class NodeMetrics(BaseModel):
    """Модель для метрик от нод"""
    Noda_RG: str
    Noda_id: str
    cpu_percent: float
    memory_used: int
    memory_total: int
    disk_used: int
    disk_total: int
    timestamp: int

и делаем эндпоинт
@app.post("/apiv1/metrics")
async def receive_metrics(metrics: NodeMetrics):
    """Прием метрик от нод"""
    logger.info(f"Метрики от {metrics.Noda_id} (регион {metrics.Noda_RG}): CPU={metrics.cpu_percent}%") <- тут пишем логику работы с метриками
    return {"status": "received"}
