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
    
    // 在這裡可以添加更多的JavaScript功能
}); 