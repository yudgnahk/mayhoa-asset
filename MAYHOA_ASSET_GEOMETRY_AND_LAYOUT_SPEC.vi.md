# Mayhoa — Asset Geometry, Anchor & Layout Spec

**Ngôn ngữ:** Tiếng Việt · [English](MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md)

**Status:** Canonical geometry/layout contract for asset audit and production  
**Project:** Mayhoa  
**Scope:** Master assets, multi-stage assets, runtime anchor metadata, normalization/QC  
**Related specs:** `MAYHOA_ART_STYLE_SPEC.vi.md`, `FARM_ASSET_GENERATION_PLAN.vi.md`, `FARM_REMAINING_PLANT_ASSET_PLAN.vi.md`, `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md`

---

## Trạng thái và quan hệ với tài liệu khác

Đây là **tài liệu geometry active và có quyền ưu tiên cao nhất** trong repo (xem thứ tự precedence do chính file này định nghĩa ở §18: geometry spec này > species-specific lifecycle spec > `FARM_ASSET_GENERATION_PLAN.vi.md` > `MAYHOA_ART_STYLE_SPEC.vi.md` > runtime JSON/README hiện có).

Tài liệu này bổ trợ (không thay thế) `MAYHOA_ART_STYLE_SPEC.vi.md` (chỉ quy định visual style, không quy định hình học) và `FARM_ASSET_GENERATION_PLAN.vi.md` (roadmap/taxonomy/thứ tự phase, không phải nguồn số đo canvas/anchor chính xác). Việc áp dụng thực tế các con số ở đây cho `masters/` hiện có được ghi lại trong `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md` (đã thực thi 2026-08-26); §20 của chính file này chứa baseline đo đạc và kết quả post-normalize.

---

## 1. Mục đích

Tài liệu này khóa các quy tắc hình học dùng chung cho asset Mayhoa để:

- mọi asset cùng loại có canvas và gameplay anchor nhất quán;
- các stage lifecycle không bị center riêng theo bounding box;
- animation chuyển stage không bị nhảy gốc / nhảy vị trí;
- master asset và runtime sprite dùng cùng một semantic anchor;
- normalize asset bằng transform raster không làm thay đổi artwork;
- có một checklist duy nhất để audit lại toàn bộ asset ở session sau.

Tài liệu này **không thay thế art-style spec**. Nó chỉ là source of truth cho:

- canvas;
- tọa độ anchor;
- scale/progression;
- transparent padding;
- placement geometry;
- normalization;
- QC hình học.

---

## 2. Nguyên tắc quan trọng nhất

### 2.1 Gameplay anchor quan trọng hơn visual center

Với asset có điểm tiếp xúc gameplay rõ ràng, **không center asset theo bounding box**.

Điểm cố định phải là semantic anchor:

- tree / perennial: điểm gốc cây tiếp xúc mặt đất;
- crop / herb: điểm footprint đặt lên soil;
- aquatic crop: root/base hoặc waterline anchor theo spec của pack;
- animal đứng trên đất: foot/contact anchor;
- object đặt trên mặt phẳng: contact/base anchor;
- asset không có contact point rõ ràng mới được dùng visual-center/pivot phù hợp.

Rule `object centered` trong art-style spec chỉ là preference cho isolated composition. Với asset có gameplay anchor, **geometry spec này ưu tiên cao hơn**.

### 2.2 Một lifecycle pack phải dùng một anchor duy nhất

Nếu một species có nhiều stage:

- tất cả stage dùng cùng canvas;
- cùng tọa độ anchor tuyệt đối trong master canvas;
- không tính anchor riêng cho từng stage ở runtime để che lỗi master;
- cây/crop phải phát triển ra khỏi anchor cố định đó.

Runtime có thể lưu anchor normalized, nhưng master artwork vẫn phải align đúng trước.

### 2.3 Không normalize bằng cách align top

Với cây/crop growth:

- top của foliage phải được phép thay đổi theo growth;
- bottom/root/contact point mới là điểm khóa;
- nếu top của mọi stage bằng nhau nhưng root khác nhau thì asset **FAIL**.

---

## 3. Hệ tọa độ chuẩn

Master raster dùng hệ tọa độ ảnh thông thường:

```text
(0,0) --------------------> +X
  |
  |
  |
  v
 +Y
```

- `(0,0)` ở góc trên-trái;
- X tăng sang phải;
- Y tăng xuống dưới;
- pixel coordinate được hiểu theo canvas master;
- khi nói `root=(x,y)`, đây là tọa độ trên raw PNG master, không phải tọa độ sau khi PixiJS tự bù anchor.

### 3.1 Absolute anchor và normalized anchor

Master QC dùng absolute pixel coordinate:

```text
anchor_px = (x, y)
```

Runtime metadata nên dùng normalized coordinate:

```text
anchor_norm = (x / canvas_width, y / canvas_height)
```

Ví dụ tree master 1024×1024 với root `(512,970)`:

```text
anchor_px   = (512, 970)
anchor_norm = (0.5, 0.947265625)
```

Không làm tròn master anchor khi QC. Runtime có thể serialize số thực với precision đủ cao.

---

## 4. Canvas master theo asset class

Các target hiện tại từ production plan:

| Asset class | Master canvas target | Ghi chú |
|---|---:|---|
| Small crop / weed / pest | `512×512` | crop pack hiện tại chủ yếu dùng 512 |
| Medium crop / herb | `768×768` target mới | cần audit các pack cũ 512 trước khi migrate |
| Aquatic crop | `768×768` | lotus LOCKED `1024×1024` — xem §5.4 |
| Normal tree / perennial / animal-sized farm asset | `1024×1024` | canonical cho fruit tree / coffee; default master target |
| Tall / special tree | `1024×1280` nếu thật sự cần | toàn bộ stage cùng species phải cùng canvas; coconut đã chốt KHÔNG dùng — xem §5.2 |
| Tool / small isolated icon | `512×512` | anchor tùy semantic |
| Large hero asset | `1536+` chỉ khi explicit | không dùng làm runtime trực tiếp |

### 4.1 Không trộn canvas trong cùng một lifecycle

Ví dụ không được:

```text
stage-01 = 1024×1024
stage-02 = 1024×1024
stage-03 = 1254×1254
stage-04 = 1024×1024
stage-05 = 1024×1024
```

Nếu normalize, normalize toàn pack về một canonical canvas.

### 4.2 Generator output không phải canonical canvas

Đo thực tế (2026-08-26) cho thấy pipeline generation thường xuất:

- `1122×1402` — mango, pomelo, lemon, star-apple;
- `1254×1254` — lychee, rambutan, coconut, lotus.

Không size nào ở trên là canonical. Mọi pack generate mới phải được resample + align về canonical canvas/anchor trước khi được coi là master hoàn chỉnh. Không lock spec theo size mà generator tình cờ xuất ra.

