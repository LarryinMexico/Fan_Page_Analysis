# 飲料社群粉絲專頁分析

這個專案分析了五大人氣飲料品牌（麻古、迷客夏、再睡五分鐘、八曜、一沐日）的社群媒體表現，透過數據挖掘與機器學習方法，找出成功貼文的關鍵因素。

## 功能特點

- 品牌比較：直觀比較不同飲料品牌在社群媒體上的表現指標
- 機器學習分析：運用多種機器學習模型分析貼文熱門度
- 情感分析：分析貼文內容的情感傾向與熱度分數的關係

## 專案結構

- `index.html`: 網站首頁
- `analysis.html`: 品牌比較分析頁面
- `visualization.html`: 視覺化分析頁面
- `brand_detail.html`: 品牌詳細資訊頁面
- `static/`: 靜態資源目錄
  - `css/`: 樣式表
  - `js/`: JavaScript 檔案
  - `data/`: 資料檔案
  - `images/`: 圖片資源
- `data/`: 原始資料檔案

## 本地運行

1. 克隆此專案到本地
2. 使用任何HTTP伺服器提供服務，例如:
   - Python: `python -m http.server`
   - Node.js: `npx serve`
   - 或使用VS Code的Live Server擴展

## GitHub Pages 部署

### 部署步驟

1. 確保專案根目錄中有 `.nojekyll` 檔案（用於禁用Jekyll處理）
2. 在GitHub儲存庫設置中，啟用GitHub Pages:
   - 前往儲存庫設置 > Pages
   - Source選擇 "Deploy from a branch"
   - Branch選擇 "main" 和 "/ (root)"
   - 點擊 "Save"

### 常見問題排除

如果遇到部署問題:

1. 確保所有檔案路徑使用相對路徑，以 `./` 開頭
2. 檢查所有資源檔案的大小寫是否正確（GitHub Pages 對大小寫敏感）
3. 確保 `.nojekyll` 檔案存在於儲存庫根目錄
4. 檢查 `_config.yml` 和其他配置檔案是否有衝突

## 聯絡方式

有任何問題或建議，請開啟Issue或聯絡專案維護者。

## 數據來源

專案使用了以下飲料品牌的Facebook粉絲專頁數據：
- 麻古茶坊
- 迷客夏
- 再睡五分鐘
- 八曜和茶
- 一沐日

## 技術棧

- 前端：HTML, CSS, JavaScript
- 數據視覺化：Plotly.js
- 數據處理：Python, Pandas
- 機器學習：Scikit-learn

## 授權

本專案僅供學術研究和教育目的使用。