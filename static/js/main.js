document.addEventListener('DOMContentLoaded', function() {
    // 簡單的頁面載入動畫
    const sections = document.querySelectorAll('section');
    
    setTimeout(() => {
        sections.forEach((section, index) => {
            setTimeout(() => {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }, 300);
    
    // 檢查是否在首頁
    const brandCardsContainer = document.getElementById('brand-cards-container');
    if (brandCardsContainer) {
        loadBrandCards();
    }
    
    // 檢查URL參數，如果是品牌詳情頁面則加載相應數據
    const urlParams = new URLSearchParams(window.location.search);
    const brandParam = urlParams.get('brand');
    if (brandParam && window.location.pathname.includes('brand_detail.html')) {
        loadBrandDetail(brandParam);
    }
});

// 加載品牌卡片
function loadBrandCards() {
    fetch('./static/data/brands.json')
        .then(response => response.json())
        .then(brands => {
            const container = document.getElementById('brand-cards-container');
            
            // 清空容器
            container.innerHTML = '';
            
            // 按名稱排序品牌
            brands.sort((a, b) => a.name.localeCompare(b.name));
            
            // 為每個品牌創建卡片
            brands.forEach(brand => {
                const brandLink = document.createElement('a');
                brandLink.href = `brand_detail.html?brand=${brand.name}`;
                brandLink.className = 'brand-card-link';
                
                const brandCard = document.createElement('div');
                brandCard.className = 'brand-card';
                
                brandCard.innerHTML = `
                    <div class="brand-logo-placeholder">
                        <i class="fas fa-mug-hot"></i>
                    </div>
                    <h3>${brand.name}</h3>
                    <div class="brand-card-hint">
                        點擊查看詳情
                        <i class="fas fa-arrow-right"></i>
                    </div>
                `;
                
                brandLink.appendChild(brandCard);
                container.appendChild(brandLink);
            });
        })
        .catch(error => {
            console.error('Error loading brand data:', error);
            document.getElementById('brand-cards-container').innerHTML = 
                '<p class="error-message">載入品牌數據時發生錯誤</p>';
        });
}

// 加載品牌詳細信息
function loadBrandDetail(brandName) {
    // 設置頁面標題
    document.title = `${brandName} - 飲料社群粉絲專頁分析`;
    
    // 更新頁面中的品牌名稱
    const brandTitleElements = document.querySelectorAll('.brand-title');
    brandTitleElements.forEach(el => {
        el.textContent = brandName;
    });
    
    // 使用標準化的路徑來加載品牌詳細數據
    const paths = [
        `./static/data/brand_detail_${brandName}.json`
    ];
    
    // 定義加載函數
    function tryLoadFromPaths(pathIndex = 0) {
        if (pathIndex >= paths.length) {
            // 所有路徑都嘗試過了但失敗了
            console.error('無法找到品牌數據，所有路徑嘗試失敗');
            const mainContent = document.querySelector('main');
            if (mainContent) {
                mainContent.innerHTML = `
                    <div class="error-container">
                        <h2>載入品牌數據時發生錯誤</h2>
                        <p>無法找到 ${brandName} 的詳細數據。</p>
                        <a href="index.html" class="btn-view">返回首頁</a>
                    </div>
                `;
            }
            return;
        }
        
        const currentPath = paths[pathIndex];
        console.log(`嘗試從路徑加載: ${currentPath}`);
        
        fetch(currentPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('品牌數據不存在');
                }
                return response.json();
            })
            .then(data => {
                console.log('載入的品牌數據:', data);
                
                // 填充統計數據
                if (data.stats) {
                    const statsContainer = document.getElementById('brand-stats');
                    if (statsContainer) {
                        statsContainer.innerHTML = `
                            <div class="stat-item">
                                <span class="stat-number">${data.stats.post_count || data.stats.total_posts || 0}</span>
                                <span class="stat-label">總貼文數</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${data.stats.total_likes || 0}</span>
                                <span class="stat-label">總讚數</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${data.stats.total_comments || 0}</span>
                                <span class="stat-label">總留言數</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${data.stats.total_shares || 0}</span>
                                <span class="stat-label">總分享數</span>
                            </div>
                        `;
                    }
                }
                
                // 填充最近貼文
                if (data.recent_posts) {
                    const postsContainer = document.getElementById('recent-posts');
                    if (postsContainer) {
                        postsContainer.innerHTML = '';
                        
                        if (data.recent_posts.length === 0) {
                            postsContainer.innerHTML = '<p>沒有近期貼文資料</p>';
                            return;
                        }
                        
                        data.recent_posts.forEach(post => {
                            const postElement = document.createElement('div');
                            postElement.className = 'post-item';
                            
                            postElement.innerHTML = `
                                <div class="post-date">${post.date || '無日期'}</div>
                                <div class="post-content">${post.content || '無內容'}</div>
                                <div class="post-stats">
                                    <span><i class="fas fa-thumbs-up"></i> ${post.like || 0}</span>
                                    <span><i class="fas fa-comment"></i> ${post.comment || 0}</span>
                                    <span><i class="fas fa-share"></i> ${post.share || 0}</span>
                                </div>
                            `;
                            
                            postsContainer.appendChild(postElement);
                        });
                    }
                } else {
                    const postsContainer = document.getElementById('recent-posts');
                    if (postsContainer) {
                        postsContainer.innerHTML = '<p>沒有貼文數據</p>';
                    }
                }
            })
            .catch(error => {
                console.error(`從 ${currentPath} 加載數據失敗:`, error);
                // 嘗試下一個路徑
                tryLoadFromPaths(pathIndex + 1);
            });
    }
    
    // 開始嘗試加載
    tryLoadFromPaths();
} 