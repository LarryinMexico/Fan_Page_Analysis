import os
import json
import pandas as pd
import hashlib

# 確保靜態數據目錄存在
os.makedirs('static/data', exist_ok=True)

def load_analysis_results():
    """載入分析結果"""
    try:
        analysis_file = os.path.join(os.path.dirname(__file__), 'analysis_results.json')
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"載入分析結果時發生錯誤: {e}")
    return None

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

def generate_brand_list():
    """生成品牌列表的靜態數據"""
    # 從data目錄中獲取所有CSV文件名稱
    brands = []
    try:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('_processed.csv'):
                    brand_name = file.replace('_processed.csv', '')
                    # 讀取CSV數據以獲取統計信息
                    data = read_csv_data(brand_name)
                    if data:
                        # 計算總互動數
                        total_likes = sum(item.get('like', 0) for item in data)
                        total_comments = sum(item.get('comment', 0) for item in data)
                        total_shares = sum(item.get('share', 0) for item in data)
                        total_interactions = total_likes + total_comments + total_shares
                        
                        # 生成品牌信息
                        brand_info = {
                            'id': hashlib.md5(brand_name.encode()).hexdigest(),
                            'name': brand_name,
                            'total_posts': len(data),
                            'total_interactions': total_interactions,
                            'avg_interactions': total_interactions / len(data) if data else 0
                        }
                        brands.append(brand_info)
        
        # 保存品牌列表
        with open('static/data/brands.json', 'w', encoding='utf-8') as f:
            json.dump(brands, f, ensure_ascii=False, indent=2)
        print(f"已生成品牌列表數據: {len(brands)} 個品牌")
        return brands
    except Exception as e:
        print(f"生成品牌列表時發生錯誤: {e}")
        return []

def generate_brand_stats(brand_name):
    """生成特定品牌的統計數據"""
    try:
        data = read_csv_data(brand_name)
        if not data:
            print(f"無法獲取品牌 {brand_name} 的數據")
            return
        
        # 計算統計數據
        total_likes = sum(item.get('like', 0) for item in data)
        total_comments = sum(item.get('comment', 0) for item in data)
        total_shares = sum(item.get('share', 0) for item in data)
        
        # 按月份分組的互動數據
        monthly_data = {}
        for item in data:
            if 'date' in item:
                # 假設日期格式為 YYYY-MM-DD
                try:
                    date_parts = item['date'].split('-')
                    if len(date_parts) >= 2:
                        month_key = f"{date_parts[0]}-{date_parts[1]}"
                        if month_key not in monthly_data:
                            monthly_data[month_key] = {
                                'likes': 0, 'comments': 0, 'shares': 0, 'posts': 0
                            }
                        monthly_data[month_key]['likes'] += item.get('like', 0)
                        monthly_data[month_key]['comments'] += item.get('comment', 0)
                        monthly_data[month_key]['shares'] += item.get('share', 0)
                        monthly_data[month_key]['posts'] += 1
                except Exception as e:
                    print(f"處理日期時發生錯誤: {e}")
        
        # 轉換為列表格式
        monthly_stats = [
            {
                'month': month,
                'likes': stats['likes'],
                'comments': stats['comments'],
                'shares': stats['shares'],
                'posts': stats['posts']
            }
            for month, stats in monthly_data.items()
        ]
        
        # 排序按月份
        monthly_stats.sort(key=lambda x: x['month'])
        
        # 保存品牌統計數據
        stats = {
            'name': brand_name,
            'total_posts': len(data),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'monthly_stats': monthly_stats
        }
        
        os.makedirs(f'static/data/brands', exist_ok=True)
        with open(f'static/data/brands/{brand_name}.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"已生成品牌 {brand_name} 的統計數據")
        return stats
    except Exception as e:
        print(f"生成品牌統計數據時發生錯誤: {e}")
        return None

def generate_comparison_data():
    """生成品牌比較的靜態數據"""
    try:
        brands = generate_brand_list()
        comparison_data = []
        
        for brand in brands:
            brand_name = brand['name']
            data = read_csv_data(brand_name)
            if data:
                # 計算平均互動數
                avg_likes = sum(item.get('like', 0) for item in data) / len(data)
                avg_comments = sum(item.get('comment', 0) for item in data) / len(data)
                avg_shares = sum(item.get('share', 0) for item in data) / len(data)
                
                comparison_data.append({
                    'name': brand_name,
                    'avg_likes': avg_likes,
                    'avg_comments': avg_comments,
                    'avg_shares': avg_shares,
                    'total_posts': len(data)
                })
        
        with open('static/data/comparison.json', 'w', encoding='utf-8') as f:
            json.dump(comparison_data, f, ensure_ascii=False, indent=2)
        print(f"已生成品牌比較數據: {len(comparison_data)} 個品牌")
        return comparison_data
    except Exception as e:
        print(f"生成比較數據時發生錯誤: {e}")
        return []

def generate_sentiment_data():
    """生成情感分析的靜態數據"""
    try:
        # 載入分析結果
        analysis_results = load_analysis_results()
        if not analysis_results:
            print("無法載入分析結果，跳過情感分析數據生成")
            return
        
        sentiment_data = {}
        
        # 從分析結果中提取情感分析數據
        if 'sentiment_analysis' in analysis_results:
            sentiment_data = analysis_results['sentiment_analysis']
        
        with open('static/data/sentiment.json', 'w', encoding='utf-8') as f:
            json.dump(sentiment_data, f, ensure_ascii=False, indent=2)
        print("已生成情感分析數據")
        return sentiment_data
    except Exception as e:
        print(f"生成情感分析數據時發生錯誤: {e}")
        return {}

def main():
    """主函數，生成所有靜態數據"""
    print("開始生成靜態數據...")
    
    # 生成品牌列表
    brands = generate_brand_list()
    
    # 為每個品牌生成統計數據
    for brand in brands:
        generate_brand_stats(brand['name'])
    
    # 生成比較數據
    generate_comparison_data()
    
    # 生成情感分析數據
    generate_sentiment_data()
    
    print("靜態數據生成完成！")

if __name__ == "__main__":
    main() 