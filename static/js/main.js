// 頁面載入時執行
document.addEventListener('DOMContentLoaded', function() {
    // 此處可以放置適用於整個網站的全局初始化代碼
    // 例如：初始化所有頁面的 Tooltips 或 Modals (如果需要)
    // if (typeof bootstrap !== 'undefined') {
    //     const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    //     tooltipTriggerList.map(function (tooltipTriggerEl) {
    //         return new bootstrap.Tooltip(tooltipTriggerEl);
    //     });
    // }
    console.log("Global main.js loaded. Dashboard-specific logic is handled in dashboard.html.");
});

// 可以保留其他非 dashboard 特有的全局輔助函數（如果有的話）
// 已移除所有 dashboard 相關的變數和函數