---

## 5. Canonical anchor theo asset class

### 5.1 Normal tree / perennial — LOCKED

Canvas:

```text
1024×1024
```

Canonical root/contact anchor:

```text
root_px   = (512, 970)
root_norm = (0.5, 0.947265625)
```

Ý nghĩa:

- X ở giữa gameplay footprint;
- Y là lowest/root contact point;
- còn `53 px` transparent padding dưới root (`1023 - 970 = 53`);
- foliage/canopy phát triển lên trên và sang hai bên;
- không move root để center canopy.

Coffee đã được dùng làm calibration cho anchor này và phải được audit lại cùng toàn bộ tree pack ở session tiếp theo.

Các species trong `FARM_REMAINING_PLANT_ASSET_PLAN.vi.md` mặc định dùng contract này nếu giữ canvas `1024×1024`:

- `coffee`;
- `dragon-fruit` nếu support post/trellis và toàn bộ plant envelope vẫn fit an toàn trong square master;
- `rubber` nếu không cần tall canvas sau cross-species audit.

`dragon-fruit` là **special-structure plant**: root/base anchor của plant + support system phải cố định, nhưng chiều cao của support post cố định **không được dùng làm growth metric** cho plant.

Trạng thái đo 2026-08-26 — `dragon-fruit`: pack nhất quán nội bộ (root ≈ `(500.5, 987.5)`, delta ≤ 1 px) nhưng lệch canonical anchor `(-11.5, +17.5)`. Visible height stage-03 là 962 px nên **không thể translate thẳng** về `(512, 970)` mà không vỡ top margin 24 px; phải scale toàn pack `×0.98` quanh root rồi translate (xem fix checklist).

### 5.2 Tall / special tree — PROVISIONAL

Nếu thật sự dùng canvas `1024×1280`, giữ cùng logic bottom padding 53 px:

```text
root_px = (512, 1226)
```

Tức:

```text
root_y = canvas_height - 54
```

Đây là provisional rule cho tới khi audit rubber/tall trees hoàn tất.

Ứng viên còn lại cho tall/special canvas:

- `rubber` — có thể cần tall canvas nếu mature/tapping stage vượt safe envelope của `1024×1024`.

`coconut` đã được đo (2026-08-26) và **chốt dùng square `1024×1024`, root `(512, 970)`**. Pack hiện tại là `1254×1254`, contactY = 1236 (Δ0), rootX ≈ 646 (Δ1.1 px) — nhất quán nội bộ nhưng sai canvas, bottom padding chỉ 17 px và stage-05 chỉ còn 6 px top margin. Resample toàn pack `×0.768` về 1024 cho stage-05 visible height ≈ 946 px — vẫn là tallest member của remaining tree pack, không cần tall canvas.

Không tự động chuyển một species sang `1024×1280` chỉ vì artwork hiện tại cao. Chỉ dùng tall canvas nếu sau cross-species audit, relative world scale hợp lý nhưng square master không còn đủ safe margin.

### 5.3 Crop / herb — LOCKED (bottom-anchor, 2026-08-26)

Legacy Phase 2/3 (ĐÃ THAY THẾ, giữ làm lịch sử):

```text
master_canvas ≈ 512×512
placement_anchor_norm ≈ (0.5, 0.684)
placement_anchor_px   ≈ (256, 350)
```

Reference legacy này từng tồn tại trong:

- `masters/farm/crops/README.vi.md` — đã cập nhật;
- `runtime/core_crops_v01.json` — atlas đã bị xoá (2026-09-07);
- `runtime/herb_crops_v01.json` — atlas đã bị xoá (2026-09-07).

Cả hai atlas trên đã được gộp thành `runtime/farm_crops_v01.json` (xem §13.2).

**Contract cuối (rev 2, cùng ngày): crop là sprite độc lập bottom-anchor giống tree.**

Quá trình chốt: (1) diễn giải "crop không cần cùng contactY" sai — chân crop stage lớn lòi dưới soil plate; (2) phương án base-align tại `(256, 350)` cũng sai nốt — điểm đó là **mép trước** của plate (plate chiếm y 157–360), trong khi calibration sheet cho thấy cây phải đứng ở **tâm plate**; và nếu giữ kiểu bake 1:1 theo tile thì base tại tâm plate chỉ cho ~236 px chiều cao — không đủ cho class M. Do đó:

- crop là sprite độc lập, bottom-anchor cùng triết lý tree;
- canvas `512×512`, root `(256, 458)` = `(0.5, 0.89453125)` — 54 px bottom padding, cùng convention tree;
- contactY = 458, Δ0 xuyên 5 stage; max visible height = `458 − 24 = 434 px`;
- engine ghim crop root vào **tile plant point = tâm soil plate `(256, 260)` ≈ `(0.5, 0.508)`** trong hệ tọa độ soil tile 512;
- align X: thân đơn/bụi (rice, corn, carrot) dùng bottom-band centroid; rosette/bush (culantro, tonkin-jasmine, mint) dùng **bbox center** (§7.1);
- QC bắt buộc composite check lên soil tile: chân cây tại tâm plate, không lòi dưới plate.

`placementAnchor` đã đổi `(0.5, 0.684)` → `(0.5, 0.89453125)`. Từ 2026-09-07 giá trị này nằm trong `runtime/farm_crops_v01.json` (ghi làm tròn 6 chữ số: `(0.5, 0.894531)`), thay cho `core_crops_v01.json` / `herb_crops_v01.json` đã bị xoá. **Code game đọc anchor này cần được kiểm tra lại điểm ghim trên tile (tâm plate).**

Session audit sau phải xác minh:

- raw PNG có thật sự cùng footprint/contact anchor không;
- metadata runtime có phản ánh master thật không;
- Phase 2/3 512 canvas có tiếp tục canonical hay migrate sang target 768 cho medium crop.

### 5.4 Aquatic crop — LOTUS LOCKED; các species còn lại MUST AUDIT

Default master:

```text
768×768
```

Lotus có thể:

```text
1024×1024
```

Semantic anchor phải là một trong:

- common root/base point;
- common waterline point;
- hoặc một pack-specific gameplay anchor được document rõ.

Tất cả 5 stage của cùng aquatic species phải dùng **cùng exact anchor**.

Không khóa pixel coordinate chung cho tất cả aquatic assets trước khi audit, vì lotus, water mimosa và water spinach có cấu trúc mặt nước khác nhau.

Semantic anchor bắt buộc cho ba species còn lại:

| Species | Canvas target | Canonical anchor semantic | Growth direction chính |
|---|---:|---|---|
| `lotus` | `768×768`, có thể `1024×1024` | common root/base hoặc common waterline point đã chọn cho cả pack | upward + radial leaf spread |
| `water-mimosa` | `768×768` | common waterline/root placement point | horizontal spread |
| `water-spinach` | `768×768` | common waterline/root placement point | horizontal spread |

