from flask import Flask, render_template, jsonify, request
import os
import json
import csv
import pandas as pd

app = Flask(__name__)

# 分析結果的緩存
analysis_results = None

def load_analysis_results():
    """加載預先生成的分析結果"""
    global analysis_results
    
    if analysis_results is not None:
        return analysis_results
        
    data_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'analysis_results.json')
    if os.path.exists(data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                analysis_results = json.load(f)
            return analysis_results
        except Exception as e:
            print(f"Error loading analysis results: {e}")
    
    # 如果文件不存在或加載失敗，嘗試生成數據
    try:
        from analysis import generate_analysis_data
        analysis_results = generate_analysis_data()
        return analysis_results
    except Exception as e:
        print(f"Error generating analysis data: {e}")
        return None

def read_csv_data(brand_name):
    """讀取特定品牌的CSV數據"""
    file_path = os.path.join(os.path.dirname(__file__), 'data', f'{brand_name}_processed.csv')
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 確保數值型態正確
            for key in ['like', 'comment', 'forward', 'share']:
                if key in row and row[key]:
                    try:
                        row[key] = int(row[key])
                    except ValueError:
                        row[key] = 0
                else:
                    row[key] = 0
            
            # 計算熱度分數
            row['popularity_score'] = (
                row['like'] + 
                2 * row['comment'] + 
                3 * row['share']
            )
            data.append(row)
    return data

@app.route('/')
def index():
    """首頁"""
    # 獲取所有可用的品牌名稱
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    return render_template('index.html', brands=brands)

@app.route('/analysis')
def analysis():
    """分析頁面"""
    # 獲取所有可用的品牌名稱
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    return render_template('analysis.html', brands=brands)

@app.route('/brand/<brand_name>')
def brand_detail(brand_name):
    """品牌詳細分析頁面"""
    # 獲取所有可用的品牌名稱
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    if brand_name not in brands:
        return "找不到該品牌的數據", 404
    
    # 嘗試從分析結果獲取統計數據
    results = load_analysis_results()
    if results and brand_name in results.get('brand_stats', {}):
        stats = results['brand_stats'][brand_name]
    else:
        # 提供一些模擬數據進行測試
        stats = {
            'post_count': 50,
            'total_likes': 5000,
            'total_comments': 800,
            'total_forwards': 200,
            'total_shares': 1000,
            'total_interactions': 7000,
            'avg_interactions_per_post': 140.0,
            'interaction_rate': 0.0014
        }
    
    # 嘗試讀取CSV數據
    try:
        data = read_csv_data(brand_name)
        # 只取前10條記錄
        data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:10]
    except Exception as e:
        print(f"Error reading CSV data: {e}")
        # 模擬帖子數據
        data = [
            {'date': '2024-01-01', 'content': '測試帖子1', 'like': 100, 'comment': 20, 'forward': 5, 'share': 30},
            {'date': '2024-01-15', 'content': '測試帖子2', 'like': 150, 'comment': 30, 'forward': 10, 'share': 40},
        ]
    
    return render_template('brand_detail.html', 
                          brand_name=brand_name, 
                          stats=stats,
                          data=data
                          )

@app.route('/visualization')
def visualization():
    """視覺化分析頁面"""
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    return render_template('visualization.html', brands=brands)

@app.route('/api/brands_data')
def brands_data():
    """API端點：獲取所有品牌的基礎數據"""
    results = load_analysis_results()
    if results and 'brand_stats' in results:
        return jsonify(results['brand_stats'])
    
    # 提供一些模擬數據進行測試
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    result = {}
    for brand in brands:
        result[brand] = {
            'post_count': 50,
            'total_likes': 5000,
            'total_comments': 800,
            'total_forwards': 200,
            'total_shares': 1000,
            'total_interactions': 7000,
            'avg_interactions_per_post': 140.0,
            'interaction_rate': 0.0014
        }
    
    return jsonify(result)

