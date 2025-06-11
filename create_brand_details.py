import os
import json
import pandas as pd
import hashlib

# 確保靜態數據目錄存在
os.makedirs('static/data', exist_ok=True)

def read_csv_data(brand_name):
    """讀取特定品牌的CSV數據"""
    file_path = os.path.join(os.path.dirname(__file__), 'data', f'{brand_name}_processed.csv')
    data = []
    try:
        # 嘗試使用不同的編碼和分隔符讀取CSV
        encodings = ['utf-8', 'utf-8-sig', 'cp950', 'big5']
        separators = [',', '\t', ';']
        
        df = None
        for encoding in encodings:
            for sep in separators:
                try:
                    df = pd.read_csv(file_path, encoding=encoding, sep=sep)
                    # 如果能夠成功讀取且包含必要的列，則停止嘗試
                    if df is not None and len(df) > 0:
                        if 'content' in df.columns and 'like' in df.columns:
                            break
                except Exception as e:
                    print(f"嘗試使用編碼 {encoding} 和分隔符 {sep} 讀取失敗: {e}")
                    continue
            if df is not None and len(df) > 0:
                break
        
        if df is None or len(df) == 0:
            raise Exception(f"無法讀取CSV文件: {file_path}")
        
        # 確保數值型態正確
        for key in ['like', 'comment', 'forward', 'share']:
            if key in df.columns:
                df[key] = pd.to_numeric(df[key], errors='coerce').fillna(0).astype(int)
            else:
                df[key] = 0
        
        # 轉換為字典列表
        for _, row in df.iterrows():
            item = row.to_dict()
            # 計算熱度分數
            item['popularity_score'] = (
                item['like'] + 
                2 * item['comment'] + 
                3 * item['share']
            )
            data.append(item)
            
        return data
    except Exception as e:
        print(f"讀取CSV數據時發生錯誤: {e}")
        # 返回空列表而不是拋出異常，以便後續代碼可以優雅地處理
        return []

def generate_brand_detail_files():
    """生成所有品牌的詳細資料檔案"""
    try:
        # 從data目錄獲取所有品牌
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        brands = []
        
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('_processed.csv'):
                    brand_name = file.replace('_processed.csv', '')
                    brands.append(brand_name)
        
        for brand_name in brands:
            # 讀取CSV數據
            data = read_csv_data(brand_name)
            
            if not data:
                print(f"無法獲取品牌 {brand_name} 的數據，創建模擬數據")
                # 創建模擬數據
                data = []
                for i in range(5):
                    data.append({
                        'date': f'2023-{(i%12)+1:02d}-{(i%28)+1:02d}',
                        'content': f'{brand_name} 測試貼文 #{i+1}',
                        'like': 100 + i * 20,
                        'comment': 10 + i * 5,
                        'share': 5 + i * 2,
                        'popularity_score': 100 + i * 20 + 2 * (10 + i * 5) + 3 * (5 + i * 2)
                    })
            
            # 計算統計數據
            post_count = len(data)
            total_likes = sum(item.get('like', 0) for item in data)
            total_comments = sum(item.get('comment', 0) for item in data)
            total_shares = sum(item.get('share', 0) for item in data)
            total_forwards = sum(item.get('forward', 0) for item in data)
            
            # 計算總互動和平均互動
            total_interactions = total_likes + total_comments + total_shares + total_forwards
            
            # 計算熱度分數
            popularity_scores = [
                item.get('like', 0) + 2 * item.get('comment', 0) + 3 * item.get('share', 0)
                for item in data
            ]
            avg_popularity = sum(popularity_scores) / post_count if post_count > 0 else 0
            
            stats = {
                'post_count': post_count,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'total_shares': total_shares,
                'total_forwards': total_forwards,
                'total_interactions': total_interactions,
                'avg_interactions_per_post': avg_popularity,
                'interaction_rate': avg_popularity / 1000  # 簡單假設的互動率
            }
            
            # 模擬月度互動數據
            monthly_interactions = [
                {"month": "2023-11", "like": 1200, "comment": 300, "forward": 50, "share": 200},
                {"month": "2023-12", "like": 1500, "comment": 350, "forward": 60, "share": 250},
                {"month": "2024-01", "like": 1800, "comment": 400, "forward": 70, "share": 300},
            ]
            
            content_length_analysis = [
                {"content_length_group": "0-50", "total_interactions": 100},
                {"content_length_group": "51-100", "total_interactions": 150},
                {"content_length_group": "101-150", "total_interactions": 200},
            ]
            
            # 只取前5條記錄作為最近的貼文
            recent_posts = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:5]
            
            # 創建結果對象
            result = {
                'stats': stats,
                'monthly_interactions': monthly_interactions,
                'content_length_analysis': content_length_analysis,
                'recent_posts': recent_posts
            }
            
            # 保存為JSON文件
            with open(f'static/data/brand_detail_{brand_name}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"已生成品牌 {brand_name} 的詳細數據檔案")
    except Exception as e:
        print(f"生成品牌詳細資料檔案時發生錯誤: {e}")

if __name__ == "__main__":
    print("開始生成品牌詳細資料檔案...")
    generate_brand_detail_files()
    print("品牌詳細資料檔案生成完成！") 