# 飲料社群粉絲專頁分析網站

這個專案分析了五大人氣飲料品牌（麻古、迷客夏、再睡五分鐘、八曜、一沐日）的社群媒體表現，透過數據挖掘與機器學習方法，找出成功貼文的關鍵因素。

## 功能特點

- 品牌比較：直觀比較不同飲料品牌在社群媒體上的表現指標
- 機器學習分析：運用多種機器學習模型分析貼文熱門度
- 情感分析：分析貼文內容的情感傾向與熱度分數的關係

## 部署到GitHub Pages

本專案已經靜態化，可以直接部署到GitHub Pages：

1. 在GitHub倉庫設置中，找到"Pages"選項
2. 在"Source"部分，選擇"Deploy from a branch"
3. 在"Branch"部分，選擇"main"分支和"/(root)"目錄
4. 點擊"Save"

## 本地開發

使用Python的HTTP服務器：
```bash
python -m http.server
```

然後在瀏覽器中訪問 `http://localhost:8000`

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

## 專案結構

```