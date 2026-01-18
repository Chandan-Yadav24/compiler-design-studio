import streamlit as st
import pandas as pd
import json
import base64
from collections import deque

# --- Conversion Logic (Internal) ---
def epsilon_closure(states, nfa_transitions):
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for eps in ['e', 'l', 'ε', 'λ']:
            if (s, eps) in nfa_transitions:
                for next_s in nfa_transitions[(s, eps)]:
                    if next_s not in closure:
                        closure.add(next_s)
                        stack.append(next_s)
    return tuple(sorted(list(closure)))

def move(states, symbol, nfa_transitions):
    res = set()
    for s in states:
        if (s, symbol) in nfa_transitions:
            res.update(nfa_transitions[(s, symbol)])
    return tuple(sorted(list(res)))

def render_lab():
    st.header("🔬 NFA to DFA: The Ultimate Interactive Lab")
    st.write("Draw your NFA with your mouse, and watch the Python engine convert it to a DFA! 🚀")

    # --- Step 0: Check for incoming data from JS (The Bridge) ---
    params = st.query_params
    if "nfa_data" in params:
        try:
            raw_data = base64.b64decode(params["nfa_data"]).decode('utf-8')
            json_data = json.loads(raw_data)
            st.session_state.current_nfa = json_data
            # Clear params after picking up data to avoid infinite loop
            st.query_params.clear()
            st.success("✅ NFA Data Synchronized! Processing...")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to sync data: {str(e)}")

    # Initialize session state for NFA
    if "current_nfa" not in st.session_state:
        st.session_state.current_nfa = {
            "nodes": [{"id": 1, "label": "q0", "isStart": True, "isFinal": False}],
            "edges": []
        }

    # --- Step 1: Mouse-Driven Drawing Canvas ---
    st.subheader("🎨 Draw Your NFA (Mouse & GUI)")
    
    with st.expander("🛠️ Advanced / Troubleshooting", expanded=False):
        st.markdown("**Manual JSON Import**")
        st.caption("If the 'Export' button doesn't work (due to browser security), paste the JSON code here from the canvas tool.")
        manual_json = st.text_area("Paste NFA JSON here", height=100)
        if st.button("📥 Import Manually"):
            try:
                st.session_state.current_nfa = json.loads(manual_json)
                st.success("Imported successfully!")
                st.rerun()
            except:
                st.error("Invalid JSON format.")

    st.info("💡 **How to Draw:** 1. Double-click to add states. 2. Drag from node center to connect. 3. Click 'EXPORT' to convert.")

    # HTML/JS Visual Builder with Python Bridge
    vis_data_json = json.dumps(st.session_state.current_nfa)
    
    vis_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {{
                width: 100%;
                height: 500px;
                border: 2px solid #3b82f6;
                background-color: #111111;
                border-radius: 12px;
            }}
            .toolbar {{
                display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;
                padding: 12px; background: #1e1e1e; border-radius: 8px; border: 1px solid #333;
            }}
            button {{
                padding: 8px 14px; cursor: pointer; border: none; border-radius: 6px; font-weight: bold;
                transition: transform 0.1s, opacity 0.2s;
            }}
            button:active {{ transform: scale(0.95); opacity: 0.8; }}
            .btn-blue {{ background: #3b82f6; color: white; }}
            .btn-green {{ background: #10b981; color: white; }}
            .btn-red {{ background: #ef4444; color: white; }}
            .btn-orange {{ background: #f59e0b; color: white; }}
            input {{ padding: 7px; border-radius: 4px; border: 1px solid #444; background: #333; color: white; width: 60px; }}
            .hint {{ font-size: 11px; color: #888; margin-top: 5px; }}
            #json-display {{ display: none; margin-top: 10px; width: 100%; height: 60px; background: #000; color: #0f0; border: 1px solid #333; font-family: monospace; font-size: 10px; }}
        </style>
    </head>
    <body style="margin: 0; font-family: sans-serif; color: white;">
        <div class="toolbar">
            <strong>Drawing Tools:</strong>
            <input type="text" id="stateLabel" placeholder="q0">
            <button class="btn-blue" onclick="addNode(false, false)">+ State</button>
            <button class="btn-blue" onclick="addNode(true, false)">⚓ Start</button>
            <button class="btn-green" onclick="addNode(false, true)">🌟 Final</button>
            <div style="border-left: 1px solid #444; margin-left:10px; padding-left:10px;">
                <button class="btn-orange" onclick="processNFA()">🚀 EXPORT & CONVERT</button>
                <button class="btn-red" onclick="clearAll()">🗑️ Reset Canvas</button>
                <button style="background: #444; color: #ccc;" onclick="toggleJSON()">📋 Show Code</button>
            </div>
        </div>
        
        <div id="mynetwork"></div>
        <textarea id="json-display" readonly placeholder="Click 'Show Code' to see NFA JSON for manual import if needed..."></textarea>
        <div class="hint">Instructions: Drag between circles to draw arrows. Double-click space to add circles. Use 'e' or 'l' for empty moves.</div>

        <script>
            var container = document.getElementById('mynetwork');
            var rawData = {vis_data_json};
            
            var nodes = new vis.DataSet(rawData.nodes);
            var edges = new vis.DataSet(rawData.edges);

            var options = {{
                nodes: {{
                    shape: 'circle', size: 35,
                    font: {{ color: '#fff', size: 16 }},
                    color: {{ background: '#1e293b', border: '#3b82f6', highlight: {{ background: '#1e3a8a', border: '#60a5fa' }} }}
                }},
                edges: {{
                    arrows: {{ to: {{ enabled: true }} }},
                    font: {{ color: '#fff', size: 14, strokeWidth: 0, align: 'top' }},
                    color: {{ color: '#64748b', highlight: '#3b82f6' }},
                    smooth: {{ type: 'curvedCW', roundness: 0.2 }}
                }},
                manipulation: {{
                    enabled: true,
                    addNode: false,
                    addEdge: function(data, callback) {{
                        var label = prompt("Transition Symbol (use 'e' for ε, 'l' for λ):", "a");
                        if (label) {{
                            data.label = (label == 'e' || label == 'ε') ? 'ε' : ((label == 'l' || label == 'λ') ? 'λ' : label);
                            callback(data);
                        }}
                    }},
                    editEdge: true,
                    deleteNode: true,
                    deleteEdge: true
                }},
                physics: {{ enabled: true, stabilization: true }}
            }};

            var network = new vis.Network(container, {{nodes: nodes, edges: edges}}, options);

            function addNode(isStart, isFinal) {{
                var label = document.getElementById('stateLabel').value || 'q' + nodes.length;
                var color = isStart ? '#3b82f6' : (isFinal ? '#10b981' : '#1e293b');
                var border = isStart ? '#fff' : (isFinal ? '#fff' : '#3b82f6');
                nodes.add({{
                    id: new Date().getTime(),
                    label: label,
                    isStart: isStart,
                    isFinal: isFinal,
                    color: {{ background: color, border: border }},
                    shape: isFinal ? 'doublecircle' : 'circle'
                }});
                document.getElementById('stateLabel').value = '';
            }}

            function clearAll() {{
                if(confirm("Wipe canvas?")){{ nodes.clear(); edges.clear(); }}
            }}

            function toggleJSON() {{
                var area = document.getElementById('json-display');
                var nData = {{ nodes: nodes.get(), edges: edges.get() }};
                area.value = JSON.stringify(nData);
                area.style.display = (area.style.display == 'none' || area.style.display == '') ? 'block' : 'none';
            }}

            function processNFA() {{
                var nData = {{ nodes: nodes.get(), edges: edges.get() }};
                var jsonStr = JSON.stringify(nData);
                var encoded = btoa(unescape(encodeURIComponent(jsonStr)));
                
                try {{
                    // Try the parent location update
                    var url = new URL(window.parent.location.href);
                    url.searchParams.set('nfa_data', encoded);
                    window.parent.location.href = url.href;
                }} catch (e) {{
                   // If blocked by iframe, try window.top
                   try {{
                       var url = new URL(window.top.location.href);
                       url.searchParams.set('nfa_data', encoded);
                       window.top.location.href = url.href;
                   }} catch (err) {{
                       alert("AUTO-EXPORT BLOCKED: Please click 'Show Code' below, copy the text, and paste it into the 'Manual JSON Import' section in Python.");
                       toggleJSON();
                   }}
                }}
            }}
        </script>
    </body>
    </html>
    """
    st.components.v1.html(vis_html, height=620)

    # --- Step 2: Python Processing (The Power Part) ---
    current_nfa = st.session_state.current_nfa
    if current_nfa.get("edges") or current_nfa.get("nodes"):
        st.markdown("---")
        st.header("🔬 NFA Analysis & Conversion Results")
        
        # Data Extraction
        nodes = current_nfa["nodes"]
        edges = current_nfa["edges"]
        id_to_label = {n["id"]: n["label"] for n in nodes}
        Q = sorted(list(set(n["label"] for n in nodes)))
        q0 = next((n["label"] for n in nodes if n.get("isStart")), "q0")
        F = sorted(list(set(n["label"] for n in nodes if n.get("isFinal"))))
        
        # Build Transition Map
        nfa_transitions = {}
        found_alphabet = set()
        for edge in edges:
            u = id_to_label.get(edge["from"])
            v = id_to_label.get(edge["to"])
            s = edge.get("label", "ε")
            if u and v:
                sym = 'e' if s in ['ε', 'e'] else ('l' if s in ['λ', 'l'] else s)
                key = (u, sym)
                if key not in nfa_transitions: nfa_transitions[key] = []
                nfa_transitions[key].append(v)
                if sym not in ['e', 'l']: found_alphabet.add(sym)
        
        Sigma = sorted(list(found_alphabet))

        # --- A. NFA Graph Preview ---
        st.subheader("1️⃣ NFA Diagram (Reconstructed)")
        nfa_dot = 'digraph { rankdir=LR; bgcolor="transparent"; node [shape=circle, fontcolor=white, color=white, style=filled, fillcolor="#1e293b"]; edge [color=white, fontcolor=white]; '
        nfa_dot += 'start [shape=none, label="", width=0, height=0]; '
        nfa_dot += f'start -> "{q0}"; '
        for n in nodes:
            lbl = n["label"]
            shape = "doublecircle" if n.get("isFinal") else "circle"
            color = "#10b981" if n.get("isFinal") else ("#3b82f6" if n.get("isStart") else "#1e293b")
            nfa_dot += f'"{lbl}" [shape={shape}, fillcolor="{color}"]; '
        for edge in edges:
            u, v, s = id_to_label[edge["from"]], id_to_label[edge["to"]], edge.get("label", "ε")
            nfa_dot += f'"{u}" -> "{v}" [label="{s}"]; '
        nfa_dot += '}'
        st.graphviz_chart(nfa_dot)

        # --- B. Formal 5-Elements ---
        st.subheader("2️⃣ Formal 5-Tuple Definition")
        st.latex(r"M = (Q, \Sigma, \delta, q_0, F)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"- **States ($Q$):** `{{ {', '.join(Q)} }}`")
            st.markdown(f"- **Alphabet ($\Sigma$):** `{{ {', '.join(Sigma)} }}`")
            st.markdown(f"- **Start State ($q_0$):** `{q0}`")
        with c2:
            st.markdown(f"- **Final States ($F$):** `{{ {', '.join(F)} }}`")
            st.markdown(r"- **Transition Function ($\delta$):** $Q \times (\Sigma \cup \{\epsilon\}) \to 2^Q$")

        # --- C. NFA Table ---
        st.subheader("3️⃣ NFA Transition Table ($\delta$)")
        nfa_table_data = []
        for state in Q:
            row = {"State": state}
            for sym in Sigma + (['ε'] if any(k[1] in ['e', 'l'] for k in nfa_transitions) else []):
                norm_sym = 'e' if sym == 'ε' else sym
                targets = nfa_transitions.get((state, norm_sym), [])
                row[sym] = "{" + ", ".join(targets) + "}" if targets else "∅"
            nfa_table_data.append(row)
        st.table(pd.DataFrame(nfa_table_data))

        # --- D. Subset Construction & DFA ---
        st.subheader("4️⃣ Subset Construction & Resulting DFA")
        
        dfa_states_subsets = []
        dfa_map = {}
        start_closure = epsilon_closure([q0], nfa_transitions)
        dfa_states_subsets.append(start_closure)
        queue = deque([start_closure])
        visited = {start_closure}
        
        while queue:
            curr = queue.popleft()
            for char in Sigma:
                next_raw = move(curr, char, nfa_transitions)
                next_closure = epsilon_closure(next_raw, nfa_transitions)
                target = next_closure if next_closure else tuple()
                dfa_map[(curr, char)] = target
                if target and target not in visited:
                    visited.add(target)
                    dfa_states_subsets.append(target)
                    queue.append(target)

        # Mapping to formal set names {q0, q1}...
        subset_to_name = {subset: ("{" + ", ".join(subset) + "}") for subset in dfa_states_subsets}
        subset_to_name[tuple()] = "∅"

        # DFA Table
        dfa_table_data = []
        for subset in dfa_states_subsets:
            row = {"DFA State (Subset)": subset_to_name[subset]}
            for char in Sigma:
                target = dfa_map.get((subset, char), tuple())
                row[f"on '{char}'"] = subset_to_name[target]
            dfa_table_data.append(row)
        
        st.markdown("**DFA Transition Table ($M'$)**")
        st.table(pd.DataFrame(dfa_table_data))

        # --- E. Final DFA Graph ---
        st.markdown("**Final DFA Diagram**")
        dfa_dot = 'digraph { rankdir=LR; bgcolor="transparent"; node [shape=circle, fontcolor=white, color=white, style=filled, fillcolor="#1e293b"]; edge [color=white, fontcolor=white]; '
        dfa_dot += 'start [shape=none, label="", width=0, height=0]; '
        dfa_dot += f'start -> "{subset_to_name[start_closure]}"; '
        
        # Add nodes and edges
        used_null = False
        for subset in dfa_states_subsets:
            name = subset_to_name[subset]
            is_fin = any(n in F for n in subset)
            shape = "doublecircle" if is_fin else "circle"
            color = "#10b981" if is_fin else ("#3b82f6" if subset == start_closure else "#1e293b")
            dfa_dot += f'"{name}" [shape={shape}, fillcolor="{color}"]; '
            
            for char in Sigma:
                tgt = dfa_map.get((subset, char), tuple())
                tgt_name = subset_to_name[tgt]
                if tgt_name == "∅": used_null = True
                dfa_dot += f'"{name}" -> "{tgt_name}" [label="{char}"]; '
        
        if used_null:
            dfa_dot += '"∅" [shape=circle, fillcolor="#444", color="#888"]; '
            for char in Sigma:
                dfa_dot += '"∅" -> "∅" [label="' + char + '"]; '

        dfa_dot += '}'
        st.graphviz_chart(dfa_dot)
        st.success(f"✨ Successfully converted NFA ({len(Q)} states) to DFA ({len(dfa_states_subsets)} states).")


    st.markdown("---")
    if st.button("Next Topic: 3.1 Grammar Basics (4-Tuple) ➡️", use_container_width=True):
        st.session_state.unit1_topic = "3.1 Grammar Basics (4-Tuple)"
        st.rerun()