Rule aquatic quan trọng:

- không yêu cầu ba species dùng cùng **pixel coordinate** trước khi audit;
- nhưng mỗi species phải có một exact anchor duy nhất xuyên suốt 5 stage;
- sau khi Wave B audit xong, nên khóa một aquatic placement convention chung nếu neutral water tile cho phép;
- không bake water surface/ripple/pond edge vào master để “giả” waterline alignment.

Trạng thái đo 2026-08-26 — `lotus` (đã LOCKED):

- pack hiện tại `1254×1254` (sai canvas policy);
- contactY = 1185–1187 (Δ2 px, chấp nhận được);
- rootX bottom-band dao động 585–647 — phần lớn do heuristic không hợp morphology radial (xem §7.1), phải align thủ công;
- spread progression 0.25 / 0.64 / 0.81 / 0.95 — gần khớp Profile D.

Quyết định: lotus **LOCKED `1024×1024`, anchor `(512, 970)`** theo cùng bottom-padding convention của tree. Resample `×0.835` + align root thủ công từng stage. `water-mimosa` / `water-spinach` **LOCKED `768×768`, anchor `(384, 728)`** — trong đó `728 = round(768 × 970/1024)`, đúng tỷ lệ bottom-padding convention của tree/lotus. Align X dùng **bbox center** (Profile E), **không** dùng bottom-band centroid.

Trạng thái đo 2026-09-05 — cả hai pack aquatic horizontal **đã normalize xong và đạt chuẩn**: canvas `768×768` đồng nhất 5/5 stage, RGBA8, contactY = 728 (Δ0), bbox center X = 383.0–384.5 (tâm canvas 383.5, Δ ≤ 1.5 px), margin L/R đối xứng trong 1–2 px. Số đo per-stage ở Appendix B của `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md`.

> **CẢNH BÁO — KHÔNG normalize lại `water-mimosa` / `water-spinach`.**
> Hai pack này đã đạt chuẩn. Nếu chạy `tools/normalize_pack.py` lên chúng mà **không có `--rootx` override**, bottom-band heuristic sẽ **phá alignment đang đúng**: rootX bottom-band của `water-mimosa` trải `376.9–474.0` (Δ 97 px) vì morphology aquatic-horizontal, nên script sẽ dịch stage s02 khoảng **−90 px**. Đây đúng là ca hỏng heuristic mà §7.1 đã mô tả và gọi tên `water-mimosa`. `rootX` bottom-band của 2 pack này **chỉ tham khảo**, không phải số PASS/FAIL — số PASS/FAIL là bbox center X.

### 5.5 Animal / fish / dragon / object

Không ép mọi asset dùng tree root.

Anchor phải theo semantic placement:

- land animal: foot/base contact;
- fish: gameplay pivot phù hợp với swimming/rotation;
- dragon/flying asset: pivot theo body mass / animation rig contract;
- tool/icon: visual pivot nếu không có world-contact semantic.

Khi một class được production hóa thành pack, phải bổ sung exact canonical anchor cho class đó vào doc này.

---

## 6. Transparent background và alpha contract

Tất cả isolated master sprite phải:

- background transparent thật;
- không matte màu đen/trắng;
- không scene background;
- không UI/text/watermark;
- không bake soil/ground tile/pond edge/pond surface trừ khi asset spec explicit yêu cầu;
- không bake decorative clutter không thuộc object.

### 6.1 Alpha threshold dùng cho geometry QC

Để tránh anti-alias fringe ảnh hưởng bbox, geometry QC nên dùng:

```text
alpha >= 24 / 255
```

Đây là threshold đang tương thích với logic playground hiện tại.

QC phải ghi rõ threshold nếu dùng giá trị khác.

### 6.2 Opaque bounding box

Với threshold `alpha >= 24`, đo:

```text
minX, minY, maxX, maxY
visibleWidth  = maxX - minX + 1
visibleHeight = maxY - minY + 1
```

Đối với grounded asset:

```text
contactY = maxY
```

`contactY` của mọi stage trong cùng pack phải giống nhau sau normalize (crop: contactY = 458 — xem §5.3).

### 6.3 Master PNG format

- Master phải là RGBA8 (PNG colortype 6).
- Không dùng palette/quantized PNG (colortype 3) làm master; quantize chỉ được phép ở runtime asset.
- Known issue đã đóng (2026-08-26): `rice`, `corn`, `carrot` từng là palette PNG; cả ba đã thành RGBA8 sau crop base-align pass. Mọi pack mới bắt buộc RGBA8.

---

## 7. Root X phải đo từ base/contact band, không đo từ canopy

Không dùng center của toàn opaque bounding box để suy ra root X.

Với tree/perennial:

1. đo visible height;
2. lấy bottom band khoảng `2–3%` visible height, tối thiểu khoảng `6–20 px` tùy master size;
3. chỉ xét alpha pixel đủ threshold trong bottom band;
4. suy ra center/centroid của phần trunk/root contact;
5. align root X về canonical X.

Mục tiêu là align **gốc thân cây**, không align canopy.

Ví dụ lỗi cần tránh:

- canopy lệch trái -> center bbox lệch trái -> script dịch cả cây -> root bị lệch;
- canopy mở rộng theo stage -> bbox center đổi -> animation nhảy ngang.

### 7.1 Giới hạn của bottom-band heuristic

Bottom-band centroid chỉ tin cậy cho morphology thân đơn (tree / palm / trụ). Với morphology radial / rosette / multi-stem (lotus, culantro, water-mimosa...), centroid của bottom band dao động mạnh theo tán lá — đo được Δ 62–125 px dù artwork không hẳn sai vị trí. Với các species này:

- không dùng bottom-band centroid làm số PASS/FAIL tự động;
- đánh anchor thủ công (visual) hoặc dùng band cao hơn quanh cụm gốc;
- ghi rõ phương pháp đo trong audit report;
- **không chạy lại normalize bằng heuristic này lên pack đã align đúng bằng bbox center** — `water-mimosa` / `water-spinach` là ca cụ thể, xem cảnh báo ở §5.4.

---

## 8. Safe padding / breathing room

### 8.1 General rule

Artwork không được chạm canvas edge ở alpha QC threshold.

Recommended opaque safe margin:

```text
>= 24 px minimum
>= 32 px preferred
```

cho cạnh trái/phải/top ở master 1024 nếu morphology cho phép.

### 8.2 Grounded tree bottom padding

Normal tree 1024 dùng root `y=970`, nên có 53 px transparent area dưới contact point.

Không được kéo tree xuống tận row 1023 chỉ để tận dụng canvas.

### 8.3 Không crop để ép fit nếu làm mất artwork

Nếu mature stage vượt canvas:

ưu tiên theo thứ tự:

1. giảm toàn bộ species pack theo relative-scale hợp lý;
2. chọn tall/special canvas nếu spec cho phép;
3. regenerate nếu morphology sai;
4. không crop leaf/fruit/branch chỉ để pass size.

