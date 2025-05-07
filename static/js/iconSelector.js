/**
 * IconSelector - 模組化圖標選擇器
 * 此模組提供可重複使用的圖標選擇功能，可在多個頁面中重複使用
 * 支持 Font Awesome 5 圖標
 */

window.IconSelector = (function() {
    // 圖標類型分類
    const ICON_CATEGORIES = {
        'common': {
            name: '常用',
            icons: [
                'fas fa-tag', 'fas fa-tags', 'fas fa-bookmark', 'fas fa-star',
                'fas fa-heart', 'fas fa-user', 'fas fa-users', 'fas fa-home',
                'fas fa-cog', 'fas fa-wrench', 'fas fa-search', 'fas fa-globe',
                'fas fa-link', 'fas fa-check', 'fas fa-times', 'fas fa-question'
            ]
        },
        'user': {
            name: '用戶',
            icons: [
                'fas fa-user', 'fas fa-user-tie', 'fas fa-user-graduate', 'fas fa-user-ninja',
                'fas fa-user-astronaut', 'fas fa-user-shield', 'fas fa-user-check', 'fas fa-user-clock',
                'fas fa-user-cog', 'fas fa-user-edit', 'fas fa-user-md', 'fas fa-user-tag',
                'fas fa-user-secret', 'fas fa-users', 'fas fa-users-cog', 'fas fa-user-friends'
            ]
        },
        'development': {
            name: '開發',
            icons: [
                'fas fa-code', 'fas fa-terminal', 'fas fa-laptop-code', 'fas fa-bug',
                'fas fa-server', 'fas fa-database', 'fas fa-cloud', 'fas fa-cogs',
                'fas fa-microchip', 'fas fa-keyboard', 'fas fa-robot', 'fas fa-sitemap',
                'fas fa-project-diagram', 'fas fa-network-wired', 'fas fa-code-branch', 'fas fa-layer-group'
            ]
        },
        'design': {
            name: '設計',
            icons: [
                'fas fa-palette', 'fas fa-paint-brush', 'fas fa-pencil-ruler', 'fas fa-ruler-combined',
                'fas fa-crop', 'fas fa-drafting-compass', 'fas fa-bezier-curve', 'fas fa-vector-square',
                'fas fa-brush', 'fas fa-fill', 'fas fa-fill-drip', 'fas fa-swatchbook',
                'fas fa-tint', 'fas fa-shapes', 'fas fa-object-group', 'fas fa-object-ungroup'
            ]
        },
        'media': {
            name: '媒體',
            icons: [
                'fas fa-image', 'fas fa-camera', 'fas fa-video', 'fas fa-film',
                'fas fa-photo-video', 'fas fa-music', 'fas fa-headphones', 'fas fa-microphone',
                'fas fa-play', 'fas fa-stop', 'fas fa-pause', 'fas fa-volume-up',
                'fas fa-broadcast-tower', 'fas fa-podcast', 'fas fa-compact-disc', 'fas fa-record-vinyl'
            ]
        },
        'education': {
            name: '教育',
            icons: [
                'fas fa-book', 'fas fa-book-open', 'fas fa-bookmark', 'fas fa-graduation-cap',
                'fas fa-school', 'fas fa-chalkboard', 'fas fa-chalkboard-teacher', 'fas fa-university',
                'fas fa-atom', 'fas fa-flask', 'fas fa-microscope', 'fas fa-brain',
                'fas fa-glasses', 'fas fa-user-graduate', 'fas fa-award', 'fas fa-certificate'
            ]
        },
        'business': {
            name: '商業',
            icons: [
                'fas fa-briefcase', 'fas fa-chart-line', 'fas fa-chart-bar', 'fas fa-chart-pie',
                'fas fa-chart-area', 'fas fa-money-bill', 'fas fa-coins', 'fas fa-credit-card',
                'fas fa-file-invoice-dollar', 'fas fa-hand-holding-usd', 'fas fa-piggy-bank', 'fas fa-percentage',
                'fas fa-dollar-sign', 'fas fa-euro-sign', 'fas fa-yen-sign', 'fas fa-bitcoin'
            ]
        },
        'communication': {
            name: '通訊',
            icons: [
                'fas fa-envelope', 'fas fa-inbox', 'fas fa-paper-plane', 'fas fa-comment',
                'fas fa-comments', 'fas fa-comment-alt', 'fas fa-comment-dots', 'fas fa-sms',
                'fas fa-phone', 'fas fa-phone-alt', 'fas fa-mobile-alt', 'fas fa-fax',
                'fas fa-satellite-dish', 'fas fa-wifi', 'fas fa-rss', 'fas fa-share-alt'
            ]
        },
        'social': {
            name: '社交媒體',
            icons: [
                'fab fa-facebook', 'fab fa-twitter', 'fab fa-instagram', 'fab fa-youtube',
                'fab fa-tiktok', 'fab fa-discord', 'fab fa-github', 'fab fa-gitlab',
                'fab fa-linkedin', 'fab fa-twitch', 'fab fa-reddit', 'fab fa-pinterest',
                'fab fa-snapchat', 'fab fa-telegram', 'fab fa-whatsapp', 'fab fa-medium'
            ]
        },
        'awards': {
            name: '獎勵',
            icons: [
                'fas fa-trophy', 'fas fa-medal', 'fas fa-award', 'fas fa-crown',
                'fas fa-certificate', 'fas fa-star', 'fas fa-ribbon', 'fas fa-gem',
                'fas fa-award', 'fas fa-thumbs-up', 'fas fa-heart', 'fas fa-bell', 
                'fas fa-fire', 'fas fa-bolt', 'fas fa-gift', 'fas fa-sun'
            ]
        },
        'other': {
            name: '其他',
            icons: [
                'fas fa-lightbulb', 'fas fa-chess', 'fas fa-gamepad', 'fas fa-puzzle-piece',
                'fas fa-dice', 'fas fa-bicycle', 'fas fa-car', 'fas fa-plane',
                'fas fa-rocket', 'fas fa-globe', 'fas fa-map-marker-alt', 'fas fa-flag',
                'fas fa-paw', 'fas fa-leaf', 'fas fa-coffee', 'fas fa-utensils'
            ]
        }
    };

    // 在頁面上創建圖標選擇器模態框
    function createModal() {
        // 如果已存在，直接返回
        if (document.getElementById('iconSelectorModal')) {
            return document.getElementById('iconSelectorModal');
        }

        // 創建模態框HTML
        const modalHTML = `
        <div class="modal fade" id="iconSelectorModal" tabindex="-1" aria-labelledby="iconSelectorModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="iconSelectorModalLabel">選擇圖標</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <input type="text" class="form-control icon-search mb-3" placeholder="搜尋圖標..." id="iconSearchInput">
                        
                        <div class="icon-filter-buttons mb-3">
                            <button type="button" class="btn btn-sm btn-outline-primary me-2 icon-filter-button active" data-category="all">所有圖標</button>
                            ${Object.keys(ICON_CATEGORIES).map(category => 
                                `<button type="button" class="btn btn-sm btn-outline-primary me-2 icon-filter-button" data-category="${category}">
                                    ${ICON_CATEGORIES[category].name}
                                </button>`
                            ).join('')}
                        </div>
                        
                        <div id="iconCategories">
                            ${Object.keys(ICON_CATEGORIES).map(category => `
                                <div class="icon-category" data-category="${category}">
                                    <div class="icon-category-title">${ICON_CATEGORIES[category].name}</div>
                                    <div class="icon-grid">
                                        ${ICON_CATEGORIES[category].icons.map(icon => `
                                            <div class="icon-item" data-icon="${icon}" title="${icon}">
                                                <i class="${icon}"></i>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary" id="selectIconBtn">選擇</button>
                    </div>
                </div>
            </div>
        </div>`;

        // 插入DOM
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHTML.trim();
        document.body.appendChild(modalContainer.firstChild);

        return document.getElementById('iconSelectorModal');
    }

    // 初始化圖標選擇器
    function init(options = {}) {
        const modalElement = createModal();
        const modal = new bootstrap.Modal(modalElement);
        
        // 默認配置
        const config = {
            onSelect: (iconClass) => { console.log('Selected icon:', iconClass); },
            iconInputSelector: null,
            iconPreviewSelector: null,
            buttonSelector: null,
            initialIcon: 'fas fa-tag'
        };
        
        // 合併用戶配置
        Object.assign(config, options);
        
        let selectedIcon = config.initialIcon;
        
        // 獲取DOM元素
        const iconItems = modalElement.querySelectorAll('.icon-item');
        const searchInput = modalElement.querySelector('#iconSearchInput');
        const selectButton = modalElement.querySelector('#selectIconBtn');
        const filterButtons = modalElement.querySelectorAll('.icon-filter-button');
        const iconCategories = modalElement.querySelectorAll('.icon-category');
        
        // 如果提供了按鈕選擇器，綁定打開模態框事件
        if (config.buttonSelector) {
            const button = document.querySelector(config.buttonSelector);
            if (button) {
                button.addEventListener('click', () => {
                    // 如果提供了輸入框選擇器，獲取當前圖標
                    if (config.iconInputSelector) {
                        const iconInput = document.querySelector(config.iconInputSelector);
                        if (iconInput) {
                            selectedIcon = iconInput.value;
                        }
                    }
                    
                    // 高亮顯示當前選中的圖標
                    iconItems.forEach(item => {
                        if (item.getAttribute('data-icon') === selectedIcon) {
                            item.classList.add('selected');
                            // 滾動到可視區域
                            item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        } else {
                            item.classList.remove('selected');
                        }
                    });
                    
                    // 打開模態框
                    modal.show();
                });
            }
        }
        
        // 綁定圖標點擊事件
        iconItems.forEach(item => {
            item.addEventListener('click', function() {
                const iconClass = this.getAttribute('data-icon');
                iconItems.forEach(i => i.classList.remove('selected'));
                this.classList.add('selected');
                selectedIcon = iconClass;
            });
        });
        
        // 綁定搜索功能
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            iconItems.forEach(item => {
                const iconClass = item.getAttribute('data-icon').toLowerCase();
                if (iconClass.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });

            // 隱藏沒有可見圖標的類別
            iconCategories.forEach(category => {
                const visibleIcons = category.querySelectorAll('.icon-item[style=""]');
                if (visibleIcons.length === 0) {
                    category.style.display = 'none';
                } else {
                    category.style.display = '';
                }
            });
        });
        
        // 綁定過濾器按鈕
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                
                // 更新按鈕活動狀態
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // 過濾圖標類別
                if (category === 'all') {
                    iconCategories.forEach(cat => {
                        cat.style.display = '';
                    });
                } else {
                    iconCategories.forEach(cat => {
                        if (cat.getAttribute('data-category') === category) {
                            cat.style.display = '';
                        } else {
                            cat.style.display = 'none';
                        }
                    });
                }
            });
        });
        
        // 綁定選擇按鈕
        selectButton.addEventListener('click', function() {
            // 如果提供了輸入框選擇器，更新輸入框值
            if (config.iconInputSelector) {
                const iconInput = document.querySelector(config.iconInputSelector);
                if (iconInput) {
                    iconInput.value = selectedIcon;
                    // 觸發 change 事件，以便其他腳本可以監聽
                    iconInput.dispatchEvent(new Event('change'));
                }
            }
            
            // 如果提供了預覽選擇器，更新預覽
            if (config.iconPreviewSelector) {
                const iconPreview = document.querySelector(config.iconPreviewSelector);
                if (iconPreview) {
                    iconPreview.innerHTML = `<i class="${selectedIcon}"></i>`;
                }
            }
            
            // 調用回調函數
            config.onSelect(selectedIcon);
            
            // 關閉模態框
            modal.hide();
        });
        
        // 返回控制對象
        return {
            modal: modal,
            show: () => modal.show(),
            hide: () => modal.hide(),
            getSelectedIcon: () => selectedIcon,
            setSelectedIcon: (iconClass) => {
                selectedIcon = iconClass;
                iconItems.forEach(item => {
                    if (item.getAttribute('data-icon') === iconClass) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                });
            }
        };
    }
    
    // 暴露公共方法
    return {
        init: init,
        getAllCategories: () => ICON_CATEGORIES
    };
})();