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
    console.log('頁面已載入，開始初始化圖表');
    
    // 設定載入中的訊息
    document.querySelectorAll('.chart-container').forEach(container => {
        container.innerHTML = '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i> 正在載入數據...</div>';
    });
    
    document.getElementById('insights-list').innerHTML = '<li><i class="fas fa-spinner fa-spin"></i> 載入中...</li>';
    
    // 載入品牌數據
    fetch('./static/data/brand_stats.json')
        .then(response => {
            console.log('品牌數據響應:', response);
            if (!response.ok) {
                throw new Error(`HTTP錯誤 ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('品牌數據載入成功:', data);
            renderCharts(data);
        })
        .catch(error => {
            console.error('獲取品牌數據失敗:', error);
            document.querySelectorAll('.chart-container').forEach(container => {
                container.innerHTML = '<div class="error-message">載入數據失敗: ' + error.message + '</div>';
            });
            document.getElementById('insights-list').innerHTML = '<li>無法載入洞察數據</li>';
        });
    
    // 載入互動比較數據
    fetch('./static/data/engagement_comparison.json')
        .then(response => {
            console.log('互動比較數據響應:', response);
            if (!response.ok) {
                throw new Error(`HTTP錯誤 ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('互動比較數據載入成功:', data);
            renderEngagementChart(data);
        })
        .catch(error => {
            console.error('獲取互動比較數據失敗:', error);
            document.getElementById('avg-engagement-chart').innerHTML = '<div class="error-message">載入數據失敗: ' + error.message + '</div>';
        });
});

// 渲染圖表的函數
function renderCharts(data) {
    console.log('開始渲染圖表');
    
    // 獲取品牌名稱列表
    const brands = Object.keys(data);
    
    // 1. 渲染貼文總數比較圖表
    const postCounts = brands.map(brand => data[brand].post_count);
    
    // 清空載入訊息
    document.getElementById('post-count-chart').innerHTML = '';
    
    const postCountTrace = {
        x: brands,
        y: postCounts,
        type: 'bar',
        marker: {
            color: '#4fa8ff',
            line: {
                color: 'rgba(255, 255, 255, 0.5)',
                width: 1
            }
        }
    };
    
    const postCountLayout = {
        title: '各品牌貼文總數比較',
        xaxis: {
            title: '品牌',
            gridcolor: darkTemplate.xaxis.gridcolor,
            zerolinecolor: darkTemplate.xaxis.zerolinecolor
        },
        yaxis: {
            title: '貼文數量',
            gridcolor: darkTemplate.yaxis.gridcolor,
            zerolinecolor: darkTemplate.yaxis.zerolinecolor
        },
        paper_bgcolor: darkTemplate.paper_bgcolor,
        plot_bgcolor: darkTemplate.plot_bgcolor,
        font: darkTemplate.font
    };
    
    Plotly.newPlot('post-count-chart', [postCountTrace], postCountLayout);
    console.log('貼文總數比較圖表渲染完成');
    
    // 2. 渲染互動量比較圖表
    const totalInteractions = brands.map(brand => data[brand].total_interactions);
    
    // 清空載入訊息
    document.getElementById('total-interactions-chart').innerHTML = '';
    
    const interactionsTrace = {
        x: brands,
        y: totalInteractions,
        type: 'bar',
        marker: {
            color: '#ff6b9d',
            line: {
                color: 'rgba(255, 255, 255, 0.5)',
                width: 1
            }
        }
    };
    
    const interactionsLayout = {
        title: '各品牌總互動量比較',
        xaxis: {
            title: '品牌',
            gridcolor: darkTemplate.xaxis.gridcolor,
            zerolinecolor: darkTemplate.xaxis.zerolinecolor
        },
        yaxis: {
            title: '總互動量',
            gridcolor: darkTemplate.yaxis.gridcolor,
            zerolinecolor: darkTemplate.yaxis.zerolinecolor
        },
        paper_bgcolor: darkTemplate.paper_bgcolor,
        plot_bgcolor: darkTemplate.plot_bgcolor,
        font: darkTemplate.font
    };
    
    Plotly.newPlot('total-interactions-chart', [interactionsTrace], interactionsLayout);
    console.log('互動量比較圖表渲染完成');
    
    // 3. 渲染互動效率比較圖表
    const interactionRates = brands.map(brand => data[brand].interaction_rate * 1000); // 乘以1000以便更好地顯示
    
    // 清空載入訊息
    document.getElementById('interaction-rate-chart').innerHTML = '';
    
    const rateTrace = {
        x: brands,
        y: interactionRates,
        type: 'bar',
        marker: {
            color: '#4caf50',
            line: {
                color: 'rgba(255, 255, 255, 0.5)',
                width: 1
            }
        }
    };
    
    const rateLayout = {
        title: '各品牌互動效率比較',
        xaxis: {
            title: '品牌',
            gridcolor: darkTemplate.xaxis.gridcolor,
            zerolinecolor: darkTemplate.xaxis.zerolinecolor
        },
        yaxis: {
            title: '互動率 (每千人)',
            gridcolor: darkTemplate.yaxis.gridcolor,
            zerolinecolor: darkTemplate.yaxis.zerolinecolor
        },
        paper_bgcolor: darkTemplate.paper_bgcolor,
        plot_bgcolor: darkTemplate.plot_bgcolor,
        font: darkTemplate.font
    };
    
    Plotly.newPlot('interaction-rate-chart', [rateTrace], rateLayout);
    console.log('互動效率比較圖表渲染完成');
    
    // 4. 更新洞察列表
    updateInsights(data);
}

