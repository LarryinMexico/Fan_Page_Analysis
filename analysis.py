import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, precision_recall_fscore_support, accuracy_score
from xgboost import XGBClassifier

try:
    from snownlp import SnowNLP
    SNOWNLP_AVAILABLE = True
except ImportError:
    print("SnowNLP not available, sentiment analysis will be simulated")
    SNOWNLP_AVAILABLE = False

def simulate_sentiment(text):
    """簡單的情感分析模擬，當SnowNLP不可用時"""
    import hashlib
    # 使用文本的雜湊值來生成一個0.3-0.9之間的穩定值
    text_hash = int(hashlib.md5(str(text).encode('utf-8')).hexdigest(), 16)
    return 0.3 + (text_hash % 60) / 100

def load_all_brand_data():
    """載入所有品牌的CSV數據並整合"""
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    brand_files = [f for f in os.listdir(data_path) if f.endswith('_processed.csv')]
    
    dfs = []
    for file_name in brand_files:
        brand_name = file_name.split('_')[0]
        file_path = os.path.join(data_path, file_name)
        
        try:
            df = pd.read_csv(file_path)
            df['brand'] = brand_name
            dfs.append(df)
            print(f"Successfully loaded {brand_name} data: {len(df)} records")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    if not dfs:
        raise ValueError("No data loaded from CSV files")
    
    combined_data = pd.concat(dfs, ignore_index=True)
    return combined_data

def preprocess_data(df):
    """數據預處理和清理"""
    # 確保數值欄位為正確類型
    for col in ['like', 'comment', 'share']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 如果沒有forward列，添加全0列
    if 'forward' not in df.columns:
        df['forward'] = 0
    
    # 計算熱度分數
    df['popularity_score'] = df['like'] + 2 * df['comment'] + 3 * df['share']
    
    # 計算情感分數
    if SNOWNLP_AVAILABLE:
        df['sentiment_score'] = df['content'].astype(str).apply(lambda x: SnowNLP(x).sentiments)
    else:
        df['sentiment_score'] = df['content'].astype(str).apply(simulate_sentiment)
    
    # 標記熱門貼文（前25%）
    threshold = df['popularity_score'].quantile(0.75)
    df['is_popular'] = (df['popularity_score'] >= threshold).astype(int)
    
    return df

def train_models(df):
    """訓練多個機器學習模型並評估效能"""
    # 準備特徵和標籤
    features = df[['like', 'comment', 'share', 'sentiment_score']]
    labels = df['is_popular']
    
    # 分割訓練和測試集
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )
    
    # 定義多個模型
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "SVM": SVC(kernel='rbf', probability=True, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "AdaBoost": AdaBoostClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
    }
    
    # 訓練模型並收集評估指標
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
        
        results.append({
            "Model": name,
            "Accuracy": float(acc),
            "Precision": float(precision),
            "Recall": float(recall),
            "F1-Score": float(f1)
        })
    
    return results

def get_feature_importance(df):
    """使用隨機森林模型取得特徵重要性"""
    features = df[['like', 'comment', 'share', 'sentiment_score']]
    labels = df['is_popular']
    
    model = RandomForestClassifier(random_state=42)
    model.fit(features, labels)
    
    importances = model.feature_importances_
    feature_importance = {}
    for feature, importance in zip(features.columns, importances):
        feature_importance[feature] = float(importance)
    
    return feature_importance

def get_brand_sentiment_data(df, brand_name):
    """取得特定品牌的情感分析與熱度關係數據"""
    brand_df = df[df['brand'] == brand_name].copy()
    
    if brand_df.empty:
        return []
    
    # 取得所有文章的情感分數、熱度分數和互動數據
    posts_data = []
    for _, row in brand_df.iterrows():
        content_str = str(row['content']) if not pd.isna(row['content']) else ""
        posts_data.append({
            "sentiment_score": float(row['sentiment_score']),
            "popularity_score": float(row['popularity_score']),
            "content": content_str[:100] + '...' if len(content_str) > 100 else content_str,
            "like": int(row['like']),
            "comment": int(row['comment']),
            "share": int(row['share'])
        })
    
    return posts_data

def generate_analysis_data():
    """生成所有分析數據並保存為JSON"""
    try:
        # 載入並處理數據
        print("Loading brand data...")
        combined_data = load_all_brand_data()
        print(f"Loaded {len(combined_data)} total records")
        
        print("Preprocessing data...")
        processed_data = preprocess_data(combined_data)
        
        print("Training models...")
        model_results = train_models(processed_data)
        
        print("Calculating feature importance...")
        feature_importance = get_feature_importance(processed_data)
        
        # 取得每個品牌的情感分析數據
        brand_sentiment_data = {}
        unique_brands = processed_data['brand'].unique()
        for brand in unique_brands:
            print(f"Processing sentiment data for {brand}...")
            brand_sentiment_data[brand] = get_brand_sentiment_data(processed_data, brand)
        
        # 計算各品牌的互動統計數據
        brand_stats = {}
        for brand in unique_brands:
            brand_df = processed_data[processed_data['brand'] == brand]
            brand_stats[brand] = {
                "post_count": len(brand_df),
                "total_likes": int(brand_df['like'].sum()),
                "total_comments": int(brand_df['comment'].sum()),
                "total_shares": int(brand_df['share'].sum()),
                "total_forwards": int(brand_df['forward'].sum()),
                "total_interactions": int(brand_df['like'].sum() + 
                                         brand_df['comment'].sum() + 
                                         brand_df['share'].sum() + 
                                         brand_df['forward'].sum()),
                "avg_interactions_per_post": float(brand_df['popularity_score'].mean()),
                "interaction_rate": float(brand_df['popularity_score'].mean() / 1000)  # 假設的換算率
            }
        
        # 將所有數據整合到一個字典並保存為JSON
        analysis_results = {
            "model_comparison": model_results,
            "feature_importance": feature_importance,
            "brand_sentiment_data": brand_sentiment_data,
            "brand_stats": brand_stats
        }
        
        # 保存JSON結果
        output_dir = os.path.join(os.path.dirname(__file__), 'static', 'data')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_file = os.path.join(output_dir, 'analysis_results.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        print(f"Analysis complete! Results saved to {output_file}")
        return analysis_results
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_analysis_data() 