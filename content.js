// ── Helpers ────────────────────────────────────────────────────────────────
const isKimiClaw = () => location.pathname === '/bot' || location.pathname.startsWith('/bot');

// ── Storage ────────────────────────────────────────────────────────────────
let folders  = {};   // regular chat folders
let bookmarks = [];  // Kimi Claw topic bookmarks [{id, label, scrollY, scrollPct, created}]

function saveState() {
    chrome.storage.local.set({ kimiFolders: folders, kimiBookmarks: bookmarks });
}

function loadState(cb) {
    chrome.storage.local.get(['kimiFolders', 'kimiBookmarks'], (result) => {
        folders   = result.kimiFolders   || {};
        bookmarks = result.kimiBookmarks || [];
        cb();
    });
}

// ══════════════════════════════════════════════════════════════════════════
//  KIMI CLAW  –  Topic Bookmark Navigator
// ══════════════════════════════════════════════════════════════════════════
function initKimiClaw() {
    if (document.getElementById('kimi-topic-nav')) return;

    // ── Floating navigator panel ──────────────────────────────────────────
    const nav = document.createElement('div');
    nav.id = 'kimi-topic-nav';
    nav.innerHTML = `
        <div id="ktn-header">
            <span>📌 Topics</span>
            <div style="display:flex;gap:4px;">
                <button id="ktn-add" title="Bookmark current position">+ Add</button>
                <button id="ktn-toggle" title="Collapse">−</button>
            </div>
        </div>
        <div id="ktn-body">
            <div id="ktn-list"></div>
            <div id="ktn-empty">Scroll to a point in the conversation, then click <strong>+ Add</strong> to bookmark it as a topic.</div>
        </div>
    `;
    document.body.appendChild(nav);

    renderBookmarks();

    document.getElementById('ktn-add').addEventListener('click', () => {
        const label = prompt('Topic name for this position:');
        if (!label) return;
        const scrollEl  = getScrollContainer();
        const scrollY   = scrollEl ? scrollEl.scrollTop : window.scrollY;
        const maxScroll = scrollEl
            ? scrollEl.scrollHeight - scrollEl.clientHeight
            : document.documentElement.scrollHeight - window.innerHeight;
        const scrollPct = maxScroll > 0 ? Math.round((scrollY / maxScroll) * 100) : 0;

        bookmarks.push({ id: 'bm_' + Date.now(), label, scrollY, scrollPct, created: Date.now() });
        bookmarks.sort((a, b) => a.scrollPct - b.scrollPct);
        saveState();
        renderBookmarks();
    });

    let collapsed = false;
    document.getElementById('ktn-toggle').addEventListener('click', () => {
        collapsed = !collapsed;
        document.getElementById('ktn-body').style.display = collapsed ? 'none' : 'block';
        document.getElementById('ktn-toggle').textContent = collapsed ? '+' : '−';
    });

    // Make panel draggable
    makeDraggable(nav, document.getElementById('ktn-header'));
}

function getScrollContainer() {
    // Walk ALL elements and find the one actually scrolling
    const all = Array.from(document.querySelectorAll('*'));
    // Prefer deeper/larger scroll containers
    const scrollables = all.filter(el => {
        const style = window.getComputedStyle(el);
        const oy = style.overflowY;
        return (oy === 'auto' || oy === 'scroll') && el.scrollHeight > el.clientHeight + 50;
    });
    // Return the one with the most scrollable height (the main conversation container)
    if (scrollables.length > 0) {
        return scrollables.reduce((a, b) => a.scrollHeight > b.scrollHeight ? a : b);
    }
    // Fallback: check html/body
    if (document.documentElement.scrollHeight > document.documentElement.clientHeight) {
        return document.documentElement;
    }
    return null;
}

