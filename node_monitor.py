import requests
import psutil
import time
import logging

# Настроечке
NODA_CFG = {
    'Region': 'RU',
    'id': '0',
}
SERVER_URL = ""  # Куда отправлять

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("monitor_client")


def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "Noda_RG": NODA_CFG['Region'],
        "Noda_id": NODA_CFG['id'],
        "cpu_percent": cpu,
        "memory_used": mem.used,
        "memory_total": mem.total,
        "disk_used": disk.used,
        "disk_total": disk.total,
        "timestamp": int(time.time())
    }


def send_metrics(metrics):
    try:
        response = requests.post(
            SERVER_URL,
            json=metrics,
            timeout=10
        )
        logger.info(f"Метрики отправлены. Статус: {response.status_code}")
    except Exception as e:
        logger.error(f"Ошибка отправки: {str(e)}")


def main():
    while True:
        metrics = get_metrics()
        cpu = metrics["cpu_percent"]

        #интервал
        if cpu > 75:
            send_metrics(metrics)
            time.sleep(30)
        elif cpu > 50:
            send_metrics(metrics)
            time.sleep(60)
        else:
            send_metrics(metrics)
            time.sleep(300)


if __name__ == "__main__":
    logger.info("Клиент мониторинга запущен")
    main()
