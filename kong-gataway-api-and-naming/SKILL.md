# Kong Gateway — Skill: Именование и Admin API

## Контекст применения

Этот скил применяется когда нужно:
- Создать или именовать объекты Kong (Services, Routes, Upstreams, Consumers)
- Выполнить операции через Kong Admin API
- Сгенерировать конфигурацию для decK или Terraform

---

## Часть 1: Правила именования

### Шаг 0: Определить топологию инстансов

Перед именованием **обязательно** выяснить:

```
Сколько Kong-инстансов в инфраструктуре?

A) Один инстанс на одну среду (или только prod):
   → суффикс среды в именах НЕ используется
   → среда фиксируется только в tags: env:prod

B) Один общий инстанс на несколько сред:
   → суффикс среды ОБЯЗАТЕЛЕН: {name}-{env}
   → tags также содержат env:{value}

C) Несколько инстансов, по одному на среду:
   → суффикс среды НЕ используется (инстанс — контекст среды)
   → среда фиксируется только в tags: env:{value}
```

---

### Services

**Принцип:** имя Kong-сервиса должно совпадать с именем микросервиса.

```
Микросервис имеет одно назначение (1 микросервис = 1 домен)?
  → {microservice-name}
  → Пример: user-service, order-service, payment-service

Один бизнес-домен разбит на несколько микросервисов?
  → {domain}-{subdomain}-service
  → Пример: order-processing-service, order-history-service
```

**Правила формата:**
- только kebab-case (строчные буквы + дефис)
- без подчёркиваний, без спецсимволов
- суффикс `-service` сохраняется из имени микросервиса

```yaml
# ✅ Правильно (prod-only инстанс)
- name: user-service
- name: order-service
- name: order-processing-service

# ❌ Неправильно
- name: UserService          # не camelCase
- name: user_service         # не underscore
- name: identity-user-service  # выдуманный домен поверх сервиса
- name: user-service-prod    # среда в имени при prod-only инстансе
```

---

### Routes

```
Количество роутов на сервис = 1?
  → name роута = name сервиса (повторяет имя)
  → суффикс -route НЕ добавляется

Количество роутов на сервис > 1?
  → {service-name}-{descriptor}
  → descriptor: public, internal, admin, legacy, v1, v2
```

```yaml
# Один роут — имя совпадает с сервисом
routes:
  - name: user-service        # ✅
    paths: [/v1/users]

# Несколько роутов — добавляется дескриптор
routes:
  - name: user-service-public    # без авторизации
  - name: user-service-internal  # только внутренняя сеть
  - name: user-service-admin     # для админки
```

---

### Upstreams

```
Формат: {service-name}-upstream
Пример: user-service-upstream, order-service-upstream
```

---

### Consumers

```
Формат: {client-app}-{role или env}
Пример: mobile-app-consumer, backoffice-internal, analytics-reader
```

---

### Tags — обязательный элемент

Теги — основной инструмент фильтрации и организации в Kong.

```yaml
tags:
  - env:prod          # всегда указывать
  - team:backend      # команда-владелец
  - domain:orders     # бизнес-домен
  - managed-by:deck   # инструмент управления
```

---

### Итоговая таблица (prod-only инстанс)

| Объект   | Формат                          | Пример                        |
|----------|----------------------------------|-------------------------------|
| Service  | `{microservice-name}`           | `order-service`               |
| Route    | `{service-name}` или `{service-name}-{descriptor}` | `order-service`, `order-service-admin` |
| Upstream | `{service-name}-upstream`       | `order-service-upstream`      |
| Consumer | `{app}-{role}`                  | `mobile-app-consumer`         |
| Tag      | `key:value`                     | `env:prod`, `team:commerce`   |

---

### Полный пример конфигурации (decK)

```yaml
# Один роут — простой случай
services:
  - name: order-service
    url: http://order-service.internal:8080
    tags: [env:prod, team:commerce, domain:orders]
    routes:
      - name: order-service
        paths: [/v1/orders]
        strip_path: false
        protocols: [http, https]
        tags: [env:prod, team:commerce]

# Несколько роутов — с дескрипторами
services:
  - name: user-service
    url: http://user-service.internal:8080
    tags: [env:prod, team:users, domain:users]
    routes:
      - name: user-service-public
        paths: [/v1/users/register, /v1/users/login]
        protocols: [http, https]
        tags: [env:prod, team:users]
      - name: user-service-internal
        paths: [/internal/users]
        protocols: [http]
        tags: [env:prod, team:users]
```

---

## Часть 2: Kong Admin API

### Базовые сведения