function renderBookmarks() {
    const list  = document.getElementById('ktn-list');
    const empty = document.getElementById('ktn-empty');
    if (!list) return;

    if (bookmarks.length === 0) {
        list.innerHTML  = '';
        empty.style.display = 'block';
        return;
    }
    empty.style.display = 'none';
    list.innerHTML = bookmarks.map(bm => `
        <div class="ktn-item" data-id="${bm.id}">
            <span class="ktn-pct">${bm.scrollPct}%</span>
            <span class="ktn-label" data-id="${bm.id}" title="Jump to: ${bm.label}">${bm.label}</span>
            <button class="ktn-del" data-id="${bm.id}" title="Remove">✕</button>
        </div>
    `).join('');

    list.querySelectorAll('.ktn-label').forEach(el => {
        el.addEventListener('click', () => {
            const bm = bookmarks.find(b => b.id === el.dataset.id);
            if (!bm) return;
            const scrollEl  = getScrollContainer();
            // Use percentage to calculate target (more reliable as content grows)
            const maxScroll = scrollEl
                ? scrollEl.scrollHeight - scrollEl.clientHeight
                : document.documentElement.scrollHeight - window.innerHeight;
            const targetY = Math.round((bm.scrollPct / 100) * maxScroll);
            if (scrollEl) {
                scrollEl.scrollTo({ top: targetY, behavior: 'smooth' });
            }
            // Always also try window scroll as fallback
            window.scrollTo({ top: targetY, behavior: 'smooth' });
            document.documentElement.scrollTo({ top: targetY, behavior: 'smooth' });
        });
    });

    list.querySelectorAll('.ktn-del').forEach(btn => {
        btn.addEventListener('click', () => {
            bookmarks = bookmarks.filter(b => b.id !== btn.dataset.id);
            saveState();
            renderBookmarks();
        });
    });
}

function makeDraggable(panel, handle) {
    let ox = 0, oy = 0, dragging = false;
    handle.style.cursor = 'grab';
    handle.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        dragging = true;
        ox = e.clientX - panel.getBoundingClientRect().left;
        oy = e.clientY - panel.getBoundingClientRect().top;
        handle.style.cursor = 'grabbing';
    });
    document.addEventListener('mousemove', (e) => {
        if (!dragging) return;
        panel.style.right  = 'auto';
        panel.style.left   = (e.clientX - ox) + 'px';
        panel.style.top    = (e.clientY - oy) + 'px';
        panel.style.bottom = 'auto';
    });
    document.addEventListener('mouseup', () => {
        dragging = false;
        handle.style.cursor = 'grab';
    });
}

// ══════════════════════════════════════════════════════════════════════════
//  REGULAR CHATS  –  Folder UI
// ══════════════════════════════════════════════════════════════════════════
function injectFolderUI() {
    const sidebar = document.querySelector('aside.sidebar') || document.querySelector('aside') || document.querySelector('.sidebar-nav');
    if (!sidebar || document.getElementById('kimi-folder-root')) return;

    const root = document.createElement('div');
    root.id = 'kimi-folder-root';
    sidebar.prepend(root);
    renderFolders();
}

function renderFolders() {
    const root = document.getElementById('kimi-folder-root');
    if (!root) return;

    root.innerHTML = `
        <div class="folder-header">
            <span>My Folders</span>
            <button id="add-folder-btn">+</button>
        </div>
        <div id="folder-list"></div>
    `;

    document.getElementById('add-folder-btn').addEventListener('click', () => {
        const name = prompt('Folder name:');
        if (!name) return;
        const id = 'f_' + Date.now();
        folders[id] = { name, chats: [] };
        saveState();
        renderFolders();
    });

    const list = document.getElementById('folder-list');
    Object.entries(folders).forEach(([id, folder]) => {
        const folderEl = document.createElement('div');
        folderEl.className = 'kimi-folder';
        folderEl.innerHTML = `
            <div class="kimi-folder-title" data-id="${id}">
                <span class="kimi-folder-arrow">▶</span>
                <span>📁 ${folder.name}</span>
                <button class="kimi-folder-delete" data-id="${id}" title="Delete folder">✕</button>
            </div>
            <div class="kimi-folder-chats" id="chats-${id}" style="display:none;">
                ${folder.chats.length === 0
                    ? '<div class="kimi-empty-hint">No chats yet — click 📁 on a chat to add it</div>'
                    : folder.chats.map(c => `
                        <div class="kimi-chat-entry">
                            <a href="${c.href}" title="${c.title}">${c.title.substring(0, 28)}${c.title.length > 28 ? '…' : ''}</a>
                            <button class="kimi-remove-chat" data-folder="${id}" data-chat="${c.id}" title="Remove">✕</button>
                        </div>`).join('')
                }
            </div>
        `;
        list.appendChild(folderEl);

        folderEl.querySelector('.kimi-folder-title').addEventListener('click', (e) => {
            if (e.target.classList.contains('kimi-folder-delete')) return;
            const chatsEl = document.getElementById(`chats-${id}`);
            const arrow   = folderEl.querySelector('.kimi-folder-arrow');
            const isOpen  = chatsEl.style.display !== 'none';
            chatsEl.style.display = isOpen ? 'none' : 'block';
            arrow.textContent     = isOpen ? '▶' : '▼';
        });

        folderEl.querySelector('.kimi-folder-delete').addEventListener('click', () => {
            if (!confirm(`Delete folder "${folder.name}"?`)) return;
            delete folders[id];
            saveState();
            renderFolders();
            attachChatButtons();
        });

        folderEl.querySelectorAll('.kimi-remove-chat').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                folders[btn.dataset.folder].chats = folders[btn.dataset.folder].chats.filter(c => c.id !== btn.dataset.chat);
                saveState();
                renderFolders();
                attachChatButtons();
            });
        });
    });
}