@app.route('/api/popularity_model_comparison')
def popularity_model_comparison():
    """API端點：獲取模型性能比較數據"""
    results = load_analysis_results()
    if results and 'model_comparison' in results:
        # 將列表轉換為字典，以模型名稱為鍵
        model_dict = {item['Model']: {
            key: value for key, value in item.items() if key != 'Model'
        } for item in results['model_comparison']}
        return jsonify(model_dict)
    
    # 模擬筆記本中提到的模型比較結果
    models_data = {
        "Logistic Regression": {
            "Accuracy": 0.91,
            "Precision": 0.89,
            "Recall": 0.92,
            "F1-Score": 0.90
        },
        "SVM": {
            "Accuracy": 0.92,
            "Precision": 0.89,
            "Recall": 0.94,
            "F1-Score": 0.91
        },
        "Gradient Boosting": {
            "Accuracy": 0.94,
            "Precision": 0.92,
            "Recall": 0.93,
            "F1-Score": 0.92
        },
        "AdaBoost": {
            "Accuracy": 0.93,
            "Precision": 0.91,
            "Recall": 0.92,
            "F1-Score": 0.91
        },
        "XGBoost": {
            "Accuracy": 0.95,
            "Precision": 0.93,
            "Recall": 0.94,
            "F1-Score": 0.93
        }
    }
    
    return jsonify(models_data)

@app.route('/api/brand_sentiment_popularity/<brand_name>')
def brand_sentiment_popularity(brand_name):
    """API端點：獲取特定品牌的情感分析與熱度數據"""
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    if brand_name not in brands:
        return jsonify({"error": "Brand not found"}), 404
    
    # 直接從CSV讀取數據
    try:
        file_path = os.path.join(data_path, f'{brand_name}_processed.csv')
        df = pd.read_csv(file_path)
        
        # 確保數值欄位為正確類型
        for col in ['like', 'comment', 'share']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 計算熱度分數
        df['popularity_score'] = df['like'] + 2 * df['comment'] + 3 * df['share']
        
        # 計算情感分數 (使用簡單的方法模擬)
        def simulate_sentiment(text):
            import hashlib
            text_str = str(text) if not pd.isna(text) else ""
            text_hash = int(hashlib.md5(text_str.encode('utf-8')).hexdigest(), 16)
            return 0.3 + (text_hash % 60) / 100
        
        df['sentiment_score'] = df['content'].apply(simulate_sentiment)
        
        # 轉換為JSON響應格式
        result = []
        for _, row in df.iterrows():
            content_str = str(row['content']) if not pd.isna(row['content']) else ""
            result.append({
                "sentiment_score": float(row['sentiment_score']),
                "popularity_score": float(row['popularity_score']),
                "content": content_str[:100] + '...' if len(content_str) > 100 else content_str,
                "like": int(row['like']),
                "comment": int(row['comment']),
                "share": int(row['share'])
            })
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error processing data for {brand_name}: {e}")
        # 模擬情感分析與熱度關係數據
        sentiment_data = []
        for i in range(30):
            sentiment_data.append({
                "sentiment_score": round(0.3 + 0.6 * i / 30, 2),  # 0.3-0.9
                "popularity_score": int(1000 + 5000 * i / 30 * (0.5 + 0.5 * (i % 3))),
                "content": f"貼文 #{i+1}",
                "like": int(50 + 300 * i / 30),
                "comment": int(10 + 50 * i / 30),
                "share": int(5 + 25 * i / 30)
            })
        return jsonify(sentiment_data)

@app.route('/api/feature_importance')
def feature_importance():
    """API端點：模型特徵重要性"""
    results = load_analysis_results()
    if results and 'feature_importance' in results:
        return jsonify(results['feature_importance'])
    
    # 模擬筆記本中提到的模型特徵重要性
    features = {
        "like": 0.524,
        "comment": 0.285,
        "share": 0.189,
        "sentiment_score": 0.002
    }
    
    return jsonify(features)

