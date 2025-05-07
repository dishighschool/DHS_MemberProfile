/**
 * 統一管理的漸層背景定義
 * 這個文件定義了所有可用的背景漸層，方便在不同頁面共享和使用
 */

// 漸層對象庫 - 包含所有可用的漸層定義
const GRADIENT_LIBRARY = {
    // 預設漸層
    'default': {
        name: '預設紫',
        cssValue: 'linear-gradient(135deg, #1A0038 0%, #32007A 50%, #6237A0 100%)',
        previewClass: 'gradient-default',
        description: '預設深紫色漸層',
    },
    // 午夜海洋
    'midnight-ocean': {
        name: '午夜海洋',
        cssValue: 'linear-gradient(135deg, #020024 0%, #090979 35%, #00d4ff 100%)',
        previewClass: 'gradient-midnight-ocean',
        description: '深藍到淺藍的海洋風格漸層',
    },
    // 日落餘暉
    'sunset': {
        name: '日落餘暉',
        cssValue: 'linear-gradient(135deg, #ff4e50 0%, #f9d423 100%)',
        previewClass: 'gradient-sunset',
        description: '紅色到黃色的夕陽漸層',
    },
    // 極光綠
    'aurora': {
        name: '極光綠',
        cssValue: 'linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%)',
        previewClass: 'gradient-aurora',
        description: '深藍到綠色的極光漸層',
    },
    // 宇宙漫遊
    'cosmic': {
        name: '宇宙漫遊',
        cssValue: 'linear-gradient(135deg, #3E1E68 0%, #834D9B 100%)',
        previewClass: 'gradient-cosmic',
        description: '紫色系宇宙風漸層',
    },
    // 森林幽境
    'forest': {
        name: '森林幽境',
        cssValue: 'linear-gradient(135deg, #134E5E 0%, #71B280 100%)',
        previewClass: 'gradient-forest',
        description: '深綠到淺綠的森林風格漸層',
    },
    // 櫻花飄雪 - 改善版
    'cherry': {
        name: '櫻花飄雪',
        cssValue: 'linear-gradient(135deg, #EB3349 0%, #FF98B7 50%, #F45C43 100%)',
        previewClass: 'gradient-cherry',
        description: '櫻花粉紅與暖橙色的溫柔漸層',
    },
    // 冬日寧靜
    'winter': {
        name: '冬日寧靜',
        cssValue: 'linear-gradient(135deg, #8e9eab 0%, #eef2f3 100%)',
        previewClass: 'gradient-winter',
        description: '灰色到白色的冬季風格漸層',
    },
    
    // --- 新增漸層 ---
    
    // 深海藍寶
    'deep-ocean': {
        name: '深海藍寶',
        cssValue: 'linear-gradient(135deg, #1A2980 0%, #26D0CE 100%)',
        previewClass: 'gradient-deep-ocean',
        description: '深藍至青綠的海洋漸層',
    },
    // 薰衣草田
    'lavender': {
        name: '薰衣草田',
        cssValue: 'linear-gradient(135deg, #654EA3 0%, #EAAFC8 100%)',
        previewClass: 'gradient-lavender',
        description: '紫色至粉色的薰衣草風格漸層',
    },
    // 金色黎明
    'golden-dawn': {
        name: '金色黎明',
        cssValue: 'linear-gradient(135deg, #F37335 0%, #FDC830 100%)',
        previewClass: 'gradient-golden-dawn',
        description: '橙色到金黃色的溫暖漸層',
    },
    // 翡翠山脈
    'emerald': {
        name: '翡翠山脈',
        cssValue: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        previewClass: 'gradient-emerald',
        description: '綠寶石色系的清新漸層',
    },
    // 靜謐夜空
    'night-sky': {
        name: '靜謐夜空',
        cssValue: 'linear-gradient(135deg, #0F2027 0%, #2C5364 70%, #203A43 100%)',
        previewClass: 'gradient-night-sky',
        description: '深藍色調的寧靜夜空',
    },
    // 科技藍調
    'tech-blue': {
        name: '科技藍調',
        cssValue: 'linear-gradient(135deg, #061161 0%, #30cfd0 100%)',
        previewClass: 'gradient-tech-blue',
        description: '科技感十足的藍色漸層',
    }
};

/**
 * 根據漸層ID獲取漸層對象
 * @param {string} gradientId - 漸層ID
 * @return {object} 漸層對象或預設漸層
 */
function getGradient(gradientId) {
    return GRADIENT_LIBRARY[gradientId] || GRADIENT_LIBRARY['default'];
}

/**
 * 獲取漸層CSS值
 * @param {string} gradientId - 漸層ID
 * @return {string} CSS漸層值
 */
function getGradientCSS(gradientId) {
    return getGradient(gradientId).cssValue;
}

/**
 * 獲取所有可用漸層
 * @return {object} 所有漸層對象
 */
function getAllGradients() {
    return GRADIENT_LIBRARY;
}

/**
 * 生成用於CSS變數的漸層樣式表
 * @return {string} 包含所有漸層預覽類的CSS樣式
 */
function generateGradientStyles() {
    let styles = '';
    
    Object.keys(GRADIENT_LIBRARY).forEach(id => {
        const gradient = GRADIENT_LIBRARY[id];
        styles += `.${gradient.previewClass} { background: ${gradient.cssValue}; }\n`;
    });
    
    return styles;
}

// 如果在瀏覽器環境中，將函數掛載到全局對象上
if (typeof window !== 'undefined') {
    window.GradientManager = {
        getGradient,
        getGradientCSS, 
        getAllGradients,
        generateGradientStyles
    };
}