function attachChatButtons() {
    const sidebar = document.querySelector('aside.sidebar') || document.querySelector('aside');
    if (!sidebar) return;
    sidebar.querySelectorAll('a[href*="/chat/"]').forEach(link => {
        if (link.querySelector('.kimi-add-to-folder')) return;
        link.style.position = 'relative';
        const btn = document.createElement('button');
        btn.className   = 'kimi-add-to-folder';
        btn.title       = 'Add to folder';
        btn.textContent = '📁';
        btn.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); showFolderPicker(btn, link); });
        link.appendChild(btn);
    });
}

function showFolderPicker(btn, link) {
    document.querySelectorAll('.kimi-folder-picker').forEach(el => el.remove());
    if (Object.keys(folders).length === 0) { alert('Create a folder first using the "+" button.'); return; }

    const chatHref  = link.getAttribute('href');
    const chatId    = chatHref.split('/chat/')[1]?.split('?')[0] || chatHref;
    const chatTitle = link.innerText.trim() || 'Untitled';

    const picker = document.createElement('div');
    picker.className = 'kimi-folder-picker';
    picker.innerHTML = Object.entries(folders).map(([id, f]) =>
        `<div class="kimi-picker-item" data-id="${id}">📁 ${f.name}</div>`
    ).join('');
    document.body.appendChild(picker);

    const rect = btn.getBoundingClientRect();
    picker.style.top  = (rect.bottom + window.scrollY + 4) + 'px';
    picker.style.left = (rect.left + window.scrollX) + 'px';

    picker.querySelectorAll('.kimi-picker-item').forEach(item => {
        item.addEventListener('click', () => {
            const fid = item.dataset.id;
            if (!folders[fid].chats.some(c => c.id === chatId)) {
                folders[fid].chats.push({ id: chatId, title: chatTitle, href: chatHref });
                saveState();
                renderFolders();
            }
            picker.remove();
        });
    });
    setTimeout(() => document.addEventListener('click', () => picker.remove(), { once: true }), 0);
}

// ── Wide Mode & Export ─────────────────────────────────────────────────────
function toggleWideMode() {
    const main = document.querySelector('main');
    if (main) main.style.maxWidth = main.style.maxWidth === '100%' ? '800px' : '100%';
}

function exportChats() {
    const items = document.querySelectorAll('aside a[href*="/chat/"]');
    const titles = Array.from(items).map(el => el.innerText.trim()).filter(Boolean);
    if (titles.length === 0) { alert('No chats found to export.'); return; }
    const blob = new Blob([titles.join('\n')], { type: 'text/plain' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = 'kimi-chats.txt'; a.click();
    URL.revokeObjectURL(url);
}

chrome.runtime.onMessage.addListener((request) => {
    if (request.action === 'toggleWide')  toggleWideMode();
    if (request.action === 'exportChats') exportChats();
});

// ── Init ───────────────────────────────────────────────────────────────────
loadState(() => {
    if (isKimiClaw()) {
        initKimiClaw();
    } else {
        injectFolderUI();
        attachChatButtons();
    }
});

const observer = new MutationObserver(() => {
    if (isKimiClaw()) {
        initKimiClaw();
    } else {
        injectFolderUI();
        attachChatButtons();
    }
});
observer.observe(document.body, { childList: true, subtree: true });
