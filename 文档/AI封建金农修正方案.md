# AI 封建金农修正方案（2026-10-19）

## 1. 问题

封建时代起靶场后 AI 仍然持续挖黄金。模组封建主力（步弓/掷矛/长矛系）全是肉木单位，
前期挖金纯浪费木材食物采集力；金只需要服务升城（400G）、铁匠铺科技（150~275G）和
后段剑士线。期望行为：**封建前期 0 金农，后期一个窗口集中攒金**，而不是全程常驻。

## 2. 机制核查结论（逐条已验证）

| # | 结论 | 出处 |
|---|---|---|
| 1 | 农民分配唯一杠杆 = 4 个百分比 SN（sn-wood/food/gold/stone-gatherer-percentage）；全 Promisory 无 sn-gather-first 类直接指派机制 | 全库 grep |
| 2 | `total-gold-amount`（goal 314）由 init.per 的 `(true)` 规则**每 tick** 从 `gold-amount` fact 刷新 = 当前库存金（不含 escrow），Mimiso 4a 分档条件有效 | init.per L841-846 |
| 3 | 加载链：gatherers(9) < researches(15) < buildings(17) < units(18) < … < **MimisoRules(末)**；同 tick 内后加载的 set-strategic-number 覆盖先加载的 | 模组 PromiDE.per2 |
| 4 | 官方"起靶场加金农"实锤：封建 ≥1 靶场 → 48/37/**15**，≥2 靶场+铁匠铺 → 40/44/**16**，为原版 45 金弩手调校 | gatherers.per L88-118 |
| 5 | units.per（模组覆盖版）里 17 处 gold-gatherer-percentage **全是读取**（条件判断），无设定点；官方封建金农唯一来源是 gatherers.per | units.per grep |
| 6 | goal 号 3020-3029 已占用（backup-direction ~ fwd-villager-id），**3030-3099 全空闲** | customConstants.per L1792-1803 |

## 3. 现状根因

覆盖**没有失败**。MimisoRules 4a 自己在封建全程保留常驻金农：

- `<400 金`：28%（为 400 金升城攒金，比官方 15% 还高）
- `400~850`：16%（马轭/重犁完成后 14%）
- `≥850`：12%
- `villager < 18` 窗口：不覆盖，回落官方 13~15%

即"收掉靶场金农"实际做成了"调低但全程不断金"。要改的是**分配结构**，不是再调数值。

## 4. 方案 A（已实施 2026-10-19，触发按"出兵优先"调整）：两段式 + goal 锁存

### 设计

| 阶段 | 触发 | 木/食/金/石 | 目的 |
|---|---|---|---|
| G0 | 封建开局 → 锁存前 | 48/52/0/0（木食比可调） | 步弓线+靶场+农场全力暴兵，0 金农 |
| 锁存 | 军事人口 ≥24（兵出够才攒钱）**或** 封建满 10 分钟（兜底）**或** 库存金 ≥400 | set-goal mimiso-goldbank yes | 出兵优先：封建先暴兵，攒金窗口越晚越好 |
| G1a | 锁存后，金 <850 | 35/37/28/0 | 攒升城 400G + 铁匠铺 150-275G |
| G1b | 锁存后，金 ≥850 | 42/46/12/0 | 富余转木食 |
| 复位 | 进城堡/帝王 | set-goal mimiso-goldbank no | 交回 4b/4c |

### 为什么需要 goal 锁存

触发条件本身会回落：4f 重开训练花粮、兵被杀导致 military-population 下降——直接用
这些条件切档位会来回震荡（金农↔木食农反复横跳，引擎重新分配有延迟，浪费采集时间）。
goal 锁存后一次触发、封建期内不回退。

### 与 4f 的节奏配合（出兵优先）

- G0 期：采集力 100% 投入出兵循环，0 金农。
- G1 期：粮破 1000 后 4f 重开步弓/掷矛/剑士训练，28% 金农与出兵并行（72% 采集力
  仍在出兵侧）。剑士若含金费且升城拖后，G1a 28% 可上调 30~32%。
- **用户指示**（模组升城 400 金就是故意拉长封建）："倾向于封建出兵，不要过早攒资源"
  ——故触发不与 4f 同线（原草案粮 ≥1000 会过早进入攒金期），改为军事人口达标优先。

### 实施代码（已写入 MimisoRules.per，替换原 4a 三条规则）

```lisp
; ---- 4a') 封建金农两段式·出兵优先 (2026-10-19, 方案A) ----
; 模组步弓/掷矛/长矛全肉木, 封建前期 0 金农, 木食全力暴兵;
; 官方"起靶场加金农"(gatherers.per L88-118, 为原版45金弩手调校)
; 彻底压掉。升城堡 400 金是故意的高门槛 —— 封建以出兵为主,
; 攒金窗口越晚越好, 由 goal 锁存触发:
;   1) military-population >= 24   封建兵出够规模, 才开始攒钱升城
;   2) current-age-time >= 600     封建满10分钟兜底(被压制时兵上
;                                  不去规模, 保证不会永远不升城)
;   3) total-gold-amount >= 400    金已攒够(市场/遗迹), 直接进档
; goal 锁存的意义: 4f 重开训练花粮导致 total-food 回落、或兵被杀
; 导致 military-population 回落, 都不会把金农翻回 0 造成采集震荡
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank no)
=>
    (set-strategic-number sn-wood-gatherer-percentage 48)
    (set-strategic-number sn-food-gatherer-percentage 52)
    (set-strategic-number sn-gold-gatherer-percentage 0)
    (set-strategic-number sn-stone-gatherer-percentage 0)
)
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank no)
(or	(military-population >= 24)
(or	(current-age-time >= 600)
	(up-compare-goal total-gold-amount >= 400)))
=>
    (set-goal mimiso-goldbank yes)
)
; G1a: 锁存后冲金 —— 升城400金 + 铁匠铺150-275金; 若剑士线含金费
; 且升城明显拖后, 此档 28% 可上调 30~32%
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank yes)
    (up-compare-goal total-gold-amount < 850)
=>
    (set-strategic-number sn-wood-gatherer-percentage 35)
    (set-strategic-number sn-food-gatherer-percentage 37)
    (set-strategic-number sn-gold-gatherer-percentage 28)
    (set-strategic-number sn-stone-gatherer-percentage 0)
)
; G1b: 850金后回落, 富余转木食
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank yes)
    (up-compare-goal total-gold-amount >= 850)
=>
    (set-strategic-number sn-wood-gatherer-percentage 42)
    (set-strategic-number sn-food-gatherer-percentage 46)
    (set-strategic-number sn-gold-gatherer-percentage 12)
    (set-strategic-number sn-stone-gatherer-percentage 0)
)
; 进城堡复位, 交回 4b 城堡档 (帝王由 4c 管)
(defrule
(or	(current-age == castle-age)
	(current-age == imperial-age))
=>
    (set-goal mimiso-goldbank no)
)
```

文件头部 defconst 区追加：

```lisp
(defconst mimiso-goldbank 3030)   ; 封建金农锁存位 (3020-3029 已占用, 3030 起空闲)
```

### 代价与权衡

- **铁匠铺科技延后**：G0 期无金进账，150~275 金的封建铁匠科技要等 G1。escrow 会自动
  排队，进 G1 后一次补齐。换来 G0 步弓产量最大化。
- **剑士线金耗**：若模组剑士含金费，G1a 的 28% 余量可能偏紧，可上调到 30~32% 观察。
- villager ≥18 下限删除：少农民窗口（被打压时）也保持 0/28 结构，官方 13~15% 不再漏进来。

## 5. 方案 B（简化）：村民数阈值，不用 goal

```
封建 villager < 26 → 金 0%
封建 villager ≥ 26 → 沿用现 28%/12% 两档
```

- 优点：不占用 goal 号，无锁存逻辑，改动量最小。
- 缺点：村民增长慢时金迟迟不开工，升城拖后；被杀农民跌破 26 时金农短暂回撤（自愈，
  无害但颠簸）。阈值可按实测 24~28 之间调。

## 6. 共同收尾（两方案通用）

1. 原 4a 三条规则删除或注释（避免同 tick 先 28% 后 0% 的无序覆盖）。
2. **4i 已随实施更新**：其封建段数值原按旧 4a 第二档（金 16→14%）调校，会与新 G1a
   的 28% 冲突（马轭一完成攒金速度腰斩）。已按 G1a(35/37/28) 基准平移：马轭
   35/33/32、重犁 35/29/36（每完成一档食-4金+4）。城堡/帝王段不动。
   其前置 `total-gold-amount >= 400` 在新模型下必然已锁存（G0 期金摸不到 400），
   窗口天然只出现在 G1。
3. **4d 市场补金保留**：它要求 `research-available castle-age` 才启动，恰好落在 G1
   冲 400 金的窗口，与两段式互补。
4. 城堡 4b / 帝王 4c 不动（城堡有金单位/科技需求）。后续可选：确认弩手 4002 实际费用，
   若同样免金，可评估城堡档 24% → 18%。

## 7. 验证方法

1. 打一局到封建：G0 期金矿上应始终无农民（或 ≤1 人过渡），AI 持续暴兵。
2. 军事人口到 24（或封建满 10 分钟 / 金到 400）后金农出现，数量 ≈ 28% × 村民数
   （25 农 ≈ 7 人）。
3. 对比旧版录像的封建时段金矿累计采集量、封建兵力峰值与升城时间：预期封建兵力
   更高、升城略晚（可接受，模组本意即拉长封建）。
4. 若升城明显拖后：military-population 触发线 24 降 20，或封建兜底 600 秒降 480。

## 8. 附：官方 gatherers.per 关键规则摘录

- L88-108（r-flush）：封建 ≥1 靶场 → 48/37/15/0（起靶场加金农主源头）
- L109-118：≥2 靶场 + 铁匠铺 → 40/44/16/0
- L182-214（sk-var 同构）：≥1 靶场 → 50/50/**0**（掷矛策略反而 0 金）
- L307-315（a-rush 城堡期）：≥2 靶场 + TC → 40/37/**23**/0

