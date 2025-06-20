// 設定Plotly深色主題（全域變數）
const darkTemplate = {
    paper_bgcolor: '#252525',
    plot_bgcolor: '#252525',
    font: {
        color: '#e8e8e8'
    },
    xaxis: {
        gridcolor: 'rgba(255, 255, 255, 0.1)',
        zerolinecolor: 'rgba(255, 255, 255, 0.1)'
    },
    yaxis: {
        gridcolor: 'rgba(255, 255, 255, 0.1)',
        zerolinecolor: 'rgba(255, 255, 255, 0.1)'
    },
    legend: {
        bgcolor: '#252525'
    }
};

// 情感分析與熱度圖表
function updateSentimentChart(brandName) {
    // 顯示載入中
    document.getElementById('sentiment-popularity-chart').innerHTML = 
        '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i> 正在載入情感分析數據...</div>';
    
    // 獲取所選品牌的情感分析數據
    fetch(`./static/data/brand_sentiment_${brandName}.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP 錯誤 ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                throw new Error('沒有可用的數據');
            }
            if (data.error) {
                throw new Error(data.error);
            }
            
            // 先清空容器，移除載入訊息
            document.getElementById('sentiment-popularity-chart').innerHTML = '';
            
            const trace = {
                x: data.map(item => item.sentiment_score),
                y: data.map(item => item.popularity_score),
                mode: 'markers',
                type: 'scatter',
                marker: {
                    size: 12,
                    color: data.map(item => item.popularity_score),
                    colorscale: 'Viridis',
                    showscale: true,
                    colorbar: {
                        title: '熱度分數',
                        titlefont: {
                            color: '#e8e8e8'
                        },
                        tickfont: {
                            color: '#e8e8e8'
                        }
                    },
                    opacity: 0.8,
                    line: {
                        width: 1,
                        color: 'rgba(255, 255, 255, 0.2)'
                    }
                },
                text: data.map(item => 
                    `內容: ${item.content || '無內容'}<br>` +
                    `按讚: ${item.like || 0}<br>` +
                    `留言: ${item.comment || 0}<br>` +
                    `分享: ${item.share || 0}<br>` +
                    `熱度: ${item.popularity_score || 0}`
                ),
                hoverinfo: 'text'
            };

            const layout = {
                title: `${brandName} 品牌貼文情感分數與熱度關係`,
                xaxis: {
                    title: '情感分數 (0=負面, 1=正面)',
                    gridcolor: darkTemplate.xaxis.gridcolor,
                    zerolinecolor: darkTemplate.xaxis.zerolinecolor
                },
                yaxis: {
                    title: '熱度分數',
                    gridcolor: darkTemplate.yaxis.gridcolor,
                    zerolinecolor: darkTemplate.yaxis.zerolinecolor
                },
                hovermode: 'closest',
                paper_bgcolor: darkTemplate.paper_bgcolor,
                plot_bgcolor: darkTemplate.plot_bgcolor,
                font: darkTemplate.font
            };

            Plotly.newPlot('sentiment-popularity-chart', [trace], layout);
        })
        .catch(error => {
            console.error('獲取數據失敗:', error);
            document.getElementById('sentiment-popularity-chart').innerHTML = 
                `<div class="error-container">
                    <p class="error"><i class="fas fa-exclamation-triangle"></i> 無法載入數據。${error.message}</p>
                    <button class="retry-btn" onclick="updateSentimentChart('${brandName}')">
                        <i class="fas fa-redo"></i> 重試
                    </button>
                </div>`;
        });
}

// 模型比較圖表
function loadModelComparisonChart() {
    // 顯示加載中的訊息
    document.getElementById('model-comparison-chart').innerHTML = 
        '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i> 正在載入數據...</div>';
        
    fetch('./static/data/popularity_model_comparison.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP 錯誤 ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data || Object.keys(data).length === 0) {
                throw new Error('沒有可用的模型比較數據');
            }
            if (data.error) {
                throw new Error(data.error);
            }
            
            // 先清空容器，移除載入訊息
            document.getElementById('model-comparison-chart').innerHTML = '';
            
            const models = Object.keys(data);
            const metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score'];
            const colors = ['#4fa8ff', '#ff6b9d', '#4caf50', '#ff9800'];
            
            const traces = metrics.map((metric, i) => {
                return {
                    x: models,
                    y: models.map(model => data[model][metric]),
                    name: metric,
                    type: 'bar',
                    marker: {
                        color: colors[i % colors.length],
                        line: {
                            width: 1,
                            color: 'rgba(255, 255, 255, 0.2)'
                        }
                    }
                };
            });

            const layout = {
                title: '不同模型預測熱門貼文的表現比較',
                barmode: 'group',
                xaxis: {
                    title: '模型',
                    gridcolor: darkTemplate.xaxis.gridcolor,
                    zerolinecolor: darkTemplate.xaxis.zerolinecolor
                },
                yaxis: {
                    title: '分數',
                    range: [0, 1],
                    gridcolor: darkTemplate.yaxis.gridcolor,
                    zerolinecolor: darkTemplate.yaxis.zerolinecolor
                },
                legend: {
                    orientation: 'h',
                    y: -0.2,
                    bgcolor: darkTemplate.legend.bgcolor
                },
                paper_bgcolor: darkTemplate.paper_bgcolor,
                plot_bgcolor: darkTemplate.plot_bgcolor,
                font: darkTemplate.font
            };

            Plotly.newPlot('model-comparison-chart', traces, layout);
        })
        .catch(error => {
            console.error('獲取數據失敗:', error);
            document.getElementById('model-comparison-chart').innerHTML = 
                `<div class="error-container">
                    <p class="error"><i class="fas fa-exclamation-triangle"></i> 無法載入數據。${error.message}</p>
                    <button class="retry-btn" onclick="loadModelComparisonChart()">
                        <i class="fas fa-redo"></i> 重試
                    </button>
                </div>`;
        });
}

// 特徵重要性圖表
function loadFeatureImportanceChart() {
    // 顯示加載中的訊息
    document.getElementById('feature-importance-chart').innerHTML = 
        '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i> 正在載入數據...</div>';
        
    fetch('./static/data/feature_importance.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP 錯誤 ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data || Object.keys(data).length === 0) {
                throw new Error('沒有可用的特徵重要性數據');
            }
            if (data.error) {
                throw new Error(data.error);
            }
            
            // 先清空容器，移除載入訊息
            document.getElementById('feature-importance-chart').innerHTML = '';
            
            const features = Object.keys(data);
            const values = features.map(feat => data[feat]);

            const trace = {
                x: features,
                y: values,
                type: 'bar',
                marker: {
                    color: '#4fa8ff',
                    line: {
                        color: 'rgba(255, 255, 255, 0.3)',
                        width: 1.5
                    }
                },
                text: values.map(val => (val * 100).toFixed(1) + '%'),
                textposition: 'auto',
                textfont: {
                    color: '#e8e8e8'
                }
            };

            const layout = {
                title: '預測貼文熱門度的特徵重要性',
                xaxis: {
                    title: '特徵',
                    gridcolor: darkTemplate.xaxis.gridcolor,
                    zerolinecolor: darkTemplate.xaxis.zerolinecolor
                },
                yaxis: {
                    title: '重要性 (比例)',
                    range: [0, Math.max(...values) * 1.1],
                    gridcolor: darkTemplate.yaxis.gridcolor,
                    zerolinecolor: darkTemplate.yaxis.zerolinecolor
                },
                paper_bgcolor: darkTemplate.paper_bgcolor,
                plot_bgcolor: darkTemplate.plot_bgcolor,
                font: darkTemplate.font
            };

            Plotly.newPlot('feature-importance-chart', [trace], layout);
        })
        .catch(error => {
            console.error('獲取數據失敗:', error);
            document.getElementById('feature-importance-chart').innerHTML = 
                `<div class="error-container">
                    <p class="error"><i class="fas fa-exclamation-triangle"></i> 無法載入數據。${error.message}</p>
                    <button class="retry-btn" onclick="loadFeatureImportanceChart()">
                        <i class="fas fa-redo"></i> 重試
                    </button>
                </div>`;
        });
}

// 載入品牌選項
function loadBrandOptions() {
    fetch('./static/data/brands.json')
        .then(response => response.json())
        .then(brands => {
            const brandSelect = document.getElementById('brandSelect');
            
            // 清空現有選項
            brandSelect.innerHTML = '';
            
            // 按名稱排序品牌
            brands.sort((a, b) => a.name.localeCompare(b.name));
            
            // 添加選項
            brands.forEach(brand => {
                const option = document.createElement('option');
                option.value = brand.name;
                option.textContent = brand.name;
                brandSelect.appendChild(option);
            });
            
            // 初始加載第一個品牌的圖表
            if (brands.length > 0) {
                updateSentimentChart(brands[0].name);
            }
        })
        .catch(error => {
            console.error('載入品牌選項失敗:', error);
            document.getElementById('brandSelect').innerHTML = 
                '<option value="">無法載入品牌</option>';
        });
}

// 頁面載入後初始化
document.addEventListener('DOMContentLoaded', function() {
    // 選擇品牌下拉框監聽
    const brandSelect = document.getElementById('brandSelect');
    brandSelect.addEventListener('change', function() {
        updateSentimentChart(this.value);
    });

    // 初始加載
    loadBrandOptions();
    loadModelComparisonChart();
    loadFeatureImportanceChart();
}); 