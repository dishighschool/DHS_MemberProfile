// Font Awesome Icon Picker - 簡化版本
const FONTAWESOME_ICONS = {
  'brands': [
    'facebook', 'twitter', 'instagram', 'linkedin', 'github', 'gitlab', 'discord', 'youtube',
    'twitch', 'reddit', 'pinterest', 'medium', 'dev', 'dribbble', 'behance', 'codepen',
    'stack-overflow', 'vimeo', 'telegram', 'whatsapp', 'snapchat', 'tiktok', 'spotify',
    'steam', 'playstation', 'xbox', 'google', 'apple', 'microsoft', 'amazon', 'paypal'
  ],
  'solid': [
    'envelope', 'phone', 'globe', 'link', 'home', 'user', 'users', 'heart', 'star',
    'comment', 'message', 'chat', 'bell', 'calendar', 'clock', 'map-marker-alt', 'location-dot',
    'camera', 'image', 'video', 'music', 'gamepad', 'code', 'terminal', 'laptop', 'mobile',
    'desktop', 'tablet', 'book', 'graduation-cap', 'briefcase', 'shopping-cart', 'shopping-bag',
    'credit-card', 'dollar-sign', 'gift', 'trophy', 'medal', 'bookmark', 'flag', 'tag', 'tags',
    'rss', 'wifi', 'signal', 'download', 'upload', 'cloud', 'database', 'server', 'network-wired'
  ],
  'regular': [
    'envelope', 'comment', 'comments', 'heart', 'star', 'bookmark', 'bell', 'calendar',
    'clock', 'file', 'folder', 'image', 'lightbulb', 'thumbs-up', 'thumbs-down', 'user',
    'circle', 'square', 'hand-point-right', 'hand-point-left'
  ]
};

class FontAwesomeIconPicker {
  constructor(input) {
    this.input = input;
    
    // 確保父元素有相對定位
    if (this.input.parentElement.style.position !== 'relative') {
      this.input.parentElement.style.position = 'relative';
    }
    
    // 創建包裝容器
    this.wrapper = document.createElement('div');
    this.wrapper.className = 'icon-picker-wrapper';
    this.wrapper.style.position = 'relative';
    this.wrapper.style.display = 'block';
    
    // 將 input 包裝起來
    this.input.parentNode.insertBefore(this.wrapper, this.input);
    this.wrapper.appendChild(this.input);
    
    // 創建圖示預覽元素
    this.preview = document.createElement('span');
    this.preview.className = 'icon-preview-badge';
    this.wrapper.appendChild(this.preview);
    
    // 創建下拉選單
    this.createDropdown();
    
    // 綁定事件
    this.input.addEventListener('click', (e) => {
      e.preventDefault();
      this.toggle();
    });
    
    // 點擊外部關閉
    document.addEventListener('click', (e) => {
      if (!this.dropdown.contains(e.target) && e.target !== this.input && e.target !== this.preview) {
        this.close();
      }
    });
    
    // 允許手動輸入
    this.input.addEventListener('input', () => {
      this.updateInputPreview();
    });
    
    // 更新預覽
    this.updateInputPreview();
  }
  
