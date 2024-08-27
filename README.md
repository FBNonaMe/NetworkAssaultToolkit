# Network Assault Toolkit

**Network Assault Toolkit (NAT)** — это инструмент для тестирования нагрузки сети и выполнения атак уровня 7 (HTTP). Он поддерживает множество методов атаки и тестирования нагрузки, включая флуудинг GET/POST запросами, обход Cloudflare и атаки с использованием UDP и TCP.

## Установка

Для использования этого инструмента вам понадобятся Python 3.7+ и следующие зависимости:

```bash
pip install requests cloudscraper
python NetworkAssaultToolkit.py <method> <url> [--port PORT] [--delay DELAY] [--threads THREADS] [--duration DURATION] [--payload_size PAYLOAD_SIZE] [--connections_per_thread CONNECTIONS_PER_THREAD] [--udp_threads UDP_THREADS] [--tcp_workers TCP_WORKERS]

Параметры

    method: Метод атаки или тестирования (один из следующих):
        GET_FLOOD
        POST_FLOOD
        BYPASS_OVH
        RANDOM_HEX
        STOMP
        STRESS
        CLOUDFLARE_BYPASS
        CLOUDFLARE_UAM_BYPASS
        UDP_FLOOD
        TCP_TEST

    url: Целевой URL или IP-адрес.

    --port PORT: Номер порта для целевого сервера (по умолчанию: 80).

    --delay DELAY: Задержка между запросами в секундах (по умолчанию: 0.1).

    --threads THREADS: Количество потоков (по умолчанию: 10).

    --duration DURATION: Продолжительность TCP теста в секундах (требуется для метода TCP_TEST).

    --payload_size PAYLOAD_SIZE: Размер полезной нагрузки в байтах для TCP теста (требуется для метода TCP_TEST).

    --connections_per_thread CONNECTIONS_PER_THREAD: Количество TCP соединений на поток (по умолчанию: 100).

    --udp_threads UDP_THREADS: Количество потоков для UDP атаки (по умолчанию: 500).

    --tcp_workers TCP_WORKERS: Количество процессов для TCP тестирования (по умолчанию: 100).

Примеры использования

    GET Flood Attack:

    bash

python script.py GET_FLOOD http://example.com --port 80 --delay 0.2 --threads 50

UDP Flood Attack:

bash

python script.py UDP_FLOOD 192.168.1.1 --port 1234 --payload_size 7812500000 --udp_threads 500

TCP Load Test:

bash

    python script.py TCP_TEST 192.168.1.1 --port 1234 --duration 60 --payload_size 1024 --tcp_workers 100 --connections_per_thread 100

Логирование

Логирование происходит в консоль с использованием модуля logging. Информация о запросах и ошибках будет отображаться в реальном времени.
Предупреждения

    Используйте инструмент ответственно. Данный скрипт предназначен для тестирования и анализа. Не используйте его для несанкционированных атак.
    Законодательство. Убедитесь, что вы имеете разрешение на выполнение тестов на целевых серверах.

Автор

Проект разработан @mvddarkovich.