Admin API — это отдельный HTTP-интерфейс управления Kong, **независимый от прокси-трафика**.

```
Admin API URL:  http://<KONG_ADMIN_HOST>:<KONG_ADMIN_PORT>
Proxy URL:      http://<KONG_PROXY_HOST>:<KONG_PROXY_PORT>

Значения по умолчанию:
  Admin API → http://localhost:8001
  Proxy     → http://localhost:8000

Настраивается в kong.conf:
  admin_listen = 0.0.0.0:8001   ← адрес и порт Admin API
  proxy_listen = 0.0.0.0:8000   ← адрес и порт Proxy
```

Во всех примерах ниже `http://localhost:8001` — это placeholder.
**Нужно заменить на реальный адрес Kong Admin API в вашей инфраструктуре.**

Типичные варианты в реальных окружениях:
```
http://kong-admin.internal:8001      # внутренний DNS
http://10.0.1.15:8001                # прямой IP
http://localhost:8001                # локальная разработка
```

> **Важно:** Admin API не должен быть доступен из публичной сети без защиты.

---

### Services

#### Создать сервис

```bash
curl -X POST http://localhost:8001/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service",
    "url": "http://order-service.internal:8080",
    "tags": ["env:prod", "team:commerce"]
  }'
```

#### Получить список сервисов

```bash
curl -X GET http://localhost:8001/services
```

#### Получить конкретный сервис

```bash
# По имени или ID
curl -X GET http://localhost:8001/services/order-service
```

#### Обновить сервис (PATCH — частичное обновление)

```bash
curl -X PATCH http://localhost:8001/services/order-service \
  -H "Content-Type: application/json" \
  -d '{"url": "http://order-service.internal:9090"}'
```

#### Обновить сервис (PUT — полная замена)

```bash
curl -X PUT http://localhost:8001/services/order-service \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service",
    "url": "http://order-service.internal:8080",
    "tags": ["env:prod", "team:commerce"]
  }'
```

#### Удалить сервис

```bash
curl -X DELETE http://localhost:8001/services/order-service
# Ответ: 204 No Content
```

---

### Routes

#### Создать роут (привязан к сервису)

```bash
# Вариант 1: через вложенный endpoint сервиса
curl -X POST http://localhost:8001/services/order-service/routes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service",
    "paths": ["/v1/orders"],
    "protocols": ["http", "https"],
    "strip_path": false
  }'

# Вариант 2: через глобальный endpoint
curl -X POST http://localhost:8001/routes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service",
    "paths": ["/v1/orders"],
    "protocols": ["http", "https"],
    "service": {"name": "order-service"}
  }'
```

#### Получить список роутов сервиса

```bash
curl -X GET http://localhost:8001/services/order-service/routes
```

#### Получить конкретный роут

```bash
curl -X GET http://localhost:8001/routes/order-service
```

#### Обновить роут

```bash
curl -X PATCH http://localhost:8001/routes/order-service \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/v1/orders", "/v2/orders"]}'
```

#### Удалить роут

```bash
curl -X DELETE http://localhost:8001/routes/order-service
# Ответ: 204 No Content
```

---

### Plugins

Плагины — основной механизм расширения Kong. Применяются на разных уровнях:

```
Глобально (все сервисы и роуты)  →  POST /plugins
На сервис                         →  POST /services/{name}/plugins
На роут                           →  POST /routes/{name}/plugins
На consumer                       →  POST /consumers/{name}/plugins
```

Чем уже область применения, тем выше приоритет. Плагин на роут перекрывает плагин на сервис.

#### CRUD-операции над плагинами

```bash
# Добавить плагин на сервис
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "rate-limiting", "config": {"minute": 60, "policy": "local"}}'

# Добавить плагин на роут
curl -X POST http://localhost:8001/routes/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "jwt"}'

# Добавить плагин глобально (применяется ко всем запросам)
curl -X POST http://localhost:8001/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "correlation-id", "config": {"header_name": "X-Request-ID", "generator": "uuid"}}'

# Список плагинов сервиса
curl -X GET http://localhost:8001/services/order-service/plugins

# Список всех плагинов в Kong
curl -X GET http://localhost:8001/plugins

# Обновить конфигурацию плагина (по ID)
curl -X PATCH http://localhost:8001/plugins/{plugin-id} \
  -H "Content-Type: application/json" \
  -d '{"config": {"minute": 100}}'

# Отключить плагин без удаления
curl -X PATCH http://localhost:8001/plugins/{plugin-id} \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'

# Удалить плагин
curl -X DELETE http://localhost:8001/plugins/{plugin-id}
```

---

## Часть 3: Встроенные плагины Kong (OSS)