---

## 9. Scale và lifecycle progression

### 9.0 Core rule — same stage không có nghĩa same absolute height

Các species ở cùng `stage-03`, `stage-04`, `stage-05` **không bắt buộc có cùng pixel height**.

Cùng stage chỉ có nghĩa là mức trưởng thành/lifecycle tương đương trong species đó.

Ví dụ:

- coffee stage 05 vẫn phải thấp/compact hơn coconut stage 05;
- water-mimosa stage 05 có thể không cao hơn stage 04 nhiều, nhưng phải spread/dense hơn;
- dragon-fruit có support post cố định nên full bbox height có thể gần như không đổi trong một số stage, trong khi plant mass vẫn phát triển rõ.

Do đó geometry audit phải tách hai khái niệm:

```text
within-species progression = stage growth logic của chính species
cross-species world scale  = relative size hợp lý giữa các species
```

Không được normalize tất cả species về cùng một stage height chỉ để bảng số trông đều.

### 9.1 Dominant growth metric

Mỗi species phải có `dominantGrowthMetric` rõ ràng. Progression 5 stage phải tăng theo metric phù hợp morphology, không nhất thiết luôn là height.

Các metric có thể dùng:

- `visibleHeight` — tree/palm/trunk-driven plant;
- `canopySpread` — crown/canopy development;
- `plantEnvelope` — plant-only envelope khi có support cố định;
- `horizontalSpread` — aquatic/vine/creeping form;
- `density` — stem/leaf mass;
- `structuralComplexity` — branch/segment/stem count;
- composite metric nếu một species cần nhiều tín hiệu.

General lifecycle relation vẫn là:

```text
stage-01 < stage-02 < stage-03 < stage-04 < stage-05
```

nhưng dấu `<` áp vào **dominant growth metric / perceived maturity**, không phải ép mọi bbox dimension đều tăng.

### 9.2 Không chỉ scale cùng một artwork

Stage phải thay đổi cấu trúc thật.

Raster scaling chỉ được dùng để **normalize relative size sau generation**, không được dùng để giả tạo lifecycle bằng cách scale một hình duy nhất thành 5 stage.

### 9.3 Stage 05 phải không regress so với stage 04

Stage 05 không được regress về perceived maturity so với stage 04.

Với vertical tree/palm:

- stage 05 không nên thấp/nhỏ hơn stage 04 nếu không có species-specific reason;
- có thể scale stage 05 nhẹ nếu artwork/morphology vẫn đúng và không crop;
- nếu scale không đủ thì regenerate.

Với horizontal aquatic plant:

- stage 05 không bắt buộc cao hơn stage 04;
- nhưng horizontal spread, density hoặc harvestable plant mass phải bằng hoặc lớn hơn stage 04.

Với support-structure plant như dragon-fruit:

- support post có thể giữ nguyên;
- plant coverage/branching/segment mass quanh support phải tăng;
- không dùng fixed support height để kết luận progression PASS.

### 9.4 Recommended progression ratio profiles

Các ratio dưới đây là **audit/calibration bands**, không phải lý do để phá morphology. Ratio đo trên dominant growth metric và normalize theo stage 05 của **chính species đó**:

```text
stageRatio = dominantMetric(stage) / dominantMetric(stage-05)
```

#### Profile A — vertical tree / shrub

Dùng cho: `coffee`, `rubber` và major fruit tree khi phù hợp.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.35–0.45` |
| 02 | `0.55–0.65` |
| 03 | `0.75–0.88` |
| 04 | `0.90–0.98` |
| 05 | `1.00` |

Band stage-03 đã nới lên `0.88` (2026-08-26) vì coffee — calibration species — đo được `0.867`.

#### Profile B — palm / strong vertical special tree

Dùng cho: `coconut`.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.35` |
| 02 | `0.40–0.55` |
| 03 | `0.65–0.78` |
| 04 | `0.88–0.96` |
| 05 | `1.00` |

Profile này cho phép early coconut nhỏ rõ rệt trước khi mature palm trunk/crown hình thành.

#### Profile C — support-structure plant

Dùng cho: `dragon-fruit`.

Đo **plant envelope / coverage**, không tính fixed post/trellis height vào metric chính.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.20–0.35` |
| 02 | `0.40–0.55` |
| 03 | `0.65–0.80` |
| 04 | `0.88–0.96` |
| 05 | `1.00` |

#### Profile D — aquatic upright/radial

Dùng cho: `lotus`.

Metric chính là composite của:

- leaf/stem structure;
- radial spread;
- vertical flower/bud envelope khi lifecycle cho phép.

Recommended maturity ratio:

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.40` |
| 02 | `0.45–0.65` |
| 03 | `0.65–0.82` |
| 04 | `0.85–0.95` |
| 05 | `1.00` |

Band stage 02/03 đã nới nhẹ (2026-08-26) theo số đo spread của lotus hiện tại (`0.64 / 0.81`).

Không dùng flower height ở stage 05 làm metric duy nhất, vì như vậy sẽ đánh giá sai leaf-spread progression.

#### Profile E — aquatic horizontal spread

Dùng cho: `water-mimosa`, `water-spinach`.

Metric chính:

```text
horizontalSpread + stem/leaf density
```