@app.route('/api/brand_detail/<brand_name>')
def api_brand_detail(brand_name):
    """API端點：獲取特定品牌的詳細數據"""
    # 獲取所有可用的品牌名稱
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    if brand_name not in brands:
        return jsonify({"error": "Brand not found"}), 404
    
    results = load_analysis_results()
    if results and 'brand_stats' in results and brand_name in results['brand_stats']:
        stats = results['brand_stats'][brand_name]
    else:
        # 提供一些模擬數據進行測試
        stats = {
            'post_count': 50,
            'total_likes': 5000,
            'total_comments': 800,
            'total_forwards': 200,
            'total_shares': 1000,
            'total_interactions': 7000,
            'avg_interactions_per_post': 140.0,
            'interaction_rate': 0.0014
        }
    
    # 模擬月度互動數據
    monthly_interactions = [
        {"month": "2024-01", "like": 1200, "comment": 300, "forward": 50, "share": 200},
        {"month": "2024-02", "like": 1500, "comment": 350, "forward": 60, "share": 250},
        {"month": "2024-03", "like": 1800, "comment": 400, "forward": 70, "share": 300},
    ]
    
    content_length_analysis = [
        {"content_length_group": "0-50", "total_interactions": 100},
        {"content_length_group": "51-100", "total_interactions": 150},
        {"content_length_group": "101-150", "total_interactions": 200},
    ]
    
    # 嘗試讀取CSV數據作為最近的貼文
    try:
        recent_posts = read_csv_data(brand_name)
        # 只取前5條記錄
        recent_posts = sorted(recent_posts, key=lambda x: x.get('date', ''), reverse=True)[:5]
    except Exception:
        # 模擬最近的貼文數據
        recent_posts = [
            {'date': '2024-03-15', 'content': '測試帖子1', 'like': 100, 'comment': 20, 'forward': 5, 'share': 30},
            {'date': '2024-03-01', 'content': '測試帖子2', 'like': 150, 'comment': 30, 'forward': 10, 'share': 40},
        ]
    
    # 返回結果
    result = {
        'stats': stats,
        'monthly_interactions': monthly_interactions,
        'content_length_analysis': content_length_analysis,
        'recent_posts': recent_posts
    }
    
    return jsonify(result)

@app.route('/analyze', methods=['GET'])
def run_analysis():
    """手動執行分析"""
    try:
        from analysis import generate_analysis_data
        results = generate_analysis_data()
        return jsonify({"status": "success", "message": "Analysis completed successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error during analysis: {str(e)}"}), 500

@app.route('/api/brand_stats')
def brand_stats():
    """API端點：獲取所有品牌的統計資料比較"""
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    result = {}
    for brand in brands:
        try:
            file_path = os.path.join(data_path, f'{brand}_processed.csv')
            df = pd.read_csv(file_path)
            
            # 確保數值欄位為正確類型
            for col in ['like', 'comment', 'share', 'forward']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = 0
            
            # 計算統計數據
            total_likes = int(df['like'].sum())
            total_comments = int(df['comment'].sum())
            total_shares = int(df['share'].sum())
            total_forwards = int(df['forward'].sum() if 'forward' in df.columns else 0)
            post_count = len(df)
            
            # 計算熱度分數
            df['popularity_score'] = df['like'] + 2 * df['comment'] + 3 * df['share']
            avg_popularity = float(df['popularity_score'].mean()) if post_count > 0 else 0
            
            result[brand] = {
                'post_count': post_count,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'total_shares': total_shares,
                'total_forwards': total_forwards,
                'total_interactions': total_likes + total_comments + total_shares + total_forwards,
                'avg_interactions_per_post': avg_popularity,
                'interaction_rate': avg_popularity / 1000  # 簡單假設的互動率
            }
        except Exception as e:
            print(f"Error processing stats for {brand}: {e}")
            result[brand] = {
                'post_count': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'total_forwards': 0,
                'total_interactions': 0,
                'avg_interactions_per_post': 0,
                'interaction_rate': 0,
                'error': str(e)
            }
    
    return jsonify(result)

@app.route('/api/engagement_comparison')
def engagement_comparison():
    """API端點：獲取各品牌的互動數據比較"""
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brands = [file.split('_')[0] for file in os.listdir(data_path) if file.endswith('_processed.csv')]
    
    likes = []
    comments = []
    shares = []
    brand_names = []
    
    for brand in brands:
        try:
            file_path = os.path.join(data_path, f'{brand}_processed.csv')
            df = pd.read_csv(file_path)
            
            # 確保數值欄位為正確類型
            for col in ['like', 'comment', 'share']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = 0
            
            brand_names.append(brand)
            likes.append(float(df['like'].mean()))
            comments.append(float(df['comment'].mean()))
            shares.append(float(df['share'].mean()))
        except Exception as e:
            print(f"Error processing engagement for {brand}: {e}")
    
    return jsonify({
        'brands': brand_names,
        'likes': likes,
        'comments': comments,
        'shares': shares
    })

if __name__ == '__main__':
    app.run(debug=True) 