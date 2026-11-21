(() => {
    const icons = {
        "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        "arrow-right-circle": '<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="m12 8 4 4-4 4"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>',
        "book-fill": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>',
        "camera-video-fill": '<path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
        "camera-video-off-fill": '<path d="m2 2 20 20"/><path d="M10.7 6H14a2 2 0 0 1 2 2v1"/><path d="m16 13 6 4V7l-4 2.7"/><path d="M6.1 6.1A2 2 0 0 0 4 8v8a2 2 0 0 0 2 2h10"/>',
        "chat-dots-fill": '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z"/><path d="M8 12h.01M12 12h.01M16 12h.01"/>',
        "check-circle-fill": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
        "chevron-right": '<path d="m9 18 6-6-6-6"/>',
        "clipboard": '<rect x="8" y="4" width="12" height="16" rx="2"/><path d="M16 4.5V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v1.5"/><path d="M4 7v14a1 1 0 0 0 1 1h11"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "cloud": '<path d="M20 16.2A4.5 4.5 0 0 0 18 7.5h-1.3A7 7 0 1 0 5 17h13"/>',
        "code-slash": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6m6-16-4 20"/>',
        "collection": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
        "controller": '<path d="M6 12h4m-2-2v4"/><path d="M15 13h.01M18 11h.01"/><path d="M7 6h10a4 4 0 0 1 3.9 3.1l1 5A3 3 0 0 1 17 17l-2-2H9l-2 2a3 3 0 0 1-4.9-2.9l1-5A4 4 0 0 1 7 6Z"/>',
        "cpu": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v4m6-4v4M9 19v4m6-4v4M1 9h4m-4 6h4m14-6h4m-4 6h4"/>',
        "cpu-fill": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v4m6-4v4M9 19v4m6-4v4M1 9h4m-4 6h4m14-6h4m-4 6h4"/>',
        "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
        "display": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>',
        "emoji-smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
        "folder2-open": '<path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v1H8a2 2 0 0 0-1.8 1.1L3 18V7Z"/><path d="M8 10h13l-2.5 8H5l3-6.8A2 2 0 0 1 8 10Z"/>',
        "globe2": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/>',
        "hash": '<path d="M4 9h16M4 15h16M10 3 8 21m8-18-2 18"/>',
        "hourglass-split": '<path d="M5 22h14M5 2h14M17 22v-4.2a2 2 0 0 0-.6-1.4L12 12l4.4-4.4a2 2 0 0 0 .6-1.4V2M7 2v4.2a2 2 0 0 0 .6 1.4L12 12"/>',
        "journal-bookmark-fill": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/><path d="M14 2v7l-2-1.5L10 9V2"/>',
        "layout-sidebar": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18"/>',
        "lightning-fill": '<path d="m13 2-3 8h7L9 22l2-9H5l8-11Z"/>',
        "map-fill": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15m6-12v15"/>',
        "megaphone-fill": '<path d="m3 11 18-5v12L3 13v-2Z"/><path d="M11.6 16.8a3 3 0 0 1-5.7-1.6m-2.5-2.4v-3a2 2 0 0 1 2-2H6"/>',
        "mic-fill": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v2a7 7 0 0 0 14 0v-2m-7 9v3m-4 0h8"/>',
        "mic-mute-fill": '<path d="m2 2 20 20"/><path d="M9 9v3a3 3 0 0 0 5.1 2.1M15 9V5a3 3 0 0 0-5.8-1M5 10v2a7 7 0 0 0 11.8 5M19 10v2m-7 7v3m-4 0h8"/>',
        "mortarboard-fill": '<path d="m22 10-10-5L2 10l10 5 10-5Z"/><path d="M6 12v5c3.3 2.7 8.7 2.7 12 0v-5m4-2v6"/>',
        "paperclip": '<path d="m21.4 11.6-8.5 8.5a5 5 0 0 1-7.1-7.1l8.5-8.5a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-2.8-2.8l8.5-8.5"/>',
        "patch-question-fill": '<path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/>',
        "people-fill": '<path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2m6-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm10 10v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
        "person-circle": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="9" r="3"/><path d="M6.2 19a6 6 0 0 1 11.6 0"/>',
        "person-fill": '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/>',
        "person-hearts": '<path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2m6-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"/><path d="M19 8.5c-1.1-1-3-.2-3 1.2 0 1.2 1.6 2.2 3 3.3 1.4-1.1 3-2.1 3-3.3 0-1.4-1.9-2.2-3-1.2Z"/>',
        "person-lines-fill": '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0m3-12h4m-4 4h4m-4 4h4"/>',
        "person-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2m6-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm11-3v6m3-3h-6"/>',
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 11.2 19a19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7l.5 2.8a2 2 0 0 1-.6 1.8L7.7 9.6a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 1.8-.6l2.8.5a2 2 0 0 1 1.7 2Z"/>',
        "play-circle-fill": '<circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4V8Z"/>',
        "play-fill": '<path d="m7 4 13 8-13 8V4Z"/>',
        "robot": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M12 8V4H8m8 9h.01M8 13h.01M9 17h6"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "send-fill": '<path d="m22 2-7 20-4-9-9-4 20-7ZM22 2 11 13"/>',
        "shield-lock": '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z"/><rect x="9" y="10" width="6" height="5" rx="1"/><path d="M10 10V8a2 2 0 0 1 4 0v2"/>',
        "sticky-fill": '<path d="M16 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10l6-6V5a2 2 0 0 0-2-2h-3Z"/><path d="M15 21v-6h6"/>',
        "stop-circle-fill": '<circle cx="12" cy="12" r="10"/><rect x="9" y="9" width="6" height="6" rx="1"/>',
        "sun-fill": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>',
        "telephone-fill": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 11.2 19a19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7l.5 2.8a2 2 0 0 1-.6 1.8L7.7 9.6a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 1.8-.6l2.8.5a2 2 0 0 1 1.7 2Z"/>',
        "telephone-inbound-fill": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 11.2 19a19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7l.5 2.8a2 2 0 0 1-.6 1.8L7.7 9.6a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 1.8-.6l2.8.5a2 2 0 0 1 1.7 2Z"/><path d="M14 2v6m-3-3 3 3 3-3"/>',
        "telephone-x-fill": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 11.2 19a19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7l.5 2.8a2 2 0 0 1-.6 1.8L7.7 9.6a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 1.8-.6l2.8.5a2 2 0 0 1 1.7 2Z"/><path d="m14 4 6 6m0-6-6 6"/>',
        "terminal-fill": '<path d="m4 17 6-6-6-6m8 14h8"/>',
        "trash": '<path d="M3 6h18m-2 0-.9 14H5.9L5 6m4 0V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2m-5 4v6m4-6v6"/>',
        "trophy-fill": '<path d="M8 21h8m-4-4v4M7 4h10v5a5 5 0 0 1-10 0V4ZM7 7H4v2a4 4 0 0 0 4 4m9-6h3v2a4 4 0 0 1-4 4"/>',
        "x-lg": '<path d="m18 6-12 12M6 6l12 12"/>',
        "arrow-left": '<path d="M19 12H5m7 7-7-7 7-7"/>',
        "circle-help": '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3m.1 4h.01"/>',
        "keyboard": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 9h.01M10 9h.01M14 9h.01M18 9h.01M8 13h.01M12 13h.01M16 13h.01M7 16h10"/>',
        "bug": '<path d="m8 2 1.9 1.9M14 2l-1.9 1.9M9 7h6m-7 4h8m-8 4h8m-8 4h8"/><path d="M4 13H2m20 0h-2m-1-6 2-2M5 7 3 5m2 12-2 2m16-2 2 2M8 7a4 4 0 0 0-4 4v4a5 5 0 0 0 5 5h6a5 5 0 0 0 5-5v-4a4 4 0 0 0-4-4"/>',
        "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v6h6m-12 5h8m-8 4h8m-8-8h2"/>',
        "brain": '<path d="M12 18V5"/><path d="M15 13a4.2 4.2 0 0 0 3.5-6.5 4.5 4.5 0 0 0-7.5-1.6 4.5 4.5 0 0 0-7.5 1.6A4.2 4.2 0 0 0 7 13"/><path d="M15 13a4.2 4.2 0 0 1 3.5 6.5 4.5 4.5 0 0 1-7.5 1.6 4.5 4.5 0 0 1-7.5-1.6A4.2 4.2 0 0 1 7 13"/>',
        "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15m6-12v15"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2m6-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm10 10v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
        "books": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/><path d="M8 7h8m-8 4h8"/>',
        "settings": '<path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/><path d="m19.4 15 .1.1 1.4 1.1-1.4 2.4-1.7-.7a8 8 0 0 1-1.6.9l-.3 1.8h-2.8l-.3-1.8a8 8 0 0 1-1.6-.9l-1.7.7-1.4-2.4 1.4-1.1a7 7 0 0 1 0-1.9l-1.4-1.1 1.4-2.4 1.7.7a8 8 0 0 1 1.6-.9l.3-1.8h2.8l.3 1.8a8 8 0 0 1 1.6.9l1.7-.7 1.4 2.4-1.4 1.1a7 7 0 0 1 0 1.9Z"/>',
        "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "zap": '<path d="m13 2-3 8h7L9 22l2-9H5l8-11Z"/>',
        "bot": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M12 8V4H8m8 9h.01M8 13h.01M9 17h6"/>',
        "cat": '<path d="M12 5c-4.5 0-8 3.5-8 8a7 7 0 0 0 7 7h2a7 7 0 0 0 7-7c0-4.5-3.5-8-8-8Z"/><path d="m3 8 1-5 5 3m12 2-1-5-5 3m-6 8h.01M15 14h.01M9 17a4 4 0 0 0 6 0"/>',
        "blocks": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="5" rx="1"/><rect x="13" y="10" width="8" height="11" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/>',
        "wrench": '<path d="M14.7 6.3a5 5 0 0 0-6.4 6.4L3 18l3 3 5.3-5.3a5 5 0 0 0 6.4-6.4L14 12l-3-3 3.7-2.7Z"/>',
        "thermometer": '<path d="M14 14.8V5a3 3 0 0 0-6 0v9.8a5 5 0 1 0 6 0Z"/><path d="M11 11v6"/>',
        "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>',
        "flame": '<path d="M8.5 14.5A5.5 5.5 0 0 0 14 20a6 6 0 0 0 6-6c0-4-3-6-4-10-2 2-3 4-3 6-2-1-3-3-3-5-3 2-6 6-6 10a6 6 0 0 0 6 6"/>',
        "atom": '<circle cx="12" cy="12" r="1"/><path d="M20.2 20.2c2.4-2.4.8-8-3.6-12.4S6.6 1.8 4.2 4.2s-.8 8 3.6 12.4 10 6 12.4 3.6Z"/><path d="M15.8 15.8c4.4-4.4 6-10 3.6-12.4s-8-.8-12.4 3.6-6 10-3.6 12.4 8 .8 12.4-3.6Z"/>',
        "circle-alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>',
        "circle-x": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6m0-6 6 6"/>',
        "timer": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2m-2-13v2m5.6.4 1.4 1.4"/>',
        "pencil": '<path d="m16 5 3 3M4 20l4.5-1 11-11a2.1 2.1 0 0 0-3-3l-11 11L4 20Z"/>',
        "pencil-line": '<path d="m16 5 3 3M4 20l4.5-1 11-11a2.1 2.1 0 0 0-3-3l-11 11L4 20Zm2-1 3 3m-5-1h12"/>',
        "waveform": '<path d="M2 10v4m4-8v12m4-16v20m4-14v8m4-12v16m4-10v4"/>',
        "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>',
        "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20m-10-10a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/>',
        "alarm-clock": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M5 3 2 6m20 0-3-3M12 5V2m-4 19h8"/>',
        "briefcase-business": '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m-13 5h18m-10 0v2h2v-2"/>',
        "credit-card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20m-15 5h2"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
        "coffee": '<path d="M10 2v2m4-2v2M4 7h15v7a5 5 0 0 1-5 5h-3a7 7 0 0 1-7-7V7Zm15 2h2a2 2 0 0 1 0 4h-2m-13 9h15"/>',
        "sparkles": '<path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2L12 3Zm7 12 .9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9L19 15Z"/>',
        "sprout": '<path d="M7 20h10M12 20V10m0 4c-4.4 0-7-2.5-7-7 4.5 0 7 2.5 7 7Zm0-4c0-4.5 2.5-7 7-7 0 4.5-2.6 7-7 7Z"/>',
        "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.2-.1-3s-2.1-.8-2.9 0ZM12 15l-3-3a22 22 0 0 1 2-3.5C14.3 4 20 3 20 3s-1 5.7-5.5 9A22 22 0 0 1 12 15Z"/><path d="M9 12H5s.5-3 3-4m4 7v4s3-.5 4-3m-7-1-2 2"/>',
        "flag": '<path d="M4 22V4m0 0c7-4 9 4 16 0v12c-7 4-9-4-16 0"/>',
        "lightbulb": '<path d="M9 18h6m-5 4h4m-3-7a6 6 0 1 1 2 0v3h-2v-3Z"/>',
        "ruler": '<path d="m21.3 8.7-6-6a1 1 0 0 0-1.4 0l-11.2 11.2a1 1 0 0 0 0 1.4l6 6a1 1 0 0 0 1.4 0L21.3 10a1 1 0 0 0 0-1.3Z"/><path d="m7.5 10.5 2 2m1-5 2 2m1-5 2 2m-1 9 2 2"/>',
        "refresh-cw": '<path d="M20 7v5h-5M4 17v-5h5"/><path d="M5.6 9a7 7 0 0 1 11.8-2L20 12M4 12l2.6 5a7 7 0 0 0 11.8-2"/>',
        "battery": '<rect x="2" y="7" width="18" height="10" rx="2"/><path d="M22 11v2m-16-2v2m4-2v2m4-2v2"/>',
        "plug": '<path d="M12 22v-5m-6-5V7m12 5V7M5 7h14m-7 0V2m-4 0h8M7 12h10a5 5 0 0 1-10 0Z"/>',
        "camera": '<path d="M14 4h-4L8 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-4l-2-3Z"/><circle cx="12" cy="13" r="3"/>',
        "wifi": '<path d="M5 12.5a11 11 0 0 1 14 0M8.5 16a5.5 5.5 0 0 1 7 0M12 20h.01M2 9a16 16 0 0 1 20 0"/>',
        "square": '<rect x="4" y="4" width="16" height="16" rx="2"/>',
        "toolbox": '<path d="M3 7h18v13H3zM8 7V4h8v3m-13 5h18m-11 0v2h4v-2"/>',
    };

    const emojiIcons = new Map([
        ["🧠", "brain"], ["🗺️", "map"], ["📚", "books"], ["🎯", "target"],
        ["💻", "monitor"], ["📢", "megaphone-fill"], ["🏆", "trophy-fill"],
        ["⚡", "zap"], ["🎓", "mortarboard-fill"], ["⌨️", "keyboard"],
        ["🐛", "bug"], ["📝", "file-text"], ["🤖", "bot"], ["🐱", "cat"],
        ["🧱", "blocks"], ["🍓", "cpu"], ["🔧", "wrench"], ["⚙️", "settings"],
        ["🌡️", "thermometer"], ["🖥️", "monitor"], ["🗄️", "database"],
        ["🎮", "controller"], ["🌍", "globe"], ["💜", "heart"], ["💼", "briefcase-business"],
        ["📖", "book"], ["💳", "credit-card"], ["✉️", "mail"], ["✅", "check-circle-fill"],
        ["❌", "circle-x"], ["⚠️", "circle-alert"], ["⏱️", "timer"], ["⏳", "hourglass-split"], ["✏️", "pencil"],
        ["✍️", "pencil-line"], ["🕹️", "controller"], ["⚛️", "atom"], ["☁️", "cloud"],
        ["🏗️", "blocks"], ["〰️", "waveform"], ["🔥", "flame"], ["❤️", "heart"],
        ["👨‍🏫", "mortarboard-fill"], ["🌐", "globe"], ["🇰🇪", "globe"],
        ["🇫🇷", "globe"], ["🇧🇷", "globe"], ["☕", "coffee"], ["🌈", "sparkles"],
        ["🌱", "sprout"], ["🎉", "sparkles"], ["🎤", "mic-fill"], ["🎨", "sparkles"],
        ["🎬", "camera-video-fill"], ["🎭", "users"], ["🐍", "code-slash"],
        ["🐣", "heart"], ["👆", "arrow-right"], ["👋", "users"], ["👍", "circle-check"],
        ["👨‍💻", "code-slash"], ["💔", "heart"], ["💡", "lightbulb"], ["💪", "trophy-fill"],
        ["💾", "clipboard"], ["📄", "file-text"], ["📋", "clipboard"], ["📌", "target"],
        ["📏", "ruler"], ["📐", "target"], ["📡", "globe"], ["📦", "folder2-open"],
        ["📶", "wifi"], ["📷", "camera"], ["🔄", "refresh-cw"], ["🔋", "battery"],
        ["🔌", "plug"], ["🔐", "shield-lock"], ["🔘", "circle-help"], ["🔩", "settings"], ["🔴", "circle-help"],
        ["😅", "emoji-smile"], ["🙏", "heart"], ["🚀", "rocket"], ["🚩", "flag"],
        ["🟩", "square"], ["🦄", "sparkles"], ["🧩", "blocks"], ["🧰", "toolbox"],
        ["✨", "sparkles"], ["➰", "refresh-cw"], ["⬜", "square"], ["⚙", "settings"],
        ["→", "arrow-right"], ["←", "arrow-left"], ["▶", "play-fill"], ["◀", "arrow-left"],
    ]);

    const emojiPattern = new RegExp(
        `(${[...emojiIcons.keys()].sort((a, b) => b.length - a.length).map(value => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`,
        "gu",
    );

    function svgMarkup(name, className = "lucide-icon-svg") {
        const paths = icons[name] || icons["circle-help"];
        return `<svg class="${className}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
    }

    function renderEmojis(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const parent = node.parentElement;
            if (!parent || parent.closest("code, pre, script, style, textarea, .lucide-icon")) return;
            const value = node.nodeValue;
            const matches = [...value.matchAll(emojiPattern)];
            if (!matches.length) return;

            const fragment = document.createDocumentFragment();
            let offset = 0;
            matches.forEach(match => {
                fragment.append(document.createTextNode(value.slice(offset, match.index)));
                const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                icon.setAttribute("class", "lucide-icon-svg");
                icon.setAttribute("viewBox", "0 0 24 24");
                icon.setAttribute("fill", "none");
                icon.setAttribute("stroke", "currentColor");
                icon.setAttribute("stroke-width", "2");
                icon.setAttribute("stroke-linecap", "round");
                icon.setAttribute("stroke-linejoin", "round");
                icon.setAttribute("aria-hidden", "true");
                icon.innerHTML = icons[emojiIcons.get(match[0])] || icons["circle-help"];
                fragment.append(icon);
                offset = match.index + match[0].length;
            });
            fragment.append(document.createTextNode(value.slice(offset)));
            node.replaceWith(fragment);
            return;
        }

        if (node.nodeType !== Node.ELEMENT_NODE || node.matches("code, pre, script, style, textarea, svg, .lucide-icon")) return;
        const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
        const textNodes = [];
        while (walker.nextNode()) textNodes.push(walker.currentNode);
        textNodes.forEach(renderEmojis);
    }

    function renderIcon(element) {
        const iconClass = [...element.classList].find(name => name.startsWith("bi-"));
        if (!iconClass) return;

        const name = iconClass.slice(3);
        const paths = icons[name] || icons["circle-help"];
        const extraClasses = [...element.classList]
            .filter(value => value !== "bi" && !value.startsWith("bi-"));
        const wrapper = element.localName === "i" ? document.createElement("span") : element;

        if (element.localName === "i") {
            for (const attribute of element.attributes) {
                if (attribute.name !== "class") wrapper.setAttribute(attribute.name, attribute.value);
            }
            element.replaceWith(wrapper);
        }

        const className = ["lucide-icon", ...extraClasses].join(" ");
        if (wrapper.className !== className) wrapper.className = className;
        wrapper.dataset.lucide = name;
        if (!wrapper.hasAttribute("aria-label")) wrapper.setAttribute("aria-hidden", "true");
        wrapper.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
    }

    function scan(node) {
        renderEmojis(node);
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (node.matches('i[class*="bi-"], span[class*="bi-"]')) renderIcon(node);
        node.querySelectorAll?.('i[class*="bi-"], span[class*="bi-"]').forEach(renderIcon);
    }

    window.CoderGridIcons = {
        render: scan,
        svg: (name, className) => svgMarkup(name, className),
    };

    scan(document.documentElement);
    new MutationObserver(records => {
        records.forEach(record => {
            if (record.type === "attributes") renderIcon(record.target);
            record.addedNodes.forEach(scan);
        });
    }).observe(document.documentElement, {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: ["class"],
    });
})();
