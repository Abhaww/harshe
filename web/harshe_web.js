/**
 * HARSHE WEB IDE, ACADEMY & CANVAS GRAPHICS
 * Full browser execution engine supporting:
 * - Text & Console output
 * - Interactive coding lessons & challenges
 * - 2D Canvas Graphics (`zana_fage`, `zana_da_ira`, `zana_murabba_i`, `zana_layi`, `zana_rubutu`)
 */

// ==========================================
// 1. MISALAI (Sample Programs)
// ==========================================
const SAMPLES = {
    sannu: `# 1. Sannu Duniya a Harshen Harshe
bari sunana = "Aminu";
bari garina = "Kano";
tsayayye KASA = "Nigeria";

buga("========================================");
buga("  Barka da zuwa Harshen Harshe!  ");
buga("========================================");
buga("Sunana:", sunana);
buga("Gari:", garina, "| Kasa:", KASA);

bari sako = "Sannu " + sunana + " daga " + garina + "!";
buga(sako);
`,

    zane: `# 2. Zane da Fasaha (Canvas Graphics)
# Wannan shirin zai zana kyakkyawan hoto a allon Zane!

# 1. Zana Fage mai duhu
zana_fage("#0b132b");

# 2. Zana Hasken Rana/Wata
zana_da_ira(250, 140, 75, "#fbbf24");
zana_da_ira(250, 140, 65, "#fef08a");

# 3. Zana Taurari
ga i a cikin kewayon(1, 15) {
    bari sx = bazuwar_lamba(20, 480);
    bari sy = bazuwar_lamba(20, 200);
    zana_da_ira(sx, sy, 2, "#ffffff");
}

# 4. Zana Gine-gine a kasa
zana_murabba_i(40, 240, 70, 120, "#1e293b");
zana_murabba_i(130, 200, 90, 160, "#334155");
zana_murabba_i(240, 220, 80, 140, "#1e293b");
zana_murabba_i(340, 180, 110, 180, "#334155");

# 5. Rubuta Taken Harshe
zana_rubutu(90, 330, "Harshe Graphics Engine", "#38bdf8", 22);
buga("An kammala zana hoto a allon Zane! (Duba shafin 'Zane')");
`,

    lissafi: `# 3. Lissafi da Sharudda (Math & Conditionals)
bari a = 20;
bari b = 6;

buga("a =", a, ", b =", b);
buga("Tara (+):", a + b);
buga("Debewa (-):", a - b);
buga("Ninkawa (*):", a * b);
buga("Rabawa (/):", a / b);
buga("Sauran Rabo (%):", a % b);

bari maki = 82;
idan (maki >= 75) {
    buga("Maki", maki, "-> Daraja 'A' (Mafi Kyau)");
} ko idan (maki >= 60) {
    buga("Maki", maki, "-> Daraja 'B' (Yayi Kyau)");
} in ba haka ba {
    buga("Maki", maki, "-> Daraja 'C'");
}
`,

    jeri: `# 4. Jeri da Madauki (Lists & Loops)
bari dabbobi = ["Doki", "Saniya", "Akuya", "Rago"];
kara(dabbobi, "Kaza");

buga("Dukkan dabbobin:", dabbobi);
buga("Tsawon jeri:", tsawo(dabbobi));

buga("\nMadaukin 'ga ... a cikin':");
ga dabba a cikin dabbobi {
    buga("  -> Ina kiwon:", dabba);
}

buga("\nMadaukin 'kewayon' (1 zuwa 5):");
ga i a cikin kewayon(1, 6) {
    buga("  Lamba:", i);
}
`,

    fibonacci: `# 5. Ayyuka da Recursion (Fibonacci)
aiki fibonacci(n) {
    idan (n <= 0) {
        koma 0;
    } ko idan (n == 1) {
        koma 1;
    }
    koma fibonacci(n - 1) + fibonacci(n - 2);
}

buga("Jerin Fibonacci na farko 8:");
ga i a cikin kewayon(0, 8) {
    buga("  fib(" + rubutu(i) + ") =", fibonacci(i));
}
`,

    kamus: `# 6. Kamus na Dalibai (Dictionaries)
bari dalibi = {
    "suna": "Zainab Abubakar",
    "shekaru": 21,
    "fanni": "Kimiyyar Kwamfuta",
    "maki": 88
};

buga("Sunan Dalibi:", dalibi["suna"]);
buga("Fannin Karatu:", dalibi["fanni"]);

dalibi["shekaru"] = 22;
buga("Sabunta shekaru:", dalibi["shekaru"]);
buga("Duk bayanan dalibi:", dalibi);
`,

    gwada: `# 7. Gwada da Kama Kuskure (Try/Catch)
gwada {
    buga("Kokarin raba lamba da sifili...");
    bari x = 10 / 0;
    buga("Sakamakon rabo:", x);
} kama (kuskure) {
    buga("[An kama kuskure]:", kuskure);
    buga("Shirin ya ci gaba da aiki lami lafiya!");
}
`
};

