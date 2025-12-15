# HW4 — Настройка алертинга в Grafana при нарушении SLO

---

## Цель работы

- Развернуть систему наблюдаемости (Prometheus + Grafana)
- Определить SLO для ML-сервиса
- Настроить алерт при нарушении SLO
- Проверить корректность срабатывания алерта

---

## Стек технологий

- Python 3.11
- FastAPI
- Prometheus
- Grafana
- Docker / Docker Compose

---

## Определение SLO

**Service Level Objective (SLO):**

> p95 latency инференса модели должна быть **меньше 1 секунды**

---

## Используемая метрика

В сервисе реализована Prometheus-метрика типа **Histogram**:

```text
prediction_latency_seconds
````

Метрика используется для расчёта p95 latency с помощью PromQL:

```promql
histogram_quantile(
  0.95,
  sum(rate(prediction_latency_seconds_bucket[5m])) by (le)
)
```

---

## Alert rule

Алерт срабатывает, если:

* p95 latency > **1 секунды**
* условие сохраняется более **1 минуты**
* проверка выполняется **каждую минуту**

Алерт настроен через **Grafana UI** с использованием Unified Alerting.

---

## Grafana Dashboard

В Grafana создан дашборд:

* отображает p95 latency инференса модели
* использует Prometheus как источник данных

Дашборд был создан через UI и экспортирован в JSON.

Файл:

```text
grafana/dashboard.json
```

---

## Скриншоты

Скриншоты, подтверждающие корректную работу системы, находятся в папке:

```text
screenshots/
```

Включают:

* Grafana dashboard с графиком p95 latency
* Alert rule в состоянии **Firing**
* Prometheus targets со статусом **UP**

---

## Как запустить проект

### 1. Запуск Prometheus и Grafana

```bash
docker compose up -d
```

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

---

### 2. Запуск ML-сервиса

Активировать виртуальное окружение и запустить сервис:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

### 3. Генерация нагрузки (для проверки алерта)

```powershell
1..30 | % { iwr "http://localhost:8000/predict?delay=2" -UseBasicParsing | Out-Null }
```

После этого алерт переходит в состояние **Firing**.

---

##  Структура репозитория

```text
MLOPS_HW4_DATA/
├── docker-compose.yml
├── prometheus.yml
├── src/
│   └── main.py
├── grafana/
│   └── dashboard.json
├── screenshots/
│   ├── dashboard.png
│   ├── grafana_alert.png
│   ├── grafana_alerts.png
│   └── prometheus.png
├── venvhw4/
└── README.md
```



