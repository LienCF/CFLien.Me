---
title: "如何使用 Docker Compose 自架 n8n 自動化工作流程平台"
date: 2025-06-26T22:45:00+08:00
draft: false
author: "ChihFeng Lien"
description: "完整教學如何使用 Docker Compose 在自己的伺服器上架設 n8n 自動化工作流程平台，包含 PostgreSQL 資料庫設定、反向代理、SSL 憑證等"
tags: ["n8n", "Docker", "Docker Compose", "自動化", "工作流程", "self-hosting"]
categories: ["tech"]
---

## 什麼是 n8n？

n8n 是一個開源的工作流程自動化平台，類似於 Zapier 或 Microsoft Power Automate，但可以完全自主託管。它提供了視覺化的工作流程編輯器，讓你可以輕鬆連接不同的服務和 API，自動化日常工作。

## 為什麼要自架 n8n？

- **完全控制**：你的資料完全在自己的伺服器上
- **無限制**：沒有工作流程數量或執行次數限制
- **成本效益**：比付費版本更經濟
- **自訂性**：可以安裝自訂節點和功能
- **隱私**：敏感資料不會傳送到第三方

## 準備工作

### 系統需求

- 一台 Linux 伺服器（推薦 2GB RAM 以上）
- Docker 和 Docker Compose
- 網域名稱（選用，但建議）

### 安裝 Docker 和 Docker Compose

```bash
# 移除舊版本（如果有）
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg -y; done

# 更新套件列表並安裝相依套件
sudo apt-get update
sudo apt-get install ca-certificates curl -y

# 新增 Docker 官方 GPG 金鑰
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 新增 Docker 官方儲存庫
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新套件列表並安裝 Docker 和 Docker Compose
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 將使用者新增到 docker 群組
sudo usermod -aG docker $USER

# 驗證安裝
docker --version
docker compose version

# 重新登入以套用群組變更（或重新啟動終端）
newgrp docker
```

## 建立 Docker Compose 設定

### 1. 建立專案目錄

```bash
mkdir n8n-docker
cd n8n-docker
```

### 2. 建立目錄結構

```bash
mkdir -p {data,postgres-data,caddy/data,caddy/config}
```

### 3. 建立 Docker Compose 檔案

建立 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=your-strong-password
      - POSTGRES_DB=n8n
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - N8N_DATABASE_TYPE=postgresdb
      - N8N_DATABASE_HOST=postgres
      - N8N_DATABASE_PORT=5432
      - N8N_DATABASE_NAME=n8n
      - N8N_DATABASE_USER=n8n
      - N8N_DATABASE_PASSWORD=your-strong-password
      - N8N_HOST=your-domain.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://your-domain.com/
      - GENERIC_TIMEZONE=Asia/Taipei
    ports:
      - "5678:5678"
    volumes:
      - ./data:/home/node/.n8n
    command: n8n start

  caddy:
    image: caddy:2
    container_name: n8n-caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./caddy/data:/data
      - ./caddy/config:/config
```

### 4. 建立 Caddyfile（反向代理和 SSL）

建立 `Caddyfile`：

```
your-domain.com {
    reverse_proxy n8n:5678
    
    # 增強安全性設定
    header {
        # 移除伺服器識別
        -Server
        
        # 安全標頭
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Referrer-Policy strict-origin-when-cross-origin
        
        # HSTS
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    }
    
    # 記錄存取日誌
    log {
        output file /var/log/caddy/access.log {
            roll_size 100mb
            roll_keep 5
        }
    }
}
```

## 啟動 n8n

### 1. 設定環境變數

建立 `.env` 檔案（選用）：

```bash
# 資料庫設定
POSTGRES_PASSWORD=your-very-strong-password-here
N8N_DATABASE_PASSWORD=your-very-strong-password-here

# n8n 設定
N8N_HOST=your-domain.com
WEBHOOK_URL=https://your-domain.com/

# 時區設定
GENERIC_TIMEZONE=Asia/Taipei
```

### 2. 更新 docker-compose.yml 使用環境變數

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - ./postgres-data:/var/lib/postgresql/data

  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    depends_on:
      - postgres
    environment:
      - N8N_DATABASE_TYPE=postgresdb
      - N8N_DATABASE_HOST=postgres
      - N8N_DATABASE_PORT=5432
      - N8N_DATABASE_NAME=n8n
      - N8N_DATABASE_USER=n8n
      - N8N_DATABASE_PASSWORD=${N8N_DATABASE_PASSWORD}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=${WEBHOOK_URL}
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE}
    ports:
      - "5678:5678"
    volumes:
      - ./data:/home/node/.n8n
```