// ==========================================
// 2. DARUSSA NA KOYO (Interactive Lessons)
// ==========================================
const LESSONS = [
    {
        id: 1,
        title: "1. Buga Sakon Farko (Hello World)",
        desc: "Koyi yadda ake buga rubutu zuwa allon kwamfuta ta amfani da 'buga'.",
        initialCode: `# Darasi na 1: Buga "Sannu Duniya!"
# Umarni: Yi amfani da 'buga' domin buga kalmar Sannu Duniya!

buga("Sannu Duniya!");
`,
        validate: (output) => output.includes("Sannu Duniya!"),
        hint: "Tabbatar ka rubuta: buga(\"Sannu Duniya!\");"
    },
    {
        id: 2,
        title: "2. Masu Canji da Lissafi (Variables & Math)",
        desc: "Sanar da mai canji tare da 'bari' kuma lissafa hadin lambobi biyu.",
        initialCode: `# Darasi na 2: Masu canji
# Umarni: Sanar da 'bari x = 15;' da 'bari y = 25;' sannan ka buga hadinsu (x + y).

bari x = 15;
bari y = 25;
bari jimilla = x + y;
buga("Jimilla:", jimilla);
`,
        validate: (output) => output.includes("40"),
        hint: "Buga sakamakon 15 + 25 wanda zai ba da 40."
    },
    {
        id: 3,
        title: "3. Hada Rubutu (String Concatenation)",
        desc: "Hada sunan mutum da gaisuwa ta amfani da alamar '+'.",
        initialCode: `# Darasi na 3: Hada Rubutu
# Umarni: Buga sakon "Barka da zuwa, Fatima!" ta amfani da mai canji.

bari suna = "Fatima";
bari sako = "Barka da zuwa, " + suna + "!";
buga(sako);
`,
        validate: (output) => output.includes("Barka da zuwa, Fatima!"),
        hint: "Yi amfani da 'Barka da zuwa, ' + suna + '!'"
    },
    {
        id: 4,
        title: "4. Sharadi da Hukunci (Conditionals)",
        desc: "Bincika idan shekaru sun cika 18 ta amfani da 'idan'.",
        initialCode: `# Darasi na 4: Sharadi
# Umarni: Idan shekaru sun kai 18 ko sama, buga "Babba ne", in ba haka ba "Yaro ne".

bari shekaru = 20;

idan (shekaru >= 18) {
    buga("Babba ne");
} in ba haka ba {
    buga("Yaro ne");
}
`,
        validate: (output) => output.includes("Babba ne"),
        hint: "Tabbatar da sharadin: idan (shekaru >= 18) { buga(\"Babba ne\"); }"
    },
    {
        id: 5,
        title: "5. Madaukin Kewayon (For Loop)",
        desc: "Lissafa lambobi daga 1 zuwa 5 ta amfani da 'ga' da 'kewayon'.",
        initialCode: `# Darasi na 5: Madauki
# Umarni: Buga lambobi 1, 2, 3, 4, 5 ta amfani da madauki.

ga i a cikin kewayon(1, 6) {
    buga(i);
}
`,
        validate: (output) => [1, 2, 3, 4, 5].every(n => output.includes(String(n))),
        hint: "Yi amfani da: ga i a cikin kewayon(1, 6) { buga(i); }"
    },
    {
        id: 6,
        title: "6. Jeri da Kayan Ciki (Lists & Arrays)",
        desc: "Sanya sabon abu a jeri tare da 'kara' kuma nemo tsawonsa tare da 'tsawo'.",
        initialCode: `# Darasi na 6: Jeri
# Umarni: Kirkiri jerin 'ya'yan itace guda 3, sannan ka buga tsawon jerin.

bari 'ya'ya = ["Lemu", "Ayaba", "Mangwaro"];
buga("Tsawon jeri:", tsawo('ya'ya));
`,
        validate: (output) => output.includes("3"),
        hint: "Kira tsawo('ya'ya) wanda zai fitar da 3."
    },
    {
        id: 7,
        title: "7. Kirkirar Aiki (Functions & Return)",
        desc: "Kirkiri aikin 'ninka(x)' wanda yake komar da x * 2.",
        initialCode: `# Darasi na 7: Aiki
# Umarni: Kirkiri aikin ninka lamba biyu kuma ka ninka 50.

aiki ninka(lamba) {
    koma lamba * 2;
}

bari res = ninka(50);
buga("Sakamako:", res);
`,
        validate: (output) => output.includes("100"),
        hint: "Kira ninka(50) wanda zai fitar da 100."
    },
    {
        id: 8,
        title: "8. Kamus na Bayanai (Dictionaries)",
        desc: "Ajiye bayanan mutum a cikin Kamus kuma ka karanta sunansa.",
        initialCode: `# Darasi na 8: Kamus
# Umarni: Ajiye kamus mai suna da shekaru, sannan ka buga sunan.

bari dalibi = {
    "suna": "Usman Aliyu",
    "shekaru": 22
};

buga("Sunan Dalibi:", dalibi["suna"]);
`,
        validate: (output) => output.includes("Usman Aliyu"),
        hint: "Buga dalibi[\"suna\"]"
    }
];