Все перечисленные плагины входят в **Kong Gateway OSS** и не требуют лицензии Enterprise.

---

### Аутентификация

#### `jwt` — проверка JWT-токенов

Валидирует JWT (HS256/RS256) на уровне gateway. Микросервис получает уже аутентифицированный запрос и не занимается проверкой токенов.

```bash
# 1. Включить плагин на сервис
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "jwt"}'

# 2. Создать consumer
curl -X POST http://localhost:8001/consumers \
  -d "username=mobile-app-consumer"

# 3. Выдать JWT-credentials consumer'у
curl -X POST http://localhost:8001/consumers/mobile-app-consumer/jwt \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "HS256", "key": "mobile-app-key", "secret": "supersecretkey"}'

# Клиент передаёт токен в заголовке:
# Authorization: Bearer <jwt-token>
```

В decK:
```yaml
plugins:
  - name: jwt
    service: order-service
    config:
      key_claim_name: iss
      claims_to_verify: [exp]
```

---

#### `key-auth` — аутентификация по API-ключу

Простейший способ защитить API. Клиент передаёт ключ в заголовке или query-параметре.

```bash
# 1. Включить плагин
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "key-auth", "config": {"key_names": ["X-Api-Key"]}}'

# 2. Создать consumer
curl -X POST http://localhost:8001/consumers \
  -d "username=mobile-app-consumer"

# 3. Выдать API-ключ consumer'у
curl -X POST http://localhost:8001/consumers/mobile-app-consumer/key-auth \
  -d "key=my-secret-api-key"

# Клиент передаёт ключ в заголовке:
# X-Api-Key: my-secret-api-key
```

---

### Контроль трафика

#### `rate-limiting` — ограничение частоты запросов

Защищает upstream от перегрузки. Можно лимитировать по IP, consumer, сервису.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "rate-limiting",
    "config": {
      "minute": 60,
      "hour": 1000,
      "policy": "local",
      "limit_by": "ip"
    }
  }'
```

Параметр `policy`:
- `local` — каждый Kong-узел считает независимо (быстро, но не точно при кластере)
- `redis` — общий счётчик через Redis (точно при кластере)

```yaml
# decK
plugins:
  - name: rate-limiting
    service: order-service
    config:
      minute: 60
      policy: local
      limit_by: consumer   # или: ip, credential, service, header
```

При превышении лимита Kong возвращает `429 Too Many Requests`.

---

#### `request-size-limiting` — ограничение размера запроса

Блокирует запросы с телом больше заданного размера. Защита от DoS.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "request-size-limiting", "config": {"allowed_payload_size": 8}}'
# allowed_payload_size — в мегабайтах
```

---

### Безопасность

#### `cors` — Cross-Origin Resource Sharing

Управляет CORS-заголовками. Нужен если фронтенд обращается к API с другого домена.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "cors",
    "config": {
      "origins": ["https://app.example.com"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "headers": ["Authorization", "Content-Type"],
      "exposed_headers": ["X-Request-ID"],
      "credentials": true,
      "max_age": 3600
    }
  }'
```

Для разработки можно разрешить все источники: `"origins": ["*"]` (не рекомендуется для prod).

---

#### `ip-restriction` — ограничение по IP

Разрешает или запрещает доступ по IP-адресу или CIDR-диапазону.

```bash
# Разрешить только конкретные IP
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "ip-restriction", "config": {"allow": ["10.0.0.0/8", "192.168.1.0/24"]}}'

# Запретить конкретные IP
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "ip-restriction", "config": {"deny": ["1.2.3.4"]}}'
```

---

### Трансформация

#### `request-transformer` — изменение запроса перед upstream

Добавляет, удаляет или изменяет заголовки и параметры запроса до передачи в микросервис.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "request-transformer",
    "config": {
      "add": {"headers": ["X-Internal-Source:kong", "X-Version:v1"]},
      "remove": {"headers": ["X-Forwarded-For"]}
    }
  }'
```

---

#### `response-transformer` — изменение ответа от upstream

Добавляет, удаляет или изменяет заголовки ответа перед отдачей клиенту.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "response-transformer",
    "config": {
      "add": {"headers": ["X-Powered-By:kong"]},
      "remove": {"headers": ["Server"]}
    }
  }'
```

---

### Наблюдаемость

#### `correlation-id` — уникальный ID запроса

Генерирует уникальный ID для каждого запроса и проставляет его в заголовок. Незаменим для трассировки через несколько микросервисов.

```bash
# Рекомендуется добавлять глобально
curl -X POST http://localhost:8001/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "correlation-id",
    "config": {
      "header_name": "X-Request-ID",
      "generator": "uuid",
      "echo_downstream": true
    }
  }'
