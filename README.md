# 飲料社群粉絲專頁分析網站

這個專案是一個基於Flask的網頁應用，用於展示對飲料品牌社群粉絲專頁的數據分析和視覺化結果。

## 專案結構

```
ML_final/
├── notebooks/        # Jupyter筆記本文件
├── data/             # 處理過的數據和分析結果
├── static/
│   ├── css/          # 樣式文件
│   ├── js/           # JavaScript文件
│   └── images/       # 圖像資源
├── templates/        # HTML頁面
├── app.py            # Flask應用入口文件
└── requirements.txt  # 項目依賴
```

## 如何運行

1. 安裝依賴：

```bash
pip install -r requirements.txt
```

2. 運行Flask應用：

```bash
python app.py
```

3. 在瀏覽器中訪問：`http://127.0.0.1:5000/`

## 整合Jupyter筆記本

本專案整合了以下Jupyter筆記本中的分析結果：

- `ML期末視覺化.ipynb` - 主要視覺化分析
- `ML_Final_Project.ipynb` - 最終專案分析

如需整合筆記本中的分析到網頁應用，可以考慮以下方法：

1. **靜態整合**：從筆記本中導出圖表為圖像文件，然後在網頁中顯示。
2. **動態整合**：使用plotly等互動式圖表庫，將分析結果轉換為JSON，在前端渲染。
3. **API整合**：將筆記本中的分析代碼轉換為API端點，前端通過AJAX請求獲取數據。

## 後續開發計劃

1. 將Jupyter筆記本中的分析結果整合到網頁應用中
2. 增加更多互動式圖表
3. 實現實時數據更新功能
4. 增加用戶登錄和數據管理功能 