// ==========================================
// 3. IN-BROWSER HARSHE INTERPRETER
// ==========================================

class HarsheWebEngine {
    constructor(outputCallback, canvasElement, onCanvasDraw) {
        this.output = outputCallback;
        this.canvas = canvasElement;
        this.ctx = canvasElement ? canvasElement.getContext('2d') : null;
        this.onCanvasDraw = onCanvasDraw;
        this.capturedOutput = "";
        this.hasDrawn = false;
    }

    run(source) {
        this.capturedOutput = "";
        this.hasDrawn = false;
        try {
            const translatedJs = this.translateToJS(source);
            const env = this.createGlobalEnv();
            this.evaluate(translatedJs, env);
            if (this.hasDrawn && this.onCanvasDraw) {
                this.onCanvasDraw();
            }
            return { success: true, output: this.capturedOutput, hasDrawn: this.hasDrawn };
        } catch (err) {
            const errMsg = `\n[Kuskure]: ${err.message}\n`;
            this.output(errMsg, true);
            this.capturedOutput += errMsg;
            return { success: false, output: this.capturedOutput, error: err.message };
        }
    }

    createGlobalEnv() {
        const env = {};

        // Console & I/O
        env['buga'] = (...args) => {
            const text = args.map(a => this.stringify(a)).join(' ');
            this.output(text + '\n');
            this.capturedOutput += text + '\n';
            return null;
        };

        env['karba'] = (promptText = '') => {
            const res = window.prompt(promptText ? String(promptText) : "Shigar da bayani:");
            return res !== null ? String(res) : "";
        };

        // 🎨 Canvas Graphics
        env['zana_fage'] = (launi = '#020617') => {
            if (!this.ctx) return;
            this.ctx.fillStyle = String(launi);
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            this.hasDrawn = true;
        };

        env['zana_da_ira'] = (x, y, r, launi = '#10b981') => {
            if (!this.ctx) return;
            this.ctx.beginPath();
            this.ctx.arc(Number(x), Number(y), Number(r), 0, Math.PI * 2);
            this.ctx.fillStyle = String(launi);
            this.ctx.fill();
            this.hasDrawn = true;
        };

        env['zana_murabba_i'] = (x, y, w, h, launi = '#06b6d4') => {
            if (!this.ctx) return;
            this.ctx.fillStyle = String(launi);
            this.ctx.fillRect(Number(x), Number(y), Number(w), Number(h));
            this.hasDrawn = true;
        };

        env['zana_layi'] = (x1, y1, x2, y2, launi = '#ffffff', kauri = 2) => {
            if (!this.ctx) return;
            this.ctx.beginPath();
            this.ctx.moveTo(Number(x1), Number(y1));
            this.ctx.lineTo(Number(x2), Number(y2));
            this.ctx.strokeStyle = String(launi);
            this.ctx.lineWidth = Number(kauri);
            this.ctx.stroke();
            this.hasDrawn = true;
        };

        env['zana_rubutu'] = (x, y, rubutu, launi = '#ffffff', girma = 16) => {
            if (!this.ctx) return;
            this.ctx.fillStyle = String(launi);
            this.ctx.font = `${Number(girma)}px Outfit, sans-serif`;
            this.ctx.fillText(String(rubutu), Number(x), Number(y));
            this.hasDrawn = true;
        };

        // Stdlib
        env['tsawo'] = (obj) => {
            if (typeof obj === 'string') return obj.length;
            if (Array.isArray(obj)) return obj.length;
            if (typeof obj === 'object' && obj !== null) return Object.keys(obj).length;
            return 0;
        };

        env['kewayon'] = (start, stop, step = 1) => {
            if (stop === undefined) { stop = start; start = 0; }
            const res = [];
            for (let i = start; i < stop; i += step) res.push(i);
            return res;
        };

        env['nau_i'] = (x) => {
            if (typeof x === 'number') return 'lamba';
            if (typeof x === 'string') return 'rubutu';
            if (typeof x === 'boolean') return "dabi'a";
            if (Array.isArray(x)) return 'jeri';
            if (typeof x === 'object' && x !== null) return 'kamus';
            if (typeof x === 'function') return 'aiki';
            return 'babu';
        };

        env['lamba'] = (x) => Number(x) || 0;
        env['rubutu'] = (x) => this.stringify(x);
        env['dabi_a'] = (x) => Boolean(x);
        env['kara'] = (arr, item) => { if (Array.isArray(arr)) arr.push(item); return arr; };
        env['cire'] = (arr) => { if (Array.isArray(arr)) return arr.pop(); return null; };
        env['raba'] = (str, delim = ' ') => String(str).split(delim);
        env['hade'] = (arr, sep = '') => Array.isArray(arr) ? arr.join(sep) : '';
        env['cikakken_lamba'] = (n) => Math.abs(n);
        env['zagaye'] = (n, d = 0) => Number(Math.round(n + 'e' + d) + 'e-' + d);
        env['mafi_girma'] = (...args) => {
            if (args.length === 1 && Array.isArray(args[0])) return Math.max(...args[0]);
            return Math.max(...args);
        };
        env['mafi_kankanta'] = (...args) => {
            if (args.length === 1 && Array.isArray(args[0])) return Math.min(...args[0]);
            return Math.min(...args);
        };
        env['tushe'] = (n) => Math.sqrt(n);
        env['iko'] = (a, b) => Math.pow(a, b);
        env['lokaci'] = () => Date.now() / 1000;
        env['bazuwar_lamba'] = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;
        env['zabi_a_jeri'] = (arr) => Array.isArray(arr) ? arr[Math.floor(Math.random() * arr.length)] : null;
        env['karanta_json'] = (s) => JSON.parse(s);
        env['rubuta_json'] = (obj) => JSON.stringify(obj);

        return env;
    }

