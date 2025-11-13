// Font Awesome Icon Picker - 完整版本
const FONTAWESOME_ICONS = {
  'brands': [
    'facebook', 'facebook-f', 'facebook-square', 'twitter', 'twitter-square', 'instagram', 'instagram-square',
    'linkedin', 'linkedin-in', 'youtube', 'youtube-square', 'github', 'github-square', 'gitlab', 'discord',
    'twitch', 'reddit', 'reddit-square', 'pinterest', 'pinterest-p', 'pinterest-square', 'snapchat',
    'snapchat-square', 'tiktok', 'telegram', 'telegram-plane', 'whatsapp', 'whatsapp-square', 'skype',
    'vimeo', 'vimeo-square', 'dribbble', 'dribbble-square', 'behance', 'behance-square', 'codepen',
    'stack-overflow', 'bitbucket', 'github-alt', 'google', 'google-plus', 'google-plus-g', 'google-plus-square',
    'apple', 'android', 'windows', 'linux', 'ubuntu', 'centos', 'redhat', 'html5', 'css3', 'js-square',
    'node-js', 'npm', 'yarn', 'react', 'angular', 'vuejs', 'php', 'python', 'java', 'dotnet', 'swift',
    'wordpress', 'joomla', 'drupal', 'chrome', 'firefox', 'safari', 'edge', 'opera', 'internet-explorer',
    'steam', 'steam-square', 'playstation', 'xbox', 'nintendo-switch', 'amazon', 'ebay', 'paypal',
    'stripe', 'cc-visa', 'cc-mastercard', 'cc-amex', 'cc-paypal', 'cc-stripe', 'cc-discover', 'btc', 'ethereum'
  ],
  'solid': [
    'ad', 'address-book', 'address-card', 'adjust', 'air-freshener', 'align-center', 'align-justify',
    'align-left', 'align-right', 'allergies', 'ambulance', 'american-sign-language-interpreting',
    'anchor', 'angle-double-down', 'angle-double-left', 'angle-double-right', 'angle-double-up',
    'angle-down', 'angle-left', 'angle-right', 'angle-up', 'angry', 'ankh', 'apple-alt', 'archive',
    'archway', 'arrow-alt-circle-down', 'arrow-alt-circle-left', 'arrow-alt-circle-right',
    'arrow-alt-circle-up', 'arrow-circle-down', 'arrow-circle-left', 'arrow-circle-right',
    'arrow-circle-up', 'arrow-down', 'arrow-left', 'arrow-right', 'arrow-up', 'arrows-alt',
    'arrows-alt-h', 'arrows-alt-v', 'assistive-listening-systems', 'asterisk', 'at', 'atlas',
    'atom', 'audio-description', 'award', 'baby', 'baby-carriage', 'backspace', 'backward',
    'bacon', 'bacteria', 'bacterium', 'bahai', 'balance-scale', 'balance-scale-left',
    'balance-scale-right', 'ban', 'band-aid', 'barcode', 'bars', 'baseball-ball', 'basketball-ball',
    'bath', 'battery-empty', 'battery-full', 'battery-half', 'battery-quarter', 'battery-three-quarters',
    'bed', 'beer', 'bell', 'bell-slash', 'bezier-curve', 'bible', 'bicycle', 'biking', 'binoculars',
    'biohazard', 'birthday-cake', 'blender', 'blender-phone', 'blind', 'blog', 'bold', 'bolt',
    'bomb', 'bone', 'bong', 'book', 'book-dead', 'book-medical', 'book-open', 'book-reader',
    'bookmark', 'border-all', 'border-none', 'border-style', 'bowling-ball', 'box', 'box-open',
    'box-tissue', 'boxes', 'braille', 'brain', 'bread-slice', 'briefcase', 'briefcase-medical',
    'broadcast-tower', 'broom', 'brush', 'bug', 'building', 'bullhorn', 'bullseye', 'burn',
    'bus', 'bus-alt', 'business-time', 'calculator', 'calendar', 'calendar-alt', 'calendar-check',
    'calendar-day', 'calendar-minus', 'calendar-plus', 'calendar-times', 'calendar-week',
    'camera', 'camera-retro', 'campground', 'candy-cane', 'cannabis', 'capsules', 'car',
    'car-alt', 'car-battery', 'car-crash', 'car-side', 'caravan', 'caret-down', 'caret-left',
    'caret-right', 'caret-square-down', 'caret-square-left', 'caret-square-right', 'caret-square-up',
    'caret-up', 'carrot', 'cart-arrow-down', 'cart-plus', 'cash-register', 'cat', 'certificate',
    'chair', 'chalkboard', 'chalkboard-teacher', 'charging-station', 'chart-area', 'chart-bar',
    'chart-line', 'chart-pie', 'check', 'check-circle', 'check-double', 'check-square',
    'cheese', 'chess', 'chess-bishop', 'chess-board', 'chess-king', 'chess-knight', 'chess-pawn',
    'chess-queen', 'chess-rook', 'chevron-circle-down', 'chevron-circle-left', 'chevron-circle-right',
    'chevron-circle-up', 'chevron-down', 'chevron-left', 'chevron-right', 'chevron-up', 'child',
    'church', 'circle', 'circle-notch', 'city', 'clinic-medical', 'clipboard', 'clipboard-check',
    'clipboard-list', 'clock', 'clone', 'closed-captioning', 'cloud', 'cloud-download-alt',
    'cloud-meatball', 'cloud-moon', 'cloud-moon-rain', 'cloud-rain', 'cloud-showers-heavy',
    'cloud-sun', 'cloud-sun-rain', 'cloud-upload-alt', 'cocktail', 'code', 'code-branch',
    'coffee', 'cog', 'cogs', 'coins', 'columns', 'comment', 'comment-alt', 'comment-dollar',
    'comment-dots', 'comment-medical', 'comment-slash', 'comments', 'comments-dollar',
    'compact-disc', 'compass', 'compress', 'compress-alt', 'compress-arrows-alt', 'concierge-bell',
    'cookie', 'cookie-bite', 'copy', 'copyright', 'couch', 'credit-card', 'crop', 'crop-alt',
    'cross', 'crosshairs', 'crow', 'crown', 'crutch', 'cube', 'cubes', 'cut', 'database',
    'deaf', 'democrat', 'desktop', 'dharmachakra', 'diagnoses', 'dice', 'dice-d6', 'dice-five',
    'dice-four', 'dice-one', 'dice-six', 'dice-three', 'dice-two', 'digital-tachograph',
    'directions', 'disease', 'divide', 'dizzy', 'dna', 'dog', 'dollar-sign', 'dolly', 'dolly-flatbed',
    'donate', 'door-closed', 'door-open', 'dot-circle', 'dove', 'download', 'drafting-compass',
    'dragon', 'draw-polygon', 'drum', 'drum-steelpan', 'drumstick-bite', 'dumbbell', 'dumpster',
    'dumpster-fire', 'dungeon', 'edit', 'egg', 'eject', 'ellipsis-h', 'ellipsis-v', 'envelope',
    'envelope-open', 'envelope-open-text', 'envelope-square', 'equals', 'eraser', 'ethernet',
    'euro-sign', 'exchange-alt', 'exclamation', 'exclamation-circle', 'exclamation-triangle',
    'expand', 'expand-alt', 'expand-arrows-alt', 'external-link-alt', 'external-link-square-alt',
    'eye', 'eye-dropper', 'eye-slash', 'fan', 'fast-backward', 'fast-forward', 'faucet', 'fax',
    'feather', 'female', 'fighter-jet', 'file', 'file-alt', 'file-archive', 'file-audio',
    'file-code', 'file-contract', 'file-csv', 'file-download', 'file-excel', 'file-export',
    'file-image', 'file-import', 'file-invoice', 'file-invoice-dollar', 'file-medical',
    'file-medical-alt', 'file-pdf', 'file-powerpoint', 'file-prescription', 'file-signature',
    'file-upload', 'file-video', 'file-word', 'fill', 'fill-drip', 'film', 'filter', 'fingerprint',
    'fire', 'fire-alt', 'fire-extinguisher', 'first-aid', 'fish', 'fist-raised', 'flag',
    'flag-checkered', 'flag-usa', 'flask', 'flushed', 'folder', 'folder-minus', 'folder-open',
    'folder-plus', 'font', 'football-ball', 'forward', 'frog', 'frown', 'frown-open', 'funnel-dollar',
    'futbol', 'gamepad', 'gas-pump', 'gavel', 'gem', 'genderless', 'ghost', 'gift', 'gifts',
    'glass-cheers', 'glass-martini', 'glass-martini-alt', 'glass-whiskey', 'glasses', 'globe',
    'globe-africa', 'globe-americas', 'globe-asia', 'globe-europe', 'golf-ball', 'gopuram',
    'graduation-cap', 'greater-than', 'greater-than-equal', 'grimace', 'grin', 'grin-alt',
    'grin-beam', 'grin-beam-sweat', 'grin-hearts', 'grin-squint', 'grin-squint-tears',
    'grin-stars', 'grin-tears', 'grin-tongue', 'grin-tongue-squint', 'grin-tongue-wink',
    'grin-wink', 'grip-horizontal', 'grip-lines', 'grip-lines-vertical', 'grip-vertical',
    'guitar', 'h-square', 'hamburger', 'hammer', 'hamsa', 'hand-holding', 'hand-holding-heart',
    'hand-holding-medical', 'hand-holding-usd', 'hand-holding-water', 'hand-lizard', 'hand-middle-finger',
    'hand-paper', 'hand-peace', 'hand-point-down', 'hand-point-left', 'hand-point-right',
    'hand-point-up', 'hand-pointer', 'hand-rock', 'hand-scissors', 'hand-spock', 'hands',
    'hands-helping', 'hands-wash', 'handshake', 'handshake-alt-slash', 'handshake-slash',
    'hanukiah', 'hard-hat', 'hashtag', 'hat-cowboy', 'hat-cowboy-side', 'hat-wizard', 'hdd',
    'head-side-cough', 'head-side-cough-slash', 'head-side-mask', 'head-side-virus', 'heading',
    'headphones', 'headphones-alt', 'headset', 'heart', 'heart-broken', 'heartbeat', 'helicopter',
    'highlighter', 'hiking', 'hippo', 'history', 'hockey-puck', 'holly-berry', 'home', 'horse',
    'horse-head', 'hospital', 'hospital-alt', 'hospital-symbol', 'hospital-user', 'hot-tub',
    'hotdog', 'hotel', 'hourglass', 'hourglass-end', 'hourglass-half', 'hourglass-start',
    'house-damage', 'house-user', 'hryvnia', 'i-cursor', 'ice-cream', 'icicles', 'icons',
    'id-badge', 'id-card', 'id-card-alt', 'igloo', 'image', 'images', 'inbox', 'indent',
    'industry', 'infinity', 'info', 'info-circle', 'italic', 'jedi', 'joint', 'journal-whills',
    'kaaba', 'key', 'keyboard', 'khanda', 'kiss', 'kiss-beam', 'kiss-wink-heart', 'kiwi-bird',
    'landmark', 'language', 'laptop', 'laptop-code', 'laptop-house', 'laptop-medical', 'laugh',
    'laugh-beam', 'laugh-squint', 'laugh-wink', 'layer-group', 'leaf', 'lemon', 'less-than',
    'less-than-equal', 'level-down-alt', 'level-up-alt', 'life-ring', 'lightbulb', 'link',
    'lira-sign', 'list', 'list-alt', 'list-ol', 'list-ul', 'location-arrow', 'lock', 'lock-open',
    'long-arrow-alt-down', 'long-arrow-alt-left', 'long-arrow-alt-right', 'long-arrow-alt-up',
    'low-vision', 'luggage-cart', 'lungs', 'lungs-virus', 'magic', 'magnet', 'mail-bulk',
    'male', 'map', 'map-marked', 'map-marked-alt', 'map-marker', 'map-marker-alt', 'map-pin',
    'map-signs', 'marker', 'mars', 'mars-double', 'mars-stroke', 'mars-stroke-h', 'mars-stroke-v',
    'mask', 'medal', 'medkit', 'meh', 'meh-blank', 'meh-rolling-eyes', 'memory', 'menorah',
    'mercury', 'meteor', 'microchip', 'microphone', 'microphone-alt', 'microphone-alt-slash',
    'microphone-slash', 'microscope', 'minus', 'minus-circle', 'minus-square', 'mitten',
    'mobile', 'mobile-alt', 'money-bill', 'money-bill-alt', 'money-bill-wave', 'money-bill-wave-alt',
    'money-check', 'money-check-alt', 'monument', 'moon', 'mortar-pestle', 'mosque', 'motorcycle',
    'mountain', 'mouse', 'mouse-pointer', 'mug-hot', 'music', 'network-wired', 'neuter',
    'newspaper', 'not-equal', 'notes-medical', 'object-group', 'object-ungroup', 'oil-can',
    'om', 'otter', 'outdent', 'pager', 'paint-brush', 'paint-roller', 'palette', 'pallet',
    'paper-plane', 'paperclip', 'parachute-box', 'paragraph', 'parking', 'passport', 'pastafarianism',
    'paste', 'pause', 'pause-circle', 'paw', 'peace', 'pen', 'pen-alt', 'pen-fancy', 'pen-nib',
    'pen-square', 'pencil-alt', 'pencil-ruler', 'people-arrows', 'people-carry', 'pepper-hot',
    'percent', 'percentage', 'person-booth', 'phone', 'phone-alt', 'phone-slash', 'phone-square',
    'phone-square-alt', 'phone-volume', 'photo-video', 'piggy-bank', 'pills', 'pizza-slice',
    'place-of-worship', 'plane', 'plane-arrival', 'plane-departure', 'plane-slash', 'play',
    'play-circle', 'plug', 'plus', 'plus-circle', 'plus-square', 'podcast', 'poll', 'poll-h',
    'poo', 'poo-storm', 'poop', 'portrait', 'pound-sign', 'power-off', 'pray', 'praying-hands',
    'prescription', 'prescription-bottle', 'prescription-bottle-alt', 'print', 'procedures',
    'project-diagram', 'pump-medical', 'pump-soap', 'puzzle-piece', 'qrcode', 'question',
    'question-circle', 'quidditch', 'quote-left', 'quote-right', 'quran', 'radiation', 'radiation-alt',
    'rainbow', 'random', 'receipt', 'record-vinyl', 'recycle', 'redo', 'redo-alt', 'registered',
    'remove-format', 'reply', 'reply-all', 'republican', 'restroom', 'retweet', 'ribbon',
    'ring', 'road', 'robot', 'rocket', 'route', 'rss', 'rss-square', 'ruble-sign', 'ruler',
    'ruler-combined', 'ruler-horizontal', 'ruler-vertical', 'running', 'rupee-sign', 'sad-cry',
    'sad-tear', 'satellite', 'satellite-dish', 'save', 'school', 'screwdriver', 'scroll',
    'sd-card', 'search', 'search-dollar', 'search-location', 'search-minus', 'search-plus',
    'seedling', 'server', 'shapes', 'share', 'share-alt', 'share-alt-square', 'share-square',
    'shekel-sign', 'shield-alt', 'shield-virus', 'ship', 'shipping-fast', 'shoe-prints',
    'shopping-bag', 'shopping-basket', 'shopping-cart', 'shower', 'shuttle-van', 'sign',
    'sign-in-alt', 'sign-language', 'sign-out-alt', 'signal', 'signature', 'sim-card', 'sink',
    'sitemap', 'skating', 'skiing', 'skiing-nordic', 'skull', 'skull-crossbones', 'slash',
    'sleigh', 'sliders-h', 'smile', 'smile-beam', 'smile-wink', 'smog', 'smoking', 'smoking-ban',
    'sms', 'snowboarding', 'snowflake', 'snowman', 'snowplow', 'soap', 'socks', 'solar-panel',
    'sort', 'sort-alpha-down', 'sort-alpha-down-alt', 'sort-alpha-up', 'sort-alpha-up-alt',
    'sort-amount-down', 'sort-amount-down-alt', 'sort-amount-up', 'sort-amount-up-alt',
    'sort-down', 'sort-numeric-down', 'sort-numeric-down-alt', 'sort-numeric-up',
    'sort-numeric-up-alt', 'sort-up', 'spa', 'space-shuttle', 'spell-check', 'spider',
    'spinner', 'splotch', 'spray-can', 'square', 'square-full', 'square-root-alt', 'stamp',
    'star', 'star-and-crescent', 'star-half', 'star-half-alt', 'star-of-david', 'star-of-life',
    'step-backward', 'step-forward', 'stethoscope', 'sticky-note', 'stop', 'stop-circle',
    'stopwatch', 'stopwatch-20', 'store', 'store-alt', 'store-alt-slash', 'store-slash',
    'stream', 'street-view', 'strikethrough', 'stroopwafel', 'subscript', 'subway', 'suitcase',
    'suitcase-rolling', 'sun', 'superscript', 'surprise', 'swatchbook', 'swimmer', 'swimming-pool',
    'synagogue', 'sync', 'sync-alt', 'syringe', 'table', 'table-tennis', 'tablet', 'tablet-alt',
    'tablets', 'tachometer-alt', 'tag', 'tags', 'tape', 'tasks', 'taxi', 'teeth', 'teeth-open',
    'temperature-high', 'temperature-low', 'tenge', 'terminal', 'text-height', 'text-width',
    'th', 'th-large', 'th-list', 'theater-masks', 'thermometer', 'thermometer-empty',
    'thermometer-full', 'thermometer-half', 'thermometer-quarter', 'thermometer-three-quarters',
    'thumbs-down', 'thumbs-up', 'thumbtack', 'ticket-alt', 'times', 'times-circle', 'tint',
    'tint-slash', 'tired', 'toggle-off', 'toggle-on', 'toilet', 'toilet-paper', 'toilet-paper-slash',
    'toolbox', 'tools', 'tooth', 'torah', 'torii-gate', 'tractor', 'trademark', 'traffic-light',
    'trailer', 'train', 'tram', 'transgender', 'transgender-alt', 'trash', 'trash-alt',
    'trash-restore', 'trash-restore-alt', 'tree', 'trophy', 'truck', 'truck-loading', 'truck-monster',
    'truck-moving', 'truck-pickup', 'tshirt', 'tty', 'tv', 'umbrella', 'umbrella-beach',
    'underline', 'undo', 'undo-alt', 'universal-access', 'university', 'unlink', 'unlock',
    'unlock-alt', 'upload', 'user', 'user-alt', 'user-alt-slash', 'user-astronaut', 'user-check',
    'user-circle', 'user-clock', 'user-cog', 'user-edit', 'user-friends', 'user-graduate',
    'user-injured', 'user-lock', 'user-md', 'user-minus', 'user-ninja', 'user-nurse',
    'user-plus', 'user-secret', 'user-shield', 'user-slash', 'user-tag', 'user-tie', 'user-times',
    'users', 'users-cog', 'users-slash', 'utensil-spoon', 'utensils', 'vector-square', 'venus',
    'venus-double', 'venus-mars', 'vest', 'vest-patches', 'vial', 'vials', 'video', 'video-slash',
    'vihara', 'virus', 'virus-slash', 'viruses', 'voicemail', 'volleyball-ball', 'volume-down',
    'volume-mute', 'volume-off', 'volume-up', 'vote-yea', 'vr-cardboard', 'walking', 'wallet',
    'warehouse', 'water', 'wave-square', 'weight', 'weight-hanging', 'wheelchair', 'wifi',
    'wind', 'window-close', 'window-maximize', 'window-minimize', 'window-restore', 'wine-bottle',
    'wine-glass', 'wine-glass-alt', 'won-sign', 'wrench', 'x-ray', 'yen-sign', 'yin-yang'
  ],
  'regular': [
    'address-book', 'address-card', 'angry', 'arrow-alt-circle-down', 'arrow-alt-circle-left',
    'arrow-alt-circle-right', 'arrow-alt-circle-up', 'bell', 'bell-slash', 'bookmark', 'building',
    'calendar', 'calendar-alt', 'calendar-check', 'calendar-minus', 'calendar-plus', 'calendar-times',
    'caret-square-down', 'caret-square-left', 'caret-square-right', 'caret-square-up', 'chart-bar',
    'check-circle', 'check-square', 'circle', 'clipboard', 'clock', 'clone', 'closed-captioning',
    'comment', 'comment-alt', 'comment-dots', 'comments', 'compass', 'copy', 'copyright', 'credit-card',
    'dot-circle', 'edit', 'envelope', 'envelope-open', 'eye', 'eye-slash', 'file', 'file-alt',
    'file-archive', 'file-audio', 'file-code', 'file-excel', 'file-image', 'file-pdf', 'file-powerpoint',
    'file-video', 'file-word', 'flag', 'folder', 'folder-open', 'frown', 'frown-open', 'futbol',
    'gem', 'grin', 'grin-alt', 'grin-beam', 'grin-beam-sweat', 'grin-hearts', 'grin-squint',
    'grin-squint-tears', 'grin-stars', 'grin-tears', 'grin-tongue', 'grin-tongue-squint',
    'grin-tongue-wink', 'grin-wink', 'hand-lizard', 'hand-paper', 'hand-peace', 'hand-point-down',
    'hand-point-left', 'hand-point-right', 'hand-point-up', 'hand-pointer', 'hand-rock', 'hand-scissors',
    'hand-spock', 'handshake', 'hdd', 'heart', 'hospital', 'hourglass', 'id-badge', 'id-card',
    'id-card-alt', 'image', 'images', 'keyboard', 'kiss', 'kiss-beam', 'kiss-wink-heart', 'laugh',
    'laugh-beam', 'laugh-squint', 'laugh-wink', 'lemon', 'life-ring', 'lightbulb', 'list-alt',
    'map', 'meh', 'meh-blank', 'meh-rolling-eyes', 'minus-square', 'money-bill-alt', 'moon',
    'newspaper', 'object-group', 'object-ungroup', 'paper-plane', 'pause-circle', 'play-circle',
    'plus-square', 'question-circle', 'registered', 'sad-cry', 'sad-tear', 'save', 'share-square',
    'smile', 'smile-beam', 'smile-wink', 'snowflake', 'square', 'star', 'star-half', 'sticky-note',
    'stop-circle', 'sun', 'surprise', 'thumbs-down', 'thumbs-up', 'times-circle', 'tired',
    'trash-alt', 'user', 'user-circle', 'window-close', 'window-maximize', 'window-minimize',
    'window-restore'
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
      // 聚焦到輸入框並選中內容，方便用戶編輯
      setTimeout(() => {
        this.input.focus();
        this.input.select();
      }, 100);
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
    
    // 限制顯示數量，避免性能問題
    icons.slice(0, 200).forEach(icon => {
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
    // 不再設置為 readOnly，讓用戶可以自由編輯
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
