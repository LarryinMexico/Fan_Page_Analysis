document.addEventListener('DOMContentLoaded', function() {
    // 模擬數據 - 實際開發時可替換為從後端API獲取的數據
    
    // 品牌互動率比較圖表
    const interactionData = {
        brands: ['品牌A', '品牌B', '品牌C', '品牌D', '品牌E'],
        rates: [0.023, 0.015, 0.032, 0.018, 0.027]
    };
    
    // 貼文類型效果分析圖表
    const postTypeData = {
        types: ['促銷活動', '新品介紹', '品牌故事', '節日活動', '用戶分享'],
        likes: [1200, 850, 650, 950, 750],
        shares: [320, 250, 150, 280, 420],
        comments: [180, 120, 90, 110, 230]
    };
    
    // 粉絲增長趨勢圖表
    const growthData = {
        months: ['1月', '2月', '3月', '4月', '5月', '6月'],
        brandA: [10000, 10500, 11200, 12000, 13500, 15000],
        brandB: [8500, 8800, 9200, 9500, 10200, 11000],
        brandC: [12000, 12300, 12800, 13500, 14200, 15500]
    };
    
    // 初始化圖表
    createInteractionChart();
    createPostTypeChart();
    createGrowthChart();
    
    // 品牌互動率比較圖表
    function createInteractionChart() {
        const trace = {
            x: interactionData.brands,
            y: interactionData.rates.map(rate => (rate * 100).toFixed(2)),
            type: 'bar',
            marker: {
                color: '#1e88e5'
            },
            text: interactionData.rates.map(rate => (rate * 100).toFixed(2) + '%'),
            textposition: 'auto'
        };
        
        const layout = {
            title: '品牌互動率比較 (%)',
            yaxis: {
                title: '互動率 (%)'
            },
            bargap: 0.3
        };
        
        Plotly.newPlot('interaction-chart', [trace], layout);
    }
    
    // 貼文類型效果分析圖表
    function createPostTypeChart() {
        const trace1 = {
            x: postTypeData.types,
            y: postTypeData.likes,
            name: '按讚',
            type: 'bar'
        };
        
        const trace2 = {
            x: postTypeData.types,
            y: postTypeData.shares,
            name: '分享',
            type: 'bar'
        };
        
        const trace3 = {
            x: postTypeData.types,
            y: postTypeData.comments,
            name: '留言',
            type: 'bar'
        };
        
        const layout = {
            title: '貼文類型效果分析',
            barmode: 'group',
            yaxis: {
                title: '互動次數'
            },
            bargap: 0.2
        };
        
        Plotly.newPlot('post-type-chart', [trace1, trace2, trace3], layout);
    }
    
    // 粉絲增長趨勢圖表
    function createGrowthChart() {
        const trace1 = {
            x: growthData.months,
            y: growthData.brandA,
            name: '品牌A',
            type: 'scatter',
            mode: 'lines+markers',
            line: {shape: 'spline', width: 3}
        };
        
        const trace2 = {
            x: growthData.months,
            y: growthData.brandB,
            name: '品牌B',
            type: 'scatter',
            mode: 'lines+markers',
            line: {shape: 'spline', width: 3}
        };
        
        const trace3 = {
            x: growthData.months,
            y: growthData.brandC,
            name: '品牌C',
            type: 'scatter',
            mode: 'lines+markers',
            line: {shape: 'spline', width: 3}
        };
        
        const layout = {
            title: '粉絲增長趨勢圖',
            yaxis: {
                title: '粉絲數量'
            },
            xaxis: {
                title: '月份'
            }
        };
        
        Plotly.newPlot('growth-chart', [trace1, trace2, trace3], layout);
    }
}); 