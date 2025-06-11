// 設定Plotly深色主題（全域變數）
const darkTemplate = {
    paper_bgcolor: '#252525',
    plot_bgcolor: '#252525',
    font: { color: '#e8e8e8' },
    xaxis: {
        gridcolor: 'rgba(255, 255, 255, 0.1)',
        zerolinecolor: 'rgba(255, 255, 255, 0.1)'
    },
    yaxis: {
        gridcolor: 'rgba(255, 255, 255, 0.1)',
        zerolinecolor: 'rgba(255, 255, 255, 0.1)'
    },
    legend: { bgcolor: '#252525' }
};

// 頁面載入後初始化
document.addEventListener('DOMContentLoaded', function() {
    // 設定載入中的訊息
    document.querySelectorAll('.chart-container').forEach(container => {
        container.innerHTML = '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i> 正在載入數據...</div>';
    });
    
    document.getElementById('insights-list').innerHTML = '<li><i class="fas fa-spinner fa-spin"></i> 載入中...</li>';
    
    // 載入品牌數據
    fetch('./static/data/brand_stats.json')
        .then(response => response.json())
        .then(data => {
            renderCharts(data);
        })
        .catch(error => {
            console.error('獲取品牌數據失敗:', error);
            document.querySelectorAll('.chart-container').forEach(container => {
                container.innerHTML = '<div class="error-message">載入數據失敗</div>';
            });
            document.getElementById('insights-list').innerHTML = '<li>無法載入洞察數據</li>';
        });
    
    // 載入互動比較數據
    fetch('./static/data/engagement_comparison.json')
        .then(response => response.json())
        .then(data => {
            renderEngagementChart(data);
        })
        .catch(error => {
            console.error('獲取互動比較數據失敗:', error);
            document.getElementById('avg-engagement-chart').innerHTML = '<div class="error-message">載入數據失敗</div>';
        });
});

// 渲染圖表的函數
function renderCharts(data) {
    // 實現圖表渲染邏輯
    console.log('數據載入成功，開始渲染圖表');
}

// 渲染互動比較圖表
function renderEngagementChart(data) {
    // 實現互動比較圖表渲染邏輯
    console.log('互動比較數據載入成功，開始渲染圖表');
} 