即官方逻辑里"靶场→金农"只对**弓兵策略**成立（原版弓要金），掷矛策略同条件给 0 金——
模组全肉木弓体系下，方案 A 相当于把弓兵策略的封建金农行为对齐到官方掷矛策略的形状，
再叠加升城攒金窗口。

## 9. 追加：封建兵营空转修复（2026-10-19，MimisoRules 5d）

### 现象

AI 打封建叉弓（长矛+步弓）常先起 2 个兵营，但兵营不出叉叉，木材白花。

### 根因（官方链核查）

| 环节 | 事实 | 出处 |
|---|---|---|
| 兵营来源 | 4g 余木补军事建筑（军少<15 + 余木≥200 + 兵营<3），封建叉弓局必触发 | MimisoRules 4g |
| 长矛训练 | 挂 `trainpike` goal，官方 30+ 条触发规则**全是反应式**（敌骑进镇/敌方马厩/军事劣势/敌方有塔等），每扫描先被 units.per 开头 `(true)` 规则重置为 no | units.per L4749-5300 |
| 触发条件 | 封建步弓对射局（无骑兵侦察、无塔、无劣势标记）一条都不触发 → trainpike 全程 no → 长矛产量 0 | 同上 |
| 剑士训练 | trainchamp 被 4f 重开 yes，但 militia-line（原版 ID 74/75/77…）费用含金：G0 期 0 金农、G1 期金走 escrow 攒升城，`can-train militiaman-line` 常假 | units.per L13361-13368 |
| siegereq | 封建期恒 yes（init.per `current-age <= feudal-age` 即置 yes），不是瓶颈 | init.per L4170-4179 |