```

---

#### `prometheus` — метрики для Prometheus

Экспортирует метрики Kong (latency, RPS, upstream health) в формате Prometheus.

```bash
# Включить глобально
curl -X POST http://localhost:8001/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "prometheus",
    "config": {
      "status_code_metrics": true,
      "latency_metrics": true,
      "bandwidth_metrics": true,
      "upstream_health_metrics": true
    }
  }'

# Метрики доступны на Admin API:
# GET http://<KONG_ADMIN_HOST>:8001/metrics
```

---

#### `file-log` — логирование в файл

Записывает данные каждого запроса/ответа в JSON-файл на диске Kong-узла.

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{"name": "file-log", "config": {"path": "/tmp/kong-access.log"}}'
```

---

#### `http-log` — отправка логов на HTTP-endpoint

Отправляет данные запроса POST-запросом на внешний сервис (Logstash, кастомный коллектор).

```bash
curl -X POST http://localhost:8001/services/order-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "http-log",
    "config": {
      "http_endpoint": "http://logstash.internal:5044",
      "method": "POST",
      "timeout": 1000,
      "keepalive": 1000
    }
  }'
```

---

### Сводная таблица встроенных плагинов

| Плагин | Категория | Область применения | Лицензия |
|---|---|---|---|
| `jwt` | Auth | Service, Route | OSS |
| `key-auth` | Auth | Service, Route | OSS |
| `rate-limiting` | Traffic | Service, Route, Global | OSS |
| `request-size-limiting` | Traffic | Service, Route | OSS |
| `cors` | Security | Service, Route | OSS |
| `ip-restriction` | Security | Service, Route | OSS |
| `request-transformer` | Transform | Service, Route | OSS |
| `response-transformer` | Transform | Service, Route | OSS |
| `correlation-id` | Observability | Global (рекомендуется) | OSS |
| `prometheus` | Observability | Global | OSS |
| `file-log` | Logging | Service, Route | OSS |
| `http-log` | Logging | Service, Route | OSS |

---

### Upstreams и Targets

#### Создать Upstream

```bash
curl -X POST http://localhost:8001/upstreams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service-upstream",
    "tags": ["env:prod"]
  }'
```

#### Добавить Target к Upstream

```bash
curl -X POST http://localhost:8001/upstreams/order-service-upstream/targets \
  -H "Content-Type: application/json" \
  -d '{
    "target": "order-service.internal:8080",
    "weight": 100
  }'
```

#### Использовать Upstream в сервисе

```bash
curl -X POST http://localhost:8001/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "order-service",
    "host": "order-service-upstream",
    "port": 80,
    "protocol": "http"
  }'
```

---

### Consumers

#### Создать Consumer

```bash
curl -X POST http://localhost:8001/consumers \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mobile-app-consumer",
    "tags": ["env:prod", "client:mobile"]
  }'
```

---

### Работа с тегами

#### Найти все объекты по тегу

```bash
curl -X GET http://localhost:8001/tags/env:prod
```

#### Фильтрация сервисов по тегу

```bash
curl -X GET "http://localhost:8001/services?tags=team:commerce"
```

---

### Диагностика

#### Проверить статус Kong

```bash
curl -X GET http://localhost:8001/status
```

#### Список всех доступных endpoints

```bash
curl -X GET http://localhost:8001/
```

#### Проверить конкретный объект перед созданием (schema validation)

```bash
curl -X POST http://localhost:8001/schemas/services/validate \
  -H "Content-Type: application/json" \
  -d '{"name": "order-service", "url": "http://order-service.internal:8080"}'
```

---

## Часть 3: HTTP-коды ответов Admin API

| Код | Значение                              |
|-----|----------------------------------------|
| 200 | Успешное чтение/обновление             |
| 201 | Объект создан                          |
| 204 | Объект удалён (тело ответа пустое)     |
| 400 | Ошибка валидации запроса               |
| 404 | Объект не найден                       |
| 409 | Конфликт — объект с таким именем уже существует |

---

## Часть 4: decK — декларативное управление

decK — рекомендуемый инструмент для управления конфигурацией Kong через файлы.

```bash
# Экспортировать текущее состояние
deck gateway dump -o kong.yaml

# Применить конфигурацию
deck gateway sync kong.yaml

# Показать diff без применения
deck gateway diff kong.yaml

# Сбросить до состояния файла
deck gateway reset
```

> При использовании decK имена объектов являются идентификаторами.
> Переименование = удаление + пересоздание объекта.
