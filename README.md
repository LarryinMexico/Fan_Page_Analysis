# 飲料社群粉絲專頁分析

這是一個分析飲料品牌社群媒體表現的網站，使用靜態頁面實現，可部署在 GitHub Pages 上。

## 專案功能

- 分析五大人氣飲料品牌（麻古、迷客夏、再睡五分鐘、八曜、一沐日）的社群媒體表現
- 提供品牌比較分析，包括互動量、互動率等指標
- 視覺化分析各品牌的貼文效果
- 提供個別品牌的詳細分析頁面

## 技術架構

- 前端：HTML, CSS, JavaScript
- 資料視覺化：Plotly.js
- 靜態資料：JSON 格式
- 部署：GitHub Pages

## 本地開發

1. 克隆專案：
   ```
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. 安裝依賴（如果需要）：
   ```
   pip install -r requirements.txt
   ```

3. 生成靜態數據：
   ```
   python generate_static_data.py
   ```

4. 啟動本地伺服器：
   ```
   python -m http.server
   ```

5. 在瀏覽器中訪問：`http://localhost:8000`

## 部署到 GitHub Pages

1. Fork 或克隆此專案
2. 啟用 GitHub Pages：
   - 在專案設置中，找到 GitHub Pages 部分
   - 選擇 `gh-pages` 分支作為來源
   - 保存設置

3. 推送更改到 `main` 分支，GitHub Actions 將自動部署到 `gh-pages` 分支

## 資料來源

本專案使用的數據來自於各飲料品牌的公開社群媒體頁面，經過收集和處理後用於分析。

## 專案結構

```
/
├── index.html             # 入口文件
├── static/                # 靜態資源目錄
│   ├── css/               # 樣式文件
│   ├── js/                # JavaScript 文件
│   ├── data/              # 靜態數據文件
│   │   ├── brands.json    # 品牌列表
│   │   ├── brands/        # 各品牌詳細數據
│   │   ├── comparison.json# 品牌比較數據
│   │   └── ...
│   ├── index.html         # 首頁
│   ├── analysis.html      # 品牌比較頁面
│   ├── visualization.html # 視覺化分析頁面
│   └── brand_detail.html  # 品牌詳情頁面
├── generate_static_data.py# 靜態數據生成腳本
├── data/                  # 原始數據目錄
│   └── *_processed.csv    # 處理過的CSV數據文件
└── .github/workflows/     # GitHub Actions 工作流程
    └── deploy.yml         # 部署工作流程
```

## 授權

本專案僅供學術研究和教育目的使用。 