### 3. 啟動服務

```bash
# 檢查設定檔語法
docker compose config

# 啟動所有服務
docker compose up -d

# 查看服務狀態
docker compose ps

# 查看日誌
docker compose logs -f n8n
```

## 初始設定

### 1. 訪問 n8n 界面

開啟瀏覽器前往 `https://your-domain.com`，你應該會看到 n8n 的設定頁面。

### 2. 建立管理員帳號

填寫以下資訊：
- Email
- 姓名
- 密碼

### 3. 設定工作區名稱

為你的 n8n 實例設定一個有意義的名稱。

## 進階設定

### 1. 啟用執行資料持久化

在 `docker-compose.yml` 中新增環境變數：

```yaml
environment:
  - EXECUTIONS_DATA_SAVE_ON_ERROR=all
  - EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
  - EXECUTIONS_DATA_MAX_AGE=168  # 7天
```

### 2. 設定 SMTP 郵件通知

```yaml
environment:
  - N8N_EMAIL_MODE=smtp
  - N8N_SMTP_HOST=smtp.gmail.com
  - N8N_SMTP_PORT=587
  - N8N_SMTP_USER=your-email@gmail.com
  - N8N_SMTP_PASS=your-app-password
  - N8N_SMTP_SENDER=your-email@gmail.com
```

### 3. 增加記憶體限制

如果需要處理大量資料：

```yaml
environment:
  - NODE_OPTIONS=--max-old-space-size=4096
```

### 4. 設定備份腳本

建立 `backup.sh`：

```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"

# 建立備份目錄
mkdir -p $BACKUP_DIR

# 備份 PostgreSQL 資料庫
docker compose exec -T postgres pg_dump -U n8n n8n > "$BACKUP_DIR/n8n_db_$DATE.sql"

# 備份 n8n 資料目錄
tar -czf "$BACKUP_DIR/n8n_data_$DATE.tar.gz" ./data

# 保留最近 7 天的備份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

設定定期備份：

```bash
# 讓腳本可執行
chmod +x backup.sh

# 新增到 crontab（每天凌晨 2 點執行）
echo "0 2 * * * /path/to/n8n-docker/backup.sh" | crontab -
```

## 監控和維護

### 1. 查看系統資源使用

```bash
# 查看容器資源使用情況
docker stats

# 查看磁碟使用情況
du -sh ./data ./postgres-data
```

### 2. 更新 n8n

```bash
# 拉取最新映像檔
docker compose pull

# 重新啟動服務
docker compose up -d

# 清理舊映像檔
docker image prune -f
```

### 3. 日誌管理

設定日誌輪轉以避免磁碟空間不足：

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 安全性考量

### 1. 防火牆設定

```bash
# 只允許 HTTP/HTTPS 和 SSH
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. 定期更新

```bash
# 系統更新
sudo apt update && sudo apt upgrade -y

# Docker 映像檔更新
docker compose pull && docker compose up -d
```

### 3. 強化 PostgreSQL

在 `docker-compose.yml` 中新增：

```yaml
postgres:
  command: >
    postgres
    -c shared_preload_libraries=pg_stat_statements
    -c max_connections=200
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
    -c maintenance_work_mem=64MB
    -c checkpoint_completion_target=0.9
    -c wal_buffers=16MB
    -c default_statistics_target=100
```

## 故障排除

### 常見問題

1. **n8n 無法連接到資料庫**
   ```bash
   # 檢查 PostgreSQL 是否正常運行
   docker compose logs postgres
   
   # 檢查連接字串是否正確
   docker compose exec postgres psql -U n8n -d n8n
   ```

2. **SSL 憑證問題**
   ```bash
   # 檢查 Caddy 日誌
   docker compose logs caddy
   
   # 手動重新載入 Caddy 設定
   docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
   ```

3. **記憶體不足**
   ```bash
   # 增加 swap 空間
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## 結語

使用 Docker Compose 自架 n8n 讓你能夠完全控制自己的自動化工作流程平台。記得定期備份資料、更新系統，並監控服務狀態。透過 n8n，你可以輕鬆整合各種服務，提升工作效率。

如果在設定過程中遇到問題，可以參考 [n8n 官方文件](https://docs.n8n.io/) 或在社群中尋求協助。

---

*想了解更多自架服務相關內容，歡迎關注我的部落格後續文章！* 