结论：兵营里剑士出不了（缺金）、长矛没目标（trainpike 不触发）→ 空转。

### 修复（已写入 MimisoRules.per 5d）

模组长矛线全肉木（封建主力三选一），兵营既然起了就该出兵。封建期绕过
trainpike 反应式与 siegereq 直训长矛，上限 25 防过量挤占人口；城堡起交回
官方 trainpike 链（长枪/戟兵与反制条件接管）。

```lisp
(defrule
    (current-age == feudal-age)
    (up-compare-goal milunits != no)
    (population-headroom > 0)
    (unit-type-count-total spearman-line < 25)
    (can-train spearman-line)
=>
    (train spearman-line)
)
```

### 联动

- 4g 兵营加建**保留**：修后兵营有产出（长矛），2-3 个兵营与"封建暴兵"定位一致。
- 与金农方案 A 互补：长矛吃肉木，正好消化 G0 的 48/52 木食产能；攒金窗口（G1）不受影响。
- 与 4f 分工：4f 管靶场线（步弓/掷矛）+ 剑士链重开；5d 管兵营长矛线。

### 验证

1. 封建叉弓局：兵营应持续吐长矛（早期长矛兵，3001 研究后自动变长矛兵）。
2. 长矛数量封顶 25，不会挤占步弓人口。
3. 若体感长矛过多/过少：调上限 25（官方肉盾档参考 6~20）。

> **10-19 修订（5d v3）**：上方"封建无条件直训上限 25"实测在步弓对射局也一直
> 出叉，挤占弓手人口，偏离叉弓本意。已改为**反骑定位**：仅当敌方有骑兵
> （斥候/骑士/骆驼）才出叉，上限 15；同时 4g 兵营加建受"敌方有骑兵 / 己方要
> 步兵"门控，步弓对射局不白建兵营。详见第 11 节。

---

## 10. 禁用黑暗 rush（drush）

### 背景

用户反馈 AI 不再进行黑暗 rush。官方 Promi 在 `init.per`/`interaction.per` 会
在特定条件下把 `strategy` 设为 `drush`，`buildings.per` 据此黑暗时代建兵营，
`units.per` 据此出民兵/长矛。这些规则都在官方文件（只读），无法直接删除。

### 修复（MimisoRules.per 第 0 节 + units.per 注释）

1. **策略重定向**（MimisoRules，加载在最后，每 tick 覆盖）：
   `goal strategy drush` → `set-goal strategy usual`，同时 `set-goal drushmicro no`。
   官方所有 drush 规则的触发条件（`goal strategy drush` / `drushmicro yes`）
   恒不满足，黑暗兵营、黑暗产兵、drush 微操全部失效，无需改官方文件。

2. **模组自有 drush 长矛规则注释**：`units.per` L7860-7875 原是模组把官方 drush
   民兵改为长矛的适配规则，现已整段注释（保留作历史参考）。

```lisp
; MimisoRules 第 0 节
(defrule
    (goal strategy drush)
=>
    (set-goal strategy usual)
    (set-goal drushmicro no)
)
```

### 说明

- `usual`（=100）是 Promi 默认爆兵/封建战策略，重定向后 AI 走常规流程。
- 官方 `champi-line` drush 规则、`drushmicro` 农民规则仍在 `units.per`，但
  因 strategy 已被重定向，条件恒假，成为死代码，无需触碰（避免误改官方逻辑）。

---

## 11. 修封建长矛刷屏（5d v3 + 4g 兵营门控）

### 现象

5d v2 把长矛改成"封建无条件直训上限 25"后，步弓对射局也一直出叉，挤占弓手
人口；同时 4g 在步弓局也白建 2 个兵营。用户反馈"2 兵营一直出叉"。

### 根因

长矛本是**反骑兵**单位，步弓对射局敌方无骑兵，出叉是浪费人口与产能。5d v2
去掉了反骑定位，变成无条件常备兵，过度生产。4g 兵营加建也没有"是否需要
步兵/反骑"的判断。

### 修复

1. **5d 改反骑定位**：仅当敌方有骑兵（斥候/骑士/骆驼）才训练长矛，上限 25→15。
   步弓对射局不出叉。

2. **4g 兵营加门控**：兵营加建增加条件 `(or (goal trainchamp yes) 敌方有骑兵)`。
   步弓对射局既不要步兵也无骑兵可反 → 不建兵营，木材留给靶场/升城。

```lisp
; 5d 封建长矛反骑直训
(defrule
    (current-age == feudal-age)
    (up-compare-goal milunits != no)
    (population-headroom > 0)
    (unit-type-count-total spearman-line < 15)
    (can-train spearman-line)
    (or (players-unit-type-count any-enemy scout-cavalry-line >= 1)
    (or (players-unit-type-count any-enemy knight-line >= 1)
        (players-unit-type-count any-enemy camel-line >= 1)))
=>
    (train spearman-line)
)

; 4g 兵营加建（节选，新增最后一个 or 条件）
(defrule
    ...
    (building-type-count-total barracks < 3)
    (can-build barracks)
    (or (goal trainchamp yes)
    (or (players-unit-type-count any-enemy scout-cavalry-line >= 1)
    (or (players-unit-type-count any-enemy knight-line >= 1)
        (players-unit-type-count any-enemy camel-line >= 1))))
=>
    (build barracks)
)
```

### 预期行为

| 对局 | 敌方骑兵 | 兵营 | 长矛 |
|---|---|---|---|
| 步弓对射 | 无 | 不建（4g 门控） | 不出（5d 门控） |
| 反骑（敌斥候/骑士） | 有 | 建 | 出，上限 15 |
| 步兵局（trainchamp yes） | — | 建 | 不出（除非敌方也有骑兵） |

### 验证

1. 步弓对射局：封建不应出现叉叉，兵营数量≤官方策略驱动值（通常 0-1）。
2. 敌方出斥候/骑士后：兵营开始吐长矛，数量缓慢爬升到 ~15 后停。
3. 长矛上限 15 可调（反骑肉盾参考 10-20）。

## 12. 追加：冲城末段提速（2026-10-19，MimisoRules 4j，修"卡资源硬等时代"）

### 现象

封建后期 AI 常卡在 ~1000F / 200G（数字举例）干等升城，期间出兵断续。

### 根因（官方链核查）

| 环节 | 事实 | 出处 |
|---|---|---|
| 升城点击路径 | 中等及以上难度不走 researches.per 直点规则（被 `#load-if-not-defined DIFFICULTY-MODERATE` 排除），走 escrow 路径：`escrow-flag==1` + `can-research-with-escrow castle-age` | researches.per L99-120、escrow.per L24-32 |
| 排队条件 | escrow 排队规则要求军事优势≥1 / 人口≥36 / 粮≥castle-f2 且（金≥200 或 ≥3 金矿工 / ≥6 贸易车）等，条件不齐 escrow-flag 不置位——资源够了也可能不点 | escrow.per L786-815 |
| 卖资源停手线 | 官方市场为升城卖余粮/余木在 castle-gold=200 停手（原版费用），模组要 400G，200G 后只剩金农涓流 | trade.per（4d 已补到 400，但需市场存在） |
| 涓流 + 震荡 | 200→400G 靠 28% 金农涓流；期间 4f 在 1000 粮线上下重开/重置训练，出兵断续 | MimisoRules 4f |

### 修复（已写入 MimisoRules.per 4j，两条小规则，均只在金农锁存后生效）

1. **金 <400 时金农 28%→40%**（木 28/食 32/金 40）：缩短涓流窗口，木食仍保 60% 出兵。
2. **库存够 800F+400G 立即 `research castle-age`**：绕过 escrow 排队条件，消除"资源够了还干等"的尾部延迟。

```lisp
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank yes)
    (research-available castle-age)
    (gold-amount < 400)
=>
    (set-strategic-number sn-wood-gatherer-percentage 28)
    (set-strategic-number sn-food-gatherer-percentage 32)
    (set-strategic-number sn-gold-gatherer-percentage 40)
    (set-strategic-number sn-stone-gatherer-percentage 0)
)
(defrule
    (current-age == feudal-age)
    (goal mimiso-goldbank yes)
    (can-research castle-age)
=>
    (research castle-age)
)
```

### 安全性

- G0 不受影响：两条都挂 `mimiso-goldbank yes`，前期仍 0 金农全力出兵。
- escrow 无残留风险：escrow.per 开头 `(true)` 规则每 tick 全量重置（release + 清零），直点不留脏账。
- 双路径无冲突：官方先点成功则 `can-research` 变假，本规则同 tick 自动空转。
- 帝王升代未动（1600F/800G 由官方 escrow 路径自理，如后续观察到同类卡顿再照此扩展）。

### 验证

1. 封建叉弓局 G1 期：金到 400 前金农应明显多于 G1a 的 28%（≈40% × 村民数）。
2. 金粮凑够的当刻 AI 应立即点升城，不再有"满资源干等"的录像片段。

---

## 13. 鼓励封建出肉马（斥候线）（2026-10-19，MimisoRules 4g 马厩 + 5e）

### 现象

AI 封建时代基本不出肉马（斥候骑兵线）。用户要求鼓励封建出肉马。

### 根因（官方链核查）

| 环节 | 事实 | 出处 |
|---|---|---|
| 训练链 | 封建肉马只走 `s-flush`（scout-rush）策略：`set-goal trainhussar yes` → `units.per` L13781 训练 | units.per L9089-9111, L13781-13788 |
| 策略门槛 | 非 s-flush 策略下 `trainhussar` 恒 no → 封建无训练规则触发 | 同上 |
| 马厩建造 | `number-stables` 在弓/步策略下为 0，官方 `buildings.per` 不建马厩；模组 4g 马厩规则也被 `stable < number-stables` 卡死 | const.per（各策略 number-stables） |
| 成本 | 原版肉马 80F/20G 耗金，但**模组改为肉木不耗金**，G0 金锁不构成阻碍 | 模组 dat |

双重压制：既不建马厩，也无训练规则 → 封建零肉马。

### 修复（MimisoRules 4g 马厩 + 5e 直训）

1. **4g 马厩封建期放开**：封建时代建马厩不再受 `number-stables` 限制（上限 2），城堡时代仍服从官方策略的 `number-stables`（骑士/骆驼由官方决定）。

2. **5e 封建肉马直训**：封建期有马厩即直训 `scout-cavalry-line`，上限 6（参照官方 `scrush-cap=5`）。城堡起交回官方 `trainhussar` 链（轻骑兵/匈牙利轻骑兵由官方反制条件接管）。

```lisp
; 4g 马厩（节选，封建期放开 number-stables）
(defrule
    ...
    (building-type-count-total stable < 2)
    (or (current-age == feudal-age)
        (building-type-count-total stable < number-stables))
    (can-build stable)
=>
    (build stable)
)

; 5e 封建肉马直训
(defrule
    (current-age == feudal-age)
    (up-compare-goal milunits != no)
    (population-headroom > 0)
    (building-type-count-total stable >= 1)
    (unit-type-count-total scout-cavalry-line < 6)
    (can-train scout-cavalry-line)
=>
    (train scout-cavalry-line)
)
```

### 说明

- 肉马不耗金，与 G0 金锁（0 金农）不冲突，吃肉木正好消化封建产能。
- 肉马克制步弓/掷矛，与叉叉（反骑）形成互补：敌方骑兵→叉叉，敌方步弓→肉马。
- 与官方 `trainhussar` 训练规则并行不冲突：`can-train` 处理资源/前置，双方都可能触发但不重复生产。
- 上限 6 可调：肉马肉盾参考 4-8；若体感过多/过少调此值。

### 验证

1. 封建局应建起 1-2 座马厩（余木≥200 + 军事人口<15 时）。
2. 马厩建成后应开始出斥候，数量缓慢爬升到 ~6 后停。
3. 城堡时代后肉马训练交回官方 `trainhussar` 链，本规则自动失效（`current-age != feudal-age`）。

---

## 14. 升城费改回官方后的规则作废与阈值归位（2026-10-19）

### 背景

用户把升级时代的费用改回官方（城堡时代 200G，不再是模组的 400G）。此前针对 400G 升城费调校的规则需要作废或调整。

### 作废（整段注释）

| 规则 | 原作用 | 作废原因 |
|---|---|---|
| **4d** 市场卖资源停手线 200→400 | 城堡需 400G，官方停手线 200 不够，延到 400 | 城堡回 200G，官方 `castle-gold=200` 已正确 |
| **4j** 冲城末段提速 | 金<400 时金农提至 40%；`can-research castle-age` 直点绕过 escrow | 200G 升城官方 escrow 路径能正常处理，无需提速 |

### 阈值归位（400 → 200）

| 位置 | 原条件 | 现条件 | 说明 |
|---|---|---|---|
| 4a G0→G1a 触发 | `total-gold-amount >= 400` | `>= 200` | 升城费从 400G 回到 200G |
| 4i 农田科技前置 | `total-gold-amount >= 400` | `>= 200` | 匹配 G1a 入门阈值（封建/城堡各两条） |

### 保留不变

- **4a G0/G1a/G1b 整体策略**：封建前期 0 金农全力出兵、军事人口≥24 / 封建满10分钟 / 金够升城费才进攒金档的设计仍有效，只是金阈值数字归位。
- **4b/4c**（城堡/帝王金农档）、**4e**（贸易车）、**4f**（余粮重开训练）、**4g**（军事建筑）、**4i**（农田科技减食农）均与升城费无直接关系，保留。
- **5d/5e**（长矛/肉马直训）与升城费无关，保留。

### 验证

1. 封建局：金农仍在 G0（0%）直到军事人口≥24 或 10 分钟或金≥200，之后进 G1a（28%）。
2. 市场卖粮木：官方 200G 停手线生效（不再卖到 400）。
3. 升城：官方 escrow 路径处理，金够 200G 且条件满足时自动点升城。
