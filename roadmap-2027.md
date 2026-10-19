# 🗺 Roadmap 2027: from Python beginner to Robotics & Physical AI
> **North star:** build a miniature **physical-digital twin of an automated container port**, with a **predictive shadow twin** that runs 60–120 s ahead and prevents cascade failures, and grow into a **Robotics & Physical AI engineer** along the way.
> Assumes **10–12 hours/week on weekdays** (weekends = bonus). Hardware arrives **~May/June 2027 or later**. Stretch freely: **never move on until the mini-project works and I can explain it out loud.**

---

## 🧭 The big picture: 4 tracks running in parallel
| Track | What | When |
|---|---|---|
| 🐍 **Code** | Python → Python libraries → C++ | all year (main track) |
| 📐 **Math for robotics** | vectors, matrices, transforms, probability, a little calculus | 1–2 h/week, all year |
| 🧩 **Problem solving** | LeetCode daily (streak to 31 Dec 2027) + HackerRank | 20–30 min/day |
| 🏗 **Build & share** | Fusion → 3D printing → hardware → YouTube | from Jan 2027 (printer) |

---

## 📅 Quarter by quarter

### Q4 2026 (Oct–Dec): Core Python ✅ *in progress*
**Phase 0 + Phase 1 (part 1).** Where I am now.
| Weeks | Topics | Port anchor ⚓ |
|---|---|---|
| ✅ Wk 1 (12–18 Oct) | print, variables, input, if/else, loops, strings, lists, functions | a list = a container stack |
| Wk 2–3 (19 Oct–2 Nov) | dicts, sets/tuples, comprehensions, errors, files, modules, sorting, recursion, **classes** | dict = the yard map · class = a crane |
| 🏝 3–15 Nov | vacation: daily LeetCode + HackerRank + phone commits | — |
| Wk 6–11 (16 Nov–Dec) | classes deep dive, **JSON**, **`dataclasses`, `enum`, type hints**, `venv` + `pip`, **pytest**, debugging with breakpoints | — |

**Mini-projects (end of Phase 1):**
1. `Container` + `YardSlot` classes, a 2-D yard grid in the terminal (place/remove containers)
2. `Crane` class with a **job queue** moving containers between slots, with timing
3. Save/load the whole yard to **JSON**. This *is* the shadow twin's "snapshot" step!

📐 **Math:** vectors & matrices basics (3Blue1Brown *Essence of Linear Algebra*)

---

### Q1 2027 (Jan–Mar): Python for data & messaging + first hardware
**Phase 2.** 🖨 *Bambu H2S arrives (Jan/Feb): print the POC parts alongside.*
| Topic | Why it matters for the port |
|---|---|
| **NumPy** | fast maths on positions, grids, sensor arrays |
| **pandas** + **matplotlib** | analyse and plot logged crane/truck data |
| **Docker** | run Mosquitto, InfluxDB, Grafana locally in one command |
| **paho-mqtt** | every truck/crane talks over MQTT topics (`meridian/yard/crane01/state`) |
| **asyncio** | many trucks reporting at the same time |
| **pydantic** | validate message formats so bad data can't break the twin |
| **influxdb-client** + **Grafana** | history + live dashboards |
| **asyncua** (OPC UA) | the industrial protocol PLCs speak |

**Mini-project:** *fake truck* publishes position every 500 ms → logger writes to InfluxDB → live Grafana dashboard. **The full POC data pipeline, with no hardware.**
📐 **Math:** 2-D/3-D transforms, rotation matrices, coordinate frames (needed for USD & robotics)

---

### Q2 2027 (Apr–Jun): Drive the twin from code + embedded
**Phase 4 + Phase 5 start.** *My Omniverse/Isaac expertise becomes code.*
| Topic | Why |
|---|---|
| **OpenUSD Python (`pxr`)** | read/write prims, transforms, custom attributes |
| **Omniverse Kit extensions (`omni.*`)** | an extension that subscribes to MQTT and moves prims |
| **Isaac Sim standalone Python** | scripted scenes, stepping physics |
| **ROS 2 + `rclpy`** | nodes, topics, services: the robotics industry's backbone |
| **MicroPython on ESP32** | reuse Python on the hardware: gate servo, limit switches *(only once hardware arrives, ~June)* |

**Mini-projects:**
1. The fake truck's MQTT message moves a truck prim in Isaac Sim live: **the operational twin** 🎉
2. The gate barrier servo opens on an MQTT command and reports its state back *(June/July, or Q3 if hardware is late. Until then, simulate the gate in Python)*

📐 **Math:** quaternions (rotations without gimbal lock), basic kinematics, **PID control**

---

### Q3 2027 (Jul–Sep): Simulation, vision & prediction
**Phase 3.** *The headline feature: the predictive shadow twin.*
| Topic | Why |
|---|---|
| **SimPy** | the fast discrete-event "mental model" of the port |
| **OpenCV** + **ArUco** | the overhead camera tracks trucks/containers → yard coordinates |
| **scikit-learn** | first ML: train/test split, regression, evaluation |
| **PyTorch** → **LSTM** | forecast crane cycle times / queue lengths 60–90 s ahead |
| **Gymnasium** + **Stable-Baselines3 (PPO)** | an RL agent learns truck dispatch inside the simulated port |

**Mini-projects:**
1. SimPy POC model (1 crane, 2 trucks, gate): slow the crane, watch the queues grow
2. **Shadow-twin loop:** snapshot → fork 3 options → fast-forward 90 s → pick the best
3. LSTM predicts truck wait time 60 s ahead
4. A PPO agent beats a simple dispatch rule

🎬 **POC demo:** the cascade failure run **twice on camera**, without and with the shadow twin
📐 **Math:** probability & statistics, gradients (how neural nets learn)

---

### Q4 2027 (Oct–Dec): C++ + Physical AI deep dive
**Phase 6 + the Robotics/Physical AI layer.**
| Topic | Why |
|---|---|
| **Modern C++ (17/20)**, CMake, STL, smart pointers | performance + embedded: where robots really run |
| **Arduino C++ / PlatformIO**, AccelStepper, PubSubClient | precise stepper control for crane axes |
| **rclcpp** (ROS 2 in C++) | production robot nodes |
| **Isaac Lab** | GPU-parallel robot learning (RL at scale) |
| **Replicator** (synthetic data) | train vision models on rendered data: domain randomization |
| **LeRobot / imitation learning** | teach robots from demonstrations: the heart of Physical AI |
| **Sim-to-real** concepts | why sim-trained policies fail on real hardware, and how to fix it |

**Mini-project:** rewrite the Phase 1 crane/yard model in C++ and **benchmark it against Python** (great YouTube episode)
📐 **Math:** optimisation basics, control theory refresher

---

## 🔗 How today's Python course feeds the port
| Course topic | Becomes... |
|---|---|
| lists | a container stack, a truck queue |
| dicts | the yard map `{slot: container}`, MQTT message payloads |
| sets | "which slots are free?", fast membership checks |
| functions | reusable steps: `move_container()`, `score_branch()` |
| classes | `Crane`, `Truck`, `Container`, `Gate`: every physical thing is an object |
| JSON + files | state snapshots, config files |
| `try` / `except` | a twin that survives a bad sensor message |
| modules + `pip` | the door to every library above |
| recursion, sorting, BEST SO FAR | scheduling and choosing the best branch |
| LeetCode patterns | the algorithmic thinking behind dispatch and path planning |

---

## 🧰 Languages & libraries at a glance
| Language | Libraries / tools |
|---|---|
| **Python** (main) | NumPy, pandas, matplotlib, paho-mqtt, asyncio, pydantic, influxdb-client, asyncua, SimPy, OpenCV, scikit-learn, PyTorch, Gymnasium, Stable-Baselines3, pxr (OpenUSD), omni.* (Kit), Isaac Sim / Isaac Lab, rclpy, LeRobot, pytest |
| **C++** | STL, CMake, Eigen, rclcpp, OpenUSD C++, Kit C++ plugins, Arduino (AccelStepper, Servo, PubSubClient), PlatformIO |
| **MicroPython** | ESP32 machine/network modules |
| **Supporting** | Bash, Git, Docker, SQL / Flux, YAML/JSON, Markdown + Mermaid, IEC 61131-3 Structured Text (PLC, later) |
| **Optional later** | CUDA basics |

---

## 📍 Checkpoints
- [ ] **31 Dec 2026:** Phase 1 done: yard grid + crane queue + JSON snapshot work, and I can explain them
- [ ] **31 Mar 2027:** fake-truck → MQTT → InfluxDB → Grafana pipeline live
- [ ] **30 Jun 2027:** MQTT moves a prim in Isaac Sim (gate servo once the hardware is here)
- [ ] **30 Sep 2027:** shadow-twin loop + POC cascade demo filmed
- [ ] **31 Dec 2027:** C++ benchmark done; first Isaac Lab / imitation-learning experiment; LeetCode streak hits day ~440 🔥