  createDropdown() {
    this.dropdown = document.createElement('div');
    this.dropdown.className = 'icon-picker-dropdown-simple';
    this.dropdown.style.display = 'none';
    
    // 提示文字
    const hint = document.createElement('small');
    hint.className = 'text-muted d-block mb-2';
    hint.textContent = '💡 提示：可直接在輸入框輸入自訂圖示代碼（如 fas fa-home）';
    
    // 搜尋框
    this.searchBox = document.createElement('input');
    this.searchBox.type = 'text';
    this.searchBox.className = 'form-control form-control-sm mb-2';
    this.searchBox.placeholder = '搜尋圖示...';
    this.searchBox.addEventListener('input', (e) => {
      e.stopPropagation();
      this.filter(e.target.value);
    });
    this.searchBox.addEventListener('click', (e) => e.stopPropagation());
    this.searchBox.addEventListener('keydown', (e) => e.stopPropagation());
    
    // 類別選擇
    this.categorySelect = document.createElement('div');
    this.categorySelect.className = 'btn-group w-100 mb-2';
    this.categorySelect.setAttribute('role', 'group');
    
    const categories = [
      { key: 'brands', label: '品牌', icon: 'fab fa-font-awesome' },
      { key: 'solid', label: '實心', icon: 'fas fa-icons' },
      { key: 'regular', label: '空心', icon: 'far fa-circle' }
    ];
    
    categories.forEach(cat => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'btn btn-sm btn-outline-secondary';
      btn.innerHTML = `<i class="${cat.icon}"></i> ${cat.label}`;
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.categorySelect.querySelectorAll('button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.renderIcons(cat.key);
      });
      if (cat.key === 'brands') btn.classList.add('active');
      this.categorySelect.appendChild(btn);
    });
    
    // 圖示網格
    this.grid = document.createElement('div');
    this.grid.className = 'icon-picker-grid-simple';
    
    // 按鈕區
    const btnGroup = document.createElement('div');
    btnGroup.className = 'd-flex gap-2 mt-2';
    
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn btn-sm btn-secondary flex-fill';
    clearBtn.innerHTML = '<i class="fas fa-times"></i> 清除';
    clearBtn.addEventListener('click', () => {
      this.select('');
      this.close();
    });
    
    const customBtn = document.createElement('button');
    customBtn.type = 'button';
    customBtn.className = 'btn btn-sm btn-primary flex-fill';
    customBtn.innerHTML = '<i class="fas fa-keyboard"></i> 自訂輸入';
    customBtn.addEventListener('click', () => {
      this.close();
      this.input.readOnly = false;
      this.input.focus();
      this.input.select();
    });
    
    btnGroup.appendChild(clearBtn);
    btnGroup.appendChild(customBtn);
    
    this.dropdown.appendChild(hint);
    this.dropdown.appendChild(this.categorySelect);
    this.dropdown.appendChild(this.searchBox);
    this.dropdown.appendChild(this.grid);
    this.dropdown.appendChild(btnGroup);

    // 根據所在位置選擇容器
    this.appendTarget = this.input.closest('.modal') || document.body;
    this.appendTarget.appendChild(this.dropdown);
    
    // 渲染品牌圖示
    this.renderIcons('brands');
  }
  
  renderIcons(category, searchQuery = '') {
    this.grid.innerHTML = '';
    const prefix = category === 'brands' ? 'fab' : (category === 'regular' ? 'far' : 'fas');
    let icons = FONTAWESOME_ICONS[category] || [];
    
    // 過濾搜尋
    if (searchQuery) {
      icons = icons.filter(icon => icon.toLowerCase().includes(searchQuery.toLowerCase()));
    }
    
    // 限制顯示數量
    icons.slice(0, 100).forEach(icon => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'icon-picker-item-simple';
      btn.innerHTML = `<i class="${prefix} fa-${icon}"></i>`;
      btn.title = icon;
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.select(`${prefix} fa-${icon}`);
        this.close();
      });
      this.grid.appendChild(btn);
    });
    
    if (icons.length === 0) {
      const noResult = document.createElement('div');
      noResult.className = 'text-center text-muted py-3';
      noResult.textContent = '找不到符合的圖示';
      this.grid.appendChild(noResult);
    }
  }
  
  filter(query) {
    const activeBtn = this.categorySelect.querySelector('button.active');
    const category = activeBtn ? 
      (activeBtn.textContent.includes('品牌') ? 'brands' : 
       (activeBtn.textContent.includes('空心') ? 'regular' : 'solid')) : 'brands';
    this.renderIcons(category, query);
  }
  
  select(iconClass) {
    this.input.value = iconClass;
    this.input.readOnly = true;
    this.updateInputPreview();
    
    // 觸發 change 事件
    const event = new Event('change', { bubbles: true });
    this.input.dispatchEvent(event);
  }
  
  updateInputPreview() {
    const iconClass = this.input.value.trim();
    if (iconClass) {
      this.input.style.paddingLeft = '2.5rem';
      this.preview.innerHTML = `<i class="${iconClass}"></i>`;
      this.preview.style.display = 'inline-flex';
    } else {
      this.preview.style.display = 'none';
      this.input.style.paddingLeft = '';
    }
  }
  
  toggle() {
    if (this.dropdown.style.display === 'none') {
      this.open();
    } else {
      this.close();
    }
  }
  
  open() {
    // 檢查是否在 Modal 中
    const modal = this.input.closest('.modal');
    const inModal = modal !== null;

    // 如果容器變動，確保 dropdown 附加在正確位置
    const expectedContainer = modal || document.body;
    if (this.appendTarget !== expectedContainer) {
      this.appendTarget = expectedContainer;
      if (this.dropdown.parentNode) {
        this.dropdown.parentNode.removeChild(this.dropdown);
      }
      this.appendTarget.appendChild(this.dropdown);
    }
    
    // 定位下拉選單
    const rect = this.input.getBoundingClientRect();
    this.dropdown.style.display = 'block';
    this.dropdown.style.position = 'fixed';
    this.dropdown.style.left = rect.left + 'px';
    
    // 根據空間決定向上或向下顯示
    const viewportHeight = window.innerHeight;
    const spaceBelow = viewportHeight - rect.bottom;
    const dropdownHeight = 500;
    
    if (spaceBelow < dropdownHeight && rect.top > dropdownHeight) {
      // 向上顯示
      this.dropdown.style.bottom = (viewportHeight - rect.top + 5) + 'px';
      this.dropdown.style.top = 'auto';
    } else {
      // 向下顯示
      this.dropdown.style.top = (rect.bottom + 5) + 'px';
      this.dropdown.style.bottom = 'auto';
    }
    
    this.dropdown.style.width = Math.max(rect.width, 320) + 'px';
    this.dropdown.style.zIndex = inModal ? '10000' : '9999';
    
    // 清空並聚焦搜尋框
    if (this.searchBox) {
      this.searchBox.value = '';
      const activeBtn = this.categorySelect.querySelector('button.active');
      const category = activeBtn ? 
        (activeBtn.textContent.includes('品牌') ? 'brands' : 
         (activeBtn.textContent.includes('空心') ? 'regular' : 'solid')) : 'brands';
      this.renderIcons(category);
      
      requestAnimationFrame(() => {
        this.searchBox.focus();
        this.searchBox.select();
      });
    }
  }
  
  close() {
    this.dropdown.style.display = 'none';
    if (this.searchBox) {
      this.searchBox.value = '';
    }
  }
}