    stringify(val) {
        if (val === null || val === undefined) return 'babu';
        if (val === true) return 'gaskiya';
        if (val === false) return 'karya';
        if (Array.isArray(val)) return '[' + val.map(v => this.stringify(v)).join(', ') + ']';
        if (typeof val === 'object' && typeof val !== 'function') {
            const pairs = Object.entries(val).map(([k, v]) => `"${k}": ${this.stringify(v)}`);
            return '{' + pairs.join(', ') + '}';
        }
        return String(val);
    }

    translateToJS(source) {
        let js = source;
        js = js.replace(/#.*$/gm, '');

        const stringTable = [];
        js = js.replace(/(["'])(?:(?=(\\?))\2[\s\S])*?\1/g, (match) => {
            const placeholder = `___STR_${stringTable.length}___`;
            stringTable.push(match);
            return placeholder;
        });

        js = js.replace(/\bin ba haka ba\b/gi, 'else');
        js = js.replace(/\bko idan\b/gi, 'else if');
        js = js.replace(/\byayin da\b/gi, 'while');
        js = js.replace(/\ba cikin\b/gi, 'of');
        js = js.replace(/\bci gaba\b|\bci_gaba\b/gi, 'continue');
        js = js.replace(/\bshigo da\b|\bshigo_da\b/gi, '// import');

        js = js.replace(/\bidan\b/gi, 'if');
        js = js.replace(/\bbari\b|\bsaka\b/gi, 'let');
        js = js.replace(/\btsayayye\b/gi, 'const');
        js = js.replace(/\baiki\b\s+([a-zA-Z0-9_']+)/gi, 'function $1');
        js = js.replace(/\bkoma\b/gi, 'return');
        js = js.replace(/\btsaya\b/gi, 'break');
        js = js.replace(/\bgwada\b/gi, 'try');
        js = js.replace(/\bkama\b/gi, 'catch');
        js = js.replace(/\bgaskiya\b/gi, 'true');
        js = js.replace(/\bkarya\b/gi, 'false');
        js = js.replace(/\bbabu\b/gi, 'null');
        js = js.replace(/\bkuma\b/gi, '&&');
        js = js.replace(/\bko\b/gi, '||');
        js = js.replace(/\bba\s+/gi, '!');

        js = js.replace(/\bga\s+([a-zA-Z0-9_']+)\s+of\s+([^\{]+)\{/gi, 'for (let $1 of ($2)) {');

        js = js.replace(/\bnau'i\b/gi, 'nau_i');
        js = js.replace(/\bdabi'a\b/gi, 'dabi_a');
        js = js.replace(/([a-zA-Z0-9_]+)'([a-zA-Z0-9_]+)/g, '$1_$2');

        stringTable.forEach((str, idx) => {
            js = js.replace(`___STR_${idx}___`, str);
        });

        return js;
    }

    evaluate(translatedJs, env) {
        const keys = Object.keys(env);
        const values = keys.map(k => env[k]);
        const safeCode = `\n${translatedJs}\n`;
        const runner = new Function(...keys, safeCode);
        runner(...values);
    }
}

// ==========================================
// 4. UI CONTROLLER & ACADEMY MANAGER
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const editor = document.getElementById('codeEditor');
    const lineNumbers = document.getElementById('lineNumbers');
    const consoleOutput = document.getElementById('consoleOutput');
    const runBtn = document.getElementById('runBtn');
    const checkLessonBtn = document.getElementById('checkLessonBtn');
    const clearConsoleBtn = document.getElementById('clearConsoleBtn');
    const clearCanvasBtn = document.getElementById('clearCanvasBtn');
    const exampleSelect = document.getElementById('exampleSelect');
    const harsheCanvas = document.getElementById('harsheCanvas');

    const tabOutputBtn = document.getElementById('tabOutputBtn');
    const tabCanvasBtn = document.getElementById('tabCanvasBtn');
    const tabLessonsBtn = document.getElementById('tabLessonsBtn');
    const tabDocsBtn = document.getElementById('tabDocsBtn');

    const outputTab = document.getElementById('outputTab');
    const canvasTab = document.getElementById('canvasTab');
    const lessonsTab = document.getElementById('lessonsTab');
    const docsTab = document.getElementById('docsTab');

    const editorStatus = document.getElementById('editorStatus');
    const lessonsList = document.getElementById('lessonsList');
    const lessonProgressBar = document.getElementById('lessonProgressBar');
    const lessonProgressText = document.getElementById('lessonProgressText');
    const lessonBanner = document.getElementById('lessonBanner');
    const activeFileName = document.getElementById('activeFileName');

    let currentLesson = null;
    let completedLessons = new Set();

    function updateLineNumbers() {
        const lines = editor.value.split('\n').length;
        lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
    }

    editor.addEventListener('input', updateLineNumbers);
    editor.addEventListener('scroll', () => {
        lineNumbers.scrollTop = editor.scrollTop;
    });

    editor.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = editor.selectionStart;
            const end = editor.selectionEnd;
            editor.value = editor.value.substring(0, start) + "    " + editor.value.substring(end);
            editor.selectionStart = editor.selectionEnd = start + 4;
            updateLineNumbers();
        } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (currentLesson) {
                checkLessonSolution();
            } else {
                runCode();
            }
        }
    });

    function runCode() {
        consoleOutput.innerHTML = '';
        lessonBanner.style.display = 'none';
        editorStatus.textContent = 'Ana aiki... (Running)';
        editorStatus.style.color = '#38bdf8';

        const engine = new HarsheWebEngine(
            (text, isError = false) => {
                if (isError) {
                    consoleOutput.innerHTML += `<span class="console-error">${escapeHtml(text)}</span>`;
                } else {
                    consoleOutput.innerHTML += escapeHtml(text);
                }
            },
            harsheCanvas,
            () => {
                tabCanvasBtn.click();
            }
        );

        const startTime = performance.now();
        const res = engine.run(editor.value);
        const duration = (performance.now() - startTime).toFixed(2);

        editorStatus.textContent = `Kammala cikin ${duration}ms (Done)`;
        editorStatus.style.color = '#10b981';

        if (!res.hasDrawn) {
            tabOutputBtn.click();
        }
        return res;
    }

    function checkLessonSolution() {
        const res = runCode();
        if (currentLesson && currentLesson.validate) {
            const passed = res.success && currentLesson.validate(res.output);
            lessonBanner.style.display = 'flex';
            if (passed) {
                lessonBanner.className = 'lesson-banner success';
                lessonBanner.innerHTML = `<span><strong>🎉 Madalla!</strong> Ka amsa wannan darasi daidai!</span> <button class="btn btn-primary" id="nextLessonBtn">Darasi Na Gaba (Next) →</button>`;
                completedLessons.add(currentLesson.id);
                updateLessonsUI();

                const nextBtn = document.getElementById('nextLessonBtn');
                if (nextBtn) {
                    nextBtn.addEventListener('click', () => {
                        const nextId = currentLesson.id + 1;
                        if (nextId <= LESSONS.length) {
                            loadLesson(nextId);
                        } else {
                            alert("Barka! Ka kammala dukkan darussan Harshe Academy! 🏆");
                        }
                    });
                }
            } else {
                lessonBanner.className = 'lesson-banner fail';
                lessonBanner.innerHTML = `<span><strong>❌ Ba daidai ba:</strong> Duba umarnin ka sake gwadawa. <br><small>${escapeHtml(currentLesson.hint || '')}</small></span>`;
            }
        }
    }

    checkLessonBtn.addEventListener('click', checkLessonSolution);

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    runBtn.addEventListener('click', runCode);
    clearConsoleBtn.addEventListener('click', () => {
        consoleOutput.innerHTML = '';
        lessonBanner.style.display = 'none';
    });

    if (clearCanvasBtn && harsheCanvas) {
        clearCanvasBtn.addEventListener('click', () => {
            const ctx = harsheCanvas.getContext('2d');
            ctx.clearRect(0, 0, harsheCanvas.width, harsheCanvas.height);
        });
    }

    exampleSelect.addEventListener('change', (e) => {
        currentLesson = null;
        checkLessonBtn.style.display = 'none';
        activeFileName.textContent = 'babban_shiri.hausa';
        const key = e.target.value;
        if (SAMPLES[key]) {
            editor.value = SAMPLES[key];
            updateLineNumbers();
            runCode();
        }
    });

    // ACADEMY LESSONS MANAGER
    function renderLessons() {
        lessonsList.innerHTML = '';
        LESSONS.forEach(l => {
            const card = document.createElement('div');
            card.className = `lesson-card ${currentLesson && currentLesson.id === l.id ? 'active' : ''} ${completedLessons.has(l.id) ? 'completed' : ''}`;
            card.innerHTML = `
                <div class="lesson-info">
                    <h4>${escapeHtml(l.title)}</h4>
                    <p>${escapeHtml(l.desc)}</p>
                </div>
                <div class="lesson-badge">${completedLessons.has(l.id) ? '✓ Kammala' : 'Darasi'}</div>
            `;
            card.addEventListener('click', () => loadLesson(l.id));
            lessonsList.appendChild(card);
        });
        updateLessonsUI();
    }

    function loadLesson(id) {
        const lesson = LESSONS.find(l => l.id === id);
        if (!lesson) return;

        currentLesson = lesson;
        activeFileName.textContent = `darasi_${lesson.id}.hausa`;
        editor.value = lesson.initialCode;
        updateLineNumbers();

        checkLessonBtn.style.display = 'inline-flex';
        tabOutputBtn.click();
        runCode();
        renderLessons();
    }

    function updateLessonsUI() {
        const count = completedLessons.size;
        const total = LESSONS.length;
        const pct = Math.round((count / total) * 100);
        lessonProgressBar.style.width = `${pct}%`;
        lessonProgressText.textContent = `${count} / ${total} Darussa Kammalu (${pct}%)`;
    }

    // TABS SWITCHING
    function switchTab(btn, tab) {
        [tabOutputBtn, tabCanvasBtn, tabLessonsBtn, tabDocsBtn].forEach(b => b.classList.remove('active'));
        [outputTab, canvasTab, lessonsTab, docsTab].forEach(t => t.classList.remove('active'));
        btn.classList.add('active');
        tab.classList.add('active');
    }

    tabOutputBtn.addEventListener('click', () => switchTab(tabOutputBtn, outputTab));
    tabCanvasBtn.addEventListener('click', () => switchTab(tabCanvasBtn, canvasTab));
    tabLessonsBtn.addEventListener('click', () => {
        switchTab(tabLessonsBtn, lessonsTab);
        renderLessons();
    });
    tabDocsBtn.addEventListener('click', () => switchTab(tabDocsBtn, docsTab));

    // MODAL HANDLERS
    const downloadModalBtn = document.getElementById('downloadModalBtn');
    const downloadModal = document.getElementById('downloadModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    if (downloadModalBtn && downloadModal && closeModalBtn) {
        downloadModalBtn.addEventListener('click', () => {
            downloadModal.style.display = 'flex';
        });

        closeModalBtn.addEventListener('click', () => {
            downloadModal.style.display = 'none';
        });

        downloadModal.addEventListener('click', (e) => {
            if (e.target === downloadModal) {
                downloadModal.style.display = 'none';
            }
        });
    }

    // Default startup
    editor.value = SAMPLES.sannu;
    updateLineNumbers();
    renderLessons();
});