Recommended spread ratio:

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.35` |
| 02 | `0.45–0.60` |
| 03 | `0.65–0.80` |
| 04 | `0.85–0.95` |
| 05 | `1.00` |

Height có thể gần như plateau ở stage 03–05 mà vẫn PASS nếu spread/density progression rõ.

### 9.5 Relative scale giữa species

Runtime semantic reference hiện tại:

| Class | Display size gợi ý | Ví dụ |
|---|---:|---|
| S | `64–96 px` | tiny stage, weed, pest, small tool |
| M | `128–160 px` | rice, carrot, herb, water-mimosa, water-spinach |
| L | `192–256 px` | corn, coffee, dragon-fruit, lotus |
| XL | `256–384 px` | mango, pomelo, coconut, rubber, major fruit tree |

Relative species scale là **canonical gameplay intent**. Lifecycle normalization không được ép các species khác nhau thành cùng pixel height.

Không dùng master bbox size để kết luận world scale một cách độc lập; phải xem semantic class và runtime display target.

Làm rõ (2026-08-26): master stage-05 target px (§9.7) là mục tiêu **tận dụng resolution của canvas**, không phải cơ chế enforce world scale. Cross-species world scale được enforce duy nhất bằng runtime display size ở bảng trên. Vì vậy hai species khác semantic class vẫn có thể cùng fill gần hết master canvas của chúng.

Calibration bổ sung (2026-08-26, sau visual review):

- `corn` là **crop duy nhất thuộc class L** (đúng bảng trên) — display target ~224 px, phải cao vượt rice rõ rệt; master corn ≈ rice là bình thường vì cả hai chạm trần canvas, khác biệt nằm ở display scale;
- `lemon` hạ xuống **cây ăn trái thấp nhất**, display target ~256 px (biên L/XL) — thấp hơn mango/pomelo/star-apple; citrus nhỏ không đứng ngang các đại thụ.

### 9.6 Remaining-plant geometry matrix — REQUIRED SUPPORT

Tất cả species trong `FARM_REMAINING_PLANT_ASSET_PLAN.vi.md` phải được audit theo matrix này:

| Species | Geometry class | Canvas policy | Anchor policy | Size class | Progression profile | Dominant growth metric | Stage-05 scale policy |
|---|---|---|---|---|---|---|---|
| `coconut` | tall/special palm | `1024×1024` — LOCKED (đo 2026-08-26, không cần tall canvas) | fixed ground root `(512,970)` | XL | B | height + crown spread | tallest member trong remaining tree pack; stage-05 visH ≈ 946 px sau resample `×0.768` |
| `dragon-fruit` | support-structure perennial | `1024×1024` preferred | fixed plant base + support anchor → `(512,970)`; pack hiện tại lệch, fix `×0.98` + translate | L | C | plant envelope/coverage excluding fixed post | thấp hơn major fruit tree; không normalize theo post height |
| `coffee` | compact tree/shrub | `1024×1024` | fixed root `(512,970)` | L | A | visible height + canopy complexity | compact; phải thấp hơn major fruit trees/coconut/rubber ở world scale |
| `rubber` | tall industrial tree | `1024×1024` nếu fit; `1024×1280` nếu cần | fixed ground root; square/tall root contract tương ứng | XL | A | height + trunk thickness | tall; lớn hơn coffee, exact relation với coconut/major tree khóa sau audit |
| `lotus` | aquatic upright/radial | `1024×1024` — LOCKED | fixed root `(512,970)`; align thủ công (radial morphology, §7.1) | L | D | radial spread + stem/leaf structure + final flower envelope | không so raw height trực tiếp với land tree |
| `water-mimosa` | aquatic horizontal | `768×768` — LOCKED | fixed waterline/root anchor `(384, 728)`; align X theo bbox center (§5.4) | M | E | horizontal spread + density | low/wide; width progression quan trọng hơn height |
| `water-spinach` | aquatic horizontal | `768×768` — LOCKED | fixed waterline/root anchor `(384, 728)`; align X theo bbox center (§5.4) | M | E | horizontal spread + density | low/wide; distinct silhouette from water-mimosa |

`Stage-05 scale policy` trong bảng trên là cross-species intent. Exact master-pixel target chỉ được `LOCKED` sau khi session audit đo toàn bộ references và chọn calibration set.

### 9.7 Stage-05 target height/dimension policy

Mỗi species sau audit phải có một record:

```text
semanticSizeClass: L | XL | M | ...
stage05TargetMetric: visibleHeight | horizontalSpread | plantEnvelope | composite
stage05TargetValuePx: <locked after audit>
stageRatios: [s1, s2, s3, s4, 1.0]
```

Không được dùng một `stage05TargetValuePx` duy nhất cho tất cả species.

Nếu hai species cùng semantic class nhưng morphology rất khác, có thể dùng target metric khác nhau. Ví dụ:

- coffee: visible height;
- dragon-fruit: plant envelope excluding support;
- lotus: radial/composite envelope;
- water-mimosa: horizontal spread.

---

## 10. Lifecycle semantics dùng chung cho plant/tree pack

Nếu species dùng 5 stage:

- đúng 5 ảnh riêng biệt;
- không contact sheet;
- không sprite sheet thay cho master;
- stage 01 nhỏ nhất;
- stage 02 là early/sapling/sprout, không harvest cue;
- stage 03 young vegetative;
- stage 04 mature/flowering khi applicable;
- stage 05 harvestable/final;
- harvest focal point chỉ xuất hiện đúng lifecycle;
- species-specific spec có thể override tên stage nhưng không override shared-anchor rule.

Fruit tree/perennial mặc định:

```text
stage-01_sprout
stage-02_sapling
stage-03_young
stage-04_flowering-or-mature
stage-05_harvestable
```

---

## 11. Naming và file contract

Master asset filename phải deterministic:

```text
<species>_stage-<NN>_<semantic>_v<NN>.png
```

Ví dụ:

```text
coffee_stage-01_sprout_v01.png
coffee_stage-02_sapling_v01.png
coffee_stage-03_young_v01.png
coffee_stage-04_flowering_v01.png
coffee_stage-05_berry_v01.png
```

Directory:

```text
masters/<domain>/<asset-class>/<species>/
```

Không đổi filename chỉ vì normalize canvas/anchor nếu artwork version không thay đổi về semantic/art direction.

### 11.1 Atlas runtime — hợp đồng đặt tên (chốt 2026-09-07)

Một atlas cho mỗi asset class, không gộp theo wave và không per-species:

```text
<domain>_<class>_v<NN>
```

Đường dẫn output cố định:

```text
runtime/<atlas>.json
runtime/1x/<domain>/<class>/<atlas>.png
```

Ví dụ: `farm_crops_v01` → `runtime/farm_crops_v01.json` + `runtime/1x/farm/crops/farm_crops_v01.png`.

Danh sách species/tile trong atlas **đọc từ filesystem và sort alphabetical**, không hardcode — thêm một pack master mới là chỉ cần build lại. Với mỗi tile/pack có nhiều version, atlas lấy version **cao nhất đọc được**; version cao hơn nhưng file hỏng thì tụt xuống và ghi rõ lý do.

---

## 12. Normalization policy — được phép và không được phép

### 12.1 Được phép không redraw

Các transform production được phép:

- translate trên transparent canvas;
- resize/downscale/upscale nhẹ để normalize relative scale;
- canvas resize/pad/crop transparent-only vùng rỗng;
- alpha-aware bbox measurement;
- metadata/anchor correction;
- atlas packing;
- runtime downsampling.

### 12.2 Không được coi là normalization

Các thay đổi sau là artwork edit/regeneration:

- vẽ thêm leaf/fruit/flower;
- xóa branch/object;
- repaint trunk;
- compositing phần của stage khác vào;
- procedural reconstruction;
- thay đổi morphology bằng raster manipulation.

Nếu cần các thay đổi này, phải regenerate/edit artwork explicit.

### 12.3 Translation phải được verify trên raw PNG

Sau mọi translation:

- đo lại alpha bbox raw file;
- đo lại contact/root band;
- không chỉ mở playground để kiểm tra.

Playground/runtime code **không được tự bù anchor per-stage để che lỗi master** trong QC mode.

---

## 13. Runtime anchor contract

Runtime anchor phải phản ánh semantic master anchor.

Nếu master tree 1024 có:

```text
root_px = (512,970)
```

runtime normalized anchor phải tương ứng:

```text
(0.5, 0.947265625)
```

Nếu runtime atlas frame đã trim/crop transparent padding, anchor phải được remap từ master-space sang frame-space một cách deterministic.

Không copy một runtime anchor cũ cho asset mới nếu master geometry khác.

### 13.1 Legacy runtime metadata cần audit — GIẢI QUYẾT XONG (giữ làm lịch sử)

> **Trạng thái 2026-09-07:** toàn bộ atlas nhắc trong mục này (`core_fruit_trees_v01/v02`,
> `core_crops_v01`, `herb_crops_v01`, `soil_states_v01`) **đã bị xoá khỏi repo** và thay bằng
> 4 atlas sinh bằng `tools/build_atlas.py` — xem §13.2. Phần dưới giữ nguyên làm ghi chép
> lịch sử của đợt audit 2026-08-26, không mô tả trạng thái hiện tại.

`runtime/core_fruit_trees_v01.json` khi đó có metadata legacy như:

```text
masterCanvas = 1122×1402
placementAnchor = (0.5, 0.88)
```

Trong khi generation plan hiện tại dùng tree master target `1024×1024`.

Do đó metadata này **không được coi là canonical geometry mới** trước khi session audit xác minh lại toàn pipeline.

Hiện trạng runtime metadata **tại thời điểm 2026-08-26** (snapshot lịch sử, đã bị §13.2 thay thế):

- `core_fruit_trees_v01.json` — legacy `1122×1402` / anchor `(0.5, 0.88)`, cover mango/pomelo/lemon/star-apple; phải rebuild `v02` sau khi masters normalize về `1024×1024` với anchor `(0.5, 0.947265625)`.
- `lychee`, `rambutan` — master `1254×1254`, **chưa có runtime JSON**.
- `coffee`, `dragon-fruit`, `coconut`, `lotus` — **chưa có runtime JSON**.
- `core_crops_v01.json`, `herb_crops_v01.json` — khớp master 512 hiện tại, giữ anchor `(0.5, 0.684)`.

### 13.2 Atlas runtime hiện hành — LOCKED (2026-09-07)

Atlas không còn dựng tay. `tools/build_atlas.py` sinh toàn bộ từ `masters/`, có test
(`tools/test_build_atlas.py`), idempotent (chạy 2 lần ra byte y hệt), build fail thì không ghi gì.

```bash
python3 tools/build_atlas.py                        # dựng lại cả 4 atlas
python3 tools/build_atlas.py --atlas farm_soil_v01  # chỉ 1 atlas
python3 tools/build_atlas.py --dry-run              # xem trước, không ghi file
```

**Atlas là sản phẩm sinh ra từ masters — không sửa tay.** Sai số liệu thì sửa master hoặc sửa
script rồi build lại, không patch JSON.

| Atlas | Nguồn master | Kích thước | Cell | Nội dung | Thay cho |
|---|---|---|---|---|---|
| `farm_crops_v01` | `masters/farm/crops/*/` | 960×1152 | 192 | 6 species × 5 stage | `core_crops_v01` + `herb_crops_v01` |
| `farm_trees_v01` | `masters/farm/trees/*/` | 1280×2560 | 256 | 10 species × 5 stage | `core_fruit_trees_v01` + `v02` |
| `farm_aquatic_v01` | `masters/farm/aquatic-crops/*/` | 960×576 | 192 | 3 species × 5 stage | *(chưa từng có atlas)* |
| `farm_soil_v01` | `masters/farm/soil/*.png` | 576×384 | 192 | 6 tile | `soil_states_v01` |

Đường dẫn: `runtime/<atlas>.json` + `runtime/1x/farm/<class>/<atlas>.png` (§11.1).

**Schema (khác bản legacy, code game phải đọc lại):**

- **Frame key là slot id** `<species>_stage-0N` — ví dụ `coffee_stage-05`, `rubber_stage-05`. Key
  **không** mang nhãn semantic, vì nhãn stage lệch nhau giữa species (`coffee` → `berry`,
  `rubber` → `tapping`, còn lại → `fruiting`); nếu key mang nhãn thì game phải tra bảng mới dựng
  được key. Soil là ngoại lệ: key là full stem (`soil_dry`, `soil_tilled`...).
- **`stageOrder`** luôn là `["stage-01","stage-02","stage-03","stage-04","stage-05"]`.
- **`stageNames`**: map `<species> -> ["seeded","sprout",...]` giữ phần semantic, **chỉ để hiển thị**.
- **`anchor.x` luôn = 0.5**, cố định theo cách các pack được normalize: nhóm thân đơn căn bottom-band
  về tâm canvas, nhóm rosette căn bbox center về tâm canvas (§7.1). **Không đo bottom-band centroid
  để làm anchorX** — heuristic đó sai với morphology rosette và từng làm culantro trượt ngang tới
  37 px giữa các stage. Centroid vẫn được đo và báo ở dòng `NOTE` như tín hiệu QC master, không làm
  fail build.
- **`anchor.y` đo từng file** = `contactY / canvasH`, ghi cho **từng frame**; `placementAnchor` chỉ
  là giá trị đại diện, kèm `anchorUniform` / `anchorSpread`:
  - crops: `0.894531` đồng nhất (458/512, `anchorUniform: true`);
  - trees: `0.947266` đồng nhất (970/1024, `anchorUniform: true`);
  - aquatic: per-frame `0.947266`–`0.947917` (lotus canvas 1024, water-* canvas 768);
  - soil: per-frame `0.701172`–`0.703125`.
- **`masterCanvasBySpecies`** có mặt khi atlas trộn nhiều canvas — hiện chỉ `farm_aquatic_v01`
  (lotus 1024×1024, water-mimosa / water-spinach 768×768). Cell giữ đồng nhất; game bù display
  scale theo §9.5, atlas không tự scale.
- `farm_soil_v01` lấy ô tilled từ `soil_tilled_v02.png` — `v01` hỏng IDAT vĩnh viễn, script chọn
  version cao nhất đọc được (§11.1).

---

## 14. Art rules dùng chung liên quan trực tiếp đến geometry

Mọi asset Mayhoa phải tiếp tục tuân art-style spec:

- nostalgic hand-painted farm sprite;
- soft painterly rendering;
- readable silhouette;
- selective dark-chromatic outlines;
- lighting upper-left;
- organic asymmetry;
- không photorealistic;
- không glossy/vector-clean quá mức;
- không over-detail;
- species/object identity đọc được ở gameplay size.

Geometry normalization không được phá các đặc điểm này.

---

## 15. Canonical QC checklist cho mỗi multi-stage species

### File / canvas

- [ ] Đúng số file/stage.
- [ ] Filename đúng convention.
- [ ] Tất cả stage cùng canvas size.
- [ ] Canvas đúng target class.
- [ ] PNG có alpha/background transparent sạch.

### Anchor

- [ ] Semantic anchor đã được xác định rõ.
- [ ] Raw master PNG cùng exact anchor coordinate.
- [ ] Grounded asset có cùng contact/root Y (crop: contactY = 458 — §5.3).
- [ ] Crop: composite check lên soil tile — chân cây tại tâm plate, không lòi dưới plate.
- [ ] Root/contact X được đo từ base band, không từ canopy center.
- [ ] Không align top.
- [ ] Không center từng stage riêng.

### Bounds

- [ ] Không opaque pixel chạm edge ngoài ý muốn.
- [ ] Có breathing room hợp lý.
- [ ] Không crop leaf/fruit/branch/body.
- [ ] Bottom padding đúng class contract.

### Growth / scale

- [ ] Perceived size tăng đúng lifecycle.
- [ ] Stage sau không nhỏ hơn stage trước nếu spec yêu cầu monotonic growth.
- [ ] Stage 05 không nhỏ hơn stage 04.
- [ ] Không chỉ là cùng hình scale lên.
- [ ] Relative world scale đúng semantic class.

### Lifecycle / content

- [ ] Stage semantics đúng species.
- [ ] Không flower/fruit/harvest cue quá sớm.
- [ ] Final stage có focal cue đủ rõ nhưng không overload.

### Runtime

- [ ] Runtime anchor được derive từ canonical master anchor.
- [ ] Atlas trim/remap không làm đổi gameplay pivot.
- [ ] Playground không dùng per-stage auto-anchor để che lỗi master.
- [ ] Atlas được build lại bằng `python3 tools/build_atlas.py` sau khi master đổi — không sửa tay JSON/PNG atlas (§13.2).
- [ ] `git status` sạch sau khi build lại atlas (script idempotent; có diff nghĩa là master đã đổi thật).

---

## 16. Audit plan cho session tiếp theo

Session tiếp theo nên quét toàn bộ `masters/` theo thứ tự:

### Pass A — inventory

Với mỗi PNG ghi:

```text
path
asset class
canvas W×H
alpha bbox
visible W×H
semantic anchor type
measured contact/root X/Y
stage index
```

### Pass B — group theo lifecycle/species

Với mỗi species:

- xác minh same canvas;
- xác minh same root/contact/waterline;
- xác minh monotonic stage scale;
- tìm top-aligned hoặc independently-centered pack;
- tìm file sai master target.

### Pass C — normalize

Chỉ normalize pack có rule đã khóa:

- tree/perennial 1024: root `(512,970)`;
- crop: giữ current crop contract cho tới khi crop audit chốt;
- aquatic: lotus đã chốt `1024×1024` root `(512,970)` — normalize được ngay; mimosa/spinach chốt anchor theo pack rồi mới normalize;
- các class khác: define semantic anchor trước khi sửa file.

### Pass D — runtime metadata

Sau khi master pass:

- audit runtime JSON anchor;
- rebuild atlas bằng `python3 tools/build_atlas.py` (dùng `--dry-run` để xem trước) — không remap tay;
- không sửa runtime trước master.

### Pass E — visual playground

Cuối cùng mới kiểm tra:

- stage transition;
- soil/pond placement;
- relative scale giữa species;
- no jump ở anchor;
- no crop/clipping khi sway/animation.

---

## 17. Audit report format đề xuất

Mỗi species nên có record dạng:

```text
Species: coffee
Class: tree/perennial
Semantic size class: L
Canvas: 1024×1024
Canonical anchor: (512,970)
Dominant growth metric: visibleHeight + canopyComplexity
Stage-05 target metric: visibleHeight
Stage-05 target value: <px after calibration>
Stage metric values: [...]
Stage ratios vs stage-05: [..., 1.0]
Measured root coordinates: [...]
Anchor delta max: ... px
Within-species progression: PASS/FAIL
Cross-species scale: PASS/FAIL
Canvas: PASS/FAIL
Lifecycle: PASS/FAIL
Clipping: PASS/FAIL
Action: KEEP / TRANSLATE / RESCALE / REGENERATE
```

Với aquatic horizontal plant, thay `visibleHeight` bằng `horizontalSpread`/composite metric phù hợp. Với dragon-fruit, report phải có plant-envelope metric **excluding fixed support post**.

Recommended tolerance:

```text
Master anchor target: exact preferred
Measurement tolerance from anti-alias/root-band heuristic: <= 1 px ideal, <= 2 px acceptable only if semantic contact is visually identical
```

Không dùng tolerance để hợp thức hóa lệch rõ bằng mắt.

---

## 18. Source-of-truth precedence

Khi các docs cũ mâu thuẫn nhau về geometry, ưu tiên:

1. **`MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md`** — anchor/canvas/layout/QC geometry.
2. Species-specific explicit lifecycle spec — morphology/harvest semantics.
3. `FARM_ASSET_GENERATION_PLAN.vi.md` — roadmap/size/lifecycle general contract.
4. `MAYHOA_ART_STYLE_SPEC.vi.md` — visual style/art direction.
5. Existing runtime JSON/README — implementation reference; có thể là legacy và phải audit.

Rule quan trọng:

> **Master geometry phải đúng trước. Runtime code/metadata không được dùng để che một master asset sai anchor.**

---

## 19. Current locked decisions

Tại thời điểm tạo spec này:

```text
Normal tree canvas: 1024×1024
Normal tree root:   (512,970)
Tree root meaning:  lowest/root contact point on raw master PNG
Tree growth:        grows upward/outward from fixed root
Tree stage rule:    same canvas + same root across lifecycle
Same stage rule:    same biological maturity, NOT same absolute pixel height
Growth audit:       use species-specific dominantGrowthMetric
Stage-05 target:    per-species/per-morphology, never one global px value
QC alpha threshold: 24/255
Master format:      RGBA8 PNG; palette/quantized master không hợp lệ
Crop contract:      512×512, root (256,458) = (0.5,0.89453125), contactY=458 Δ0, max visH 434
Tile plant point:   tâm soil plate (256,260) ≈ (0.5,0.508) — điểm engine ghim mọi plant root
Aquatic anchor:     lotus LOCKED 1024×1024 root (512,970); mimosa/spinach pack-specific, pending
Coconut canvas:     1024×1024 LOCKED — không dùng 1024×1280
Runtime legacy:     removed 2026-09-07 — thay bằng 4 atlas sinh từ script (§13.2)
Atlas naming:       <domain>_<class>_v<NN>, một atlas cho mỗi class (§11.1)
Atlas build:        python3 tools/build_atlas.py — atlas là build product, không sửa tay
Atlas frame key:    slot id <species>_stage-0N; soil dùng full stem (soil_dry...)
Atlas anchorX:      hằng số 0.5, không đo bottom-band centroid
Atlas anchorY:      contactY/canvasH, đo và ghi cho từng frame
```

Remaining-plan support is explicitly defined for:

- `coconut` → Profile B / tall-special palm;
- `dragon-fruit` → Profile C / support-structure plant;
- `coffee` → Profile A / compact tree-shrub;
- `rubber` → Profile A / tall industrial tree;
- `lotus` → Profile D / aquatic upright-radial;
- `water-mimosa` → Profile E / aquatic horizontal;
- `water-spinach` → Profile E / aquatic horizontal.

Đây là baseline cho lần quét/normalize toàn bộ Mayhoa assets tiếp theo.

---

## 20. Measured baseline — 2026-08-26

Đo bằng `tools/geometry_audit.py` (alpha ≥ 24/255, bottom band 3% visible height). Δ = chênh lệch lớn nhất giữa các stage trong pack. Chuẩn PASS cho tree: contactY Δ=0, rootX Δ≤2 px, margin ≥24 px.

### Trees / perennial

| Species | Canvas | contactY (Δ) | rootX (Δ) | Margin xấu nhất | Ghi chú progression | Verdict |
|---|---|---|---|---|---|---|
| coffee | 1024² ✓ | 970 (Δ0) ✓ | 511–513 (Δ1.6) ✓ | 33 px ✓ | Profile A khớp (s03 = 0.867) | **PASS — calibration chuẩn** |
| dragon-fruit | 1024² ✓ | 987–988 (Δ1) | 500–501 (Δ1.4) | top 27 px (s03) | s04 ≈ s05 bbox trùng — visual check density | Nhất quán nội bộ, lệch canonical (−11.5, +17.5) |
| coconut | 1254² ✗ | 1236 (Δ0) ✓ | 645–647 (Δ1.1) ✓ | top 6 px (s05) ✗, đáy 17 px ✗ | 0.65/0.84/0.95/0.99 — vỡ Profile B | FAIL canvas + margin + progression |
| mango | 1122×1402 | 1282–1310 (Δ28) ✗ | 568–581 (Δ13) ✗ | 47 px ✓ | s05 visH < s04 (907 < 993) — check fruit cue | FAIL align |
| pomelo | 1122×1402 | 1290–1357 (Δ67) ✗ | 568–579 (Δ11) ✗ | 7 px (s05) ✗ | tăng dần ✓ | FAIL align + margin |
| lemon | 1122×1402 | 1167–1259 (Δ92) ✗ | 561–581 (Δ21) ✗ | 20 px (s05) ✗ | tăng dần ✓ | FAIL align |
| star-apple | 1122×1402 | 1218–1364 (Δ146) ✗ | 567–575 (Δ8) ✗ | 14 px (s05) ✗ | tăng dần ✓ | FAIL align (nặng nhất) |
| lychee | 1254² ✗ | 1155–1230 (Δ75) ✗ | 650–698 (Δ48) ✗ | 22 px (s05) ✗ | tăng dần ✓ | FAIL align cả 2 trục |
| rambutan | 1254² ✗ | 1173–1211 (Δ38) ✗ | 641–648 (Δ7) ✗ | 10 px (s04) ✗ | s05 < s04 cả 2 chiều ✗ | FAIL align + s04/s05 mâu thuẫn |

### Aquatic

| Species | Canvas | contactY (Δ) | rootX (Δ) | Margin | Spread progression | Verdict |
|---|---|---|---|---|---|---|
| lotus | 1254² ✗ | 1185–1187 (Δ2) | 585–647 (Δ62)* | 12 px (s05) ✗ | 0.25/0.64/0.81/0.95 — khớp Profile D (đã nới) | FAIL canvas; *heuristic radial, align thủ công |

### Crops (soil-plate anchor — không chấm contactY)

| Species | Canvas | rootX (Δ) | Margin xấu nhất | Progression | Verdict |
|---|---|---|---|---|---|
| rice | 512² ✓ (palette ✗) | 252–258 (Δ6) | 33 px ✓ | tăng dần ✓ | Hình học OK; format palette |
| corn | 512² ✓ (palette ✗) | 255–260 (Δ4) | top 4 px, đáy 19 px (s05) ✗ | tăng dần ✓ | FAIL margin s05 |
| carrot | 512² ✓ (palette ✗) | 256–265 (Δ9) | top 12 px (s04) ✗ | s05 < s04 (443 < 479) | FAIL margin s04; check s05 |
| tonkin-jasmine | 512² ✓ | 250–276 (Δ26) | 20 px (s03) | s05 < s04 cả 2 chiều ✗ | Visual check s05 |
| culantro | 512² ✓ | 228–352 (Δ125)* | 26 px | tăng dần ✓ | *Rosette — anchor thủ công (§7.1) |
| mint | 512² ✓ | 257–270 (Δ13) | 28 px | tăng dần ✓ | Gần PASS |

Kế hoạch xử lý chi tiết + scale factors: xem `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md`.

### 20.1 Post-normalize results — 2026-08-26 (cùng ngày)

Normalize pass đã chạy xong bằng `tools/normalize_pack.py`. Kết quả đo lại:

- **Tất cả 10 tree pack + lotus**: canvas `1024×1024`, contactY = 970 (Δ0), rootX 511.6–512.5 (Δ ≤ 1 px), mọi margin ≥ 25 px — **PASS toàn bộ**.
- **coconut**: per-stage rescale theo Profile B, ratio mới 0.332 / 0.506 / 0.725 / 0.916 / 1.0 — trong band.
- **crops (rev 2 cuối, cùng ngày)**: hai bước — (a) composite QC phát hiện chân crop lòi dưới soil plate; (b) calibration sheet xác nhận cây phải đứng **tâm plate**, dẫn tới chuyển crop sang **bottom-anchor sprite** root `(256, 458)`. Transform từ bản gốc (single resample): rice / tonkin-jasmine / culantro / mint scale 1.0 (chỉ translate), corn 0.8855, carrot 0.904. Herb rosette align X theo bbox center. Runtime `placementAnchor` cả 2 JSON đổi → `(0.5, 0.89453125)`, texture rebuild. Cả 3 pack palette thành RGBA8. Composite 30 frame + playground verify PASS. **Chờ xác nhận phía game code: điểm ghim trên tile = tâm plate.**
- **Visual QC**: 6/6 case trong regenerate queue PASS — không file nào phải generate lại.
- **Runtime**: `core_fruit_trees_v02.json` + atlas đã rebuild (cell 256×256, anchor `(0.5, 0.947265625)`); atlas cho các pack mới chờ quyết định naming; crops atlas texture nên re-render vì corn/carrot đã scale. *(Cập nhật 2026-09-07: naming đã chốt là một atlas cho mỗi class — `core_fruit_trees_v02` bị thay bằng `farm_trees_v01`, và toàn bộ atlas nay sinh bằng `tools/build_atlas.py`; xem §11.1 + §13.2.)*
- **Còn chờ**: playground verify (Pass E) + user compare diff + commit.