// 添加 CSS 樣式
const style = document.createElement('style');
style.textContent = `
.icon-picker-wrapper {
  position: relative;
  display: block;
}

.icon-preview-badge {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  display: none;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  color: #6c757d;
  font-size: 1.1rem;
  pointer-events: none;
  z-index: 5;
}

.icon-picker-dropdown-simple {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 15px;
  max-height: 500px;
  overflow-y: auto;
  z-index: 9999;
}

.icon-picker-grid-simple {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
  padding: 5px;
  background: #f8f9fa;
  border-radius: 6px;
  margin: 10px 0;
}

.icon-picker-item-simple {
  width: 45px;
  height: 45px;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  font-size: 1.2rem;
  color: #495057;
}

.icon-picker-item-simple:hover {
  border-color: #6c5ce7;
  background: #f0edff;
  transform: scale(1.1);
}

.icon-picker-item-simple:active {
  transform: scale(0.95);
}
`;
document.head.appendChild(style);

// 自動初始化函式
function initFontAwesomeIconPickers() {
  document.querySelectorAll('.icon-picker-input').forEach(input => {
    if (!input.dataset.iconPickerInit && !input.closest('.icon-picker-wrapper')) {
      new FontAwesomeIconPicker(input);
      input.dataset.iconPickerInit = 'true';
    }
  });
}

// 頁面載入時自動初始化
document.addEventListener('DOMContentLoaded', initFontAwesomeIconPickers);

// 導出供外部使用
window.FontAwesomeIconPicker = FontAwesomeIconPicker;
window.initFontAwesomeIconPickers = initFontAwesomeIconPickers;