// 渲染互動比較圖表
function renderEngagementChart(data) {
    console.log('開始渲染互動比較圖表');
    
    // 清空載入訊息
    document.getElementById('avg-engagement-chart').innerHTML = '';
    
    const brands = data.brands;
    const likes = data.likes;
    const comments = data.comments;
    const shares = data.shares;
    
    const trace1 = {
        x: brands,
        y: likes,
        name: '平均讚數',
        type: 'bar',
        marker: { color: '#4fa8ff' }
    };
    
    const trace2 = {
        x: brands,
        y: comments,
        name: '平均留言數',
        type: 'bar',
        marker: { color: '#ff6b9d' }
    };
    
    const trace3 = {
        x: brands,
        y: shares,
        name: '平均分享數',
        type: 'bar',
        marker: { color: '#4caf50' }
    };
    
    const layout = {
        title: '各品牌平均每貼文互動類型比較',
        barmode: 'group',
        xaxis: {
            title: '品牌',
            gridcolor: darkTemplate.xaxis.gridcolor,
            zerolinecolor: darkTemplate.xaxis.zerolinecolor
        },
        yaxis: {
            title: '平均數量',
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
    
    Plotly.newPlot('avg-engagement-chart', [trace1, trace2, trace3], layout);
    console.log('互動比較圖表渲染完成');
}

// 更新洞察列表
function updateInsights(data) {
    console.log('更新洞察列表');
    
    const brands = Object.keys(data);
    
    // 找出貼文數量最多的品牌
    const mostPostsBrand = brands.reduce((a, b) => data[a].post_count > data[b].post_count ? a : b);
    
    // 找出總互動量最高的品牌
    const mostInteractionsBrand = brands.reduce((a, b) => data[a].total_interactions > data[b].total_interactions ? a : b);
    
    // 找出互動率最高的品牌
    const highestRateBrand = brands.reduce((a, b) => data[a].interaction_rate > data[b].interaction_rate ? a : b);
    
    // 更新洞察列表
    const insightsList = document.getElementById('insights-list');
    insightsList.innerHTML = `
        <li><strong>${mostPostsBrand}</strong> 發布了最多貼文，總計 ${data[mostPostsBrand].post_count} 篇。</li>
        <li><strong>${mostInteractionsBrand}</strong> 獲得了最高的總互動量，達 ${data[mostInteractionsBrand].total_interactions} 次。</li>
        <li><strong>${highestRateBrand}</strong> 擁有最高的互動效率，每則貼文平均獲得 ${(data[highestRateBrand].interaction_rate * 1000).toFixed(2)} 互動（每千人）。</li>
        <li>整體而言，讚數是最常見的互動方式，其次是留言和分享。</li>
    `;
    console.log('洞察列表更新完成');
} 