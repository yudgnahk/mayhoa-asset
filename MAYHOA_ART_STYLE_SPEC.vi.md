# Mayhoa Art Style Spec — Nostalgic Hand-Painted Farm Sprite

## 1. Mục tiêu

Tài liệu này định nghĩa phong cách artwork chuẩn cho game **mayhoa**.

Mục tiêu là tạo ra một hệ visual thống nhất cho:

- Plants
- Animals
- Fish
- Dragons
- Farm props / environmental assets

Phong cách cần gợi cảm giác:

- **hoài niệm**
- **cozy**
- **casual**
- **dễ thương**
- **thân thuộc như game nông trại web đời cũ**
- nhưng vẫn đủ sạch và nhất quán để dùng cho game hiện đại

Định hướng tổng thể:

> **Nostalgic Hand-Painted Farm Sprite**
> = browser farm game nostalgia (2008–2012) + modern consistency

---

## 2. North Star

Phong cách tham chiếu chính:

- game nông trại web/social đời cũ
- cảm giác illustrated, hand-painted nhẹ
- cheerful pastel palette
- silhouette rõ, đọc tốt trong game
- không quá modern-vector
- không photoreal
- không glossy mobile fantasy hiện đại

Tinh thần hình ảnh:

- mềm
- sáng
- thân thiện
- có cảm giác “vẽ tay digital”
- không quá kỹ thuật
- không quá polished theo kiểu bóng bẩy

---

## 3. Style pillars

Có 5 trụ cột bắt buộc:

### 3.1 Soft painterly rendering

- Render mềm, hơi brushy
- Có texture cảm giác vẽ tay nhẹ
- Không dùng cel-shading quá cứng
- Không dùng gradient gắt
- Không dùng highlight trắng bóng kiểu nhựa

### 3.2 Selective outlines

- Có outline nhưng không bắt buộc viền mọi shape
- Outline nên mềm và có chọn lọc
- Ưu tiên dark green / dark brown / dark chromatic line
- Tránh pure black
- Tránh line quá dày, đều và cứng như vector icon

### 3.3 Readable silhouettes

- Asset phải đọc được nhanh trong gameplay
- Ưu tiên silhouette trước detail
- Nhìn ở kích thước nhỏ vẫn phải nhận ra loại object

### 3.4 Cheerful pastel palette

- Màu sáng, vui, thân thiện
- Hơi washed/pastel hơn game mobile modern
- Không neon
- Không overly saturated toàn asset
- Saturation cao chỉ dùng cho focal parts

### 3.5 Classic browser-farm nostalgia

- Giữ cảm giác game nông trại cũ
- Hơi 2.5D / farm-view quen thuộc
- Shape organic
- Không quá sạch như vector infographic
- Chấp nhận “khuyết điểm đẹp” như foliage hơi messy hoặc brush texture nhẹ

---

## 4. Style summary ngắn gọn

> A cozy nostalgic farming-game art style inspired by classic browser/social farm games.
> Assets are soft painterly sprites with readable silhouettes, cheerful pastel colors, selective outlines, gentle shading, and a hand-painted cartoon feel.
> The art should feel warm, familiar, and nostalgic rather than sleek, glossy, or hyper-detailed.

---

## 5. Hình khối và silhouette

## 5.1 Nguyên tắc chung

- Bắt đầu từ silhouette lớn trước
- Detail chỉ bổ sung sau khi silhouette đã rõ
- Asset organic không được quá đối xứng
- Shape nên tròn, thân thiện, mềm mại

## 5.2 Số lượng mass chính

Mỗi asset nên được xây từ khoảng:

- **3–7 primary masses** đối với asset nhỏ/trung bình
- **5–9 primary masses** đối với asset phức tạp hơn như tree lớn hoặc dragon

## 5.3 Organic asymmetry

- Không làm object quá cân đối
- Cây, bụi, con vật nên có lệch nhẹ tự nhiên
- Asymmetry tạo cảm giác sống và bớt “AI generic”

---

## 6. Outline system

## 6.1 Outer outline

- Có thể dùng outline ngoài ở mức nhẹ đến trung bình
- Màu outline: dark chromatic, không pure black
- Ưu tiên:
  - dark olive
  - dark moss
  - dark bark brown
  - muted dark green-brown

## 6.2 Inner line

- Inner line nhẹ hơn outer line
- Có thể dùng ít hoặc bỏ bớt ở vùng soft foliage
- Không line toàn bộ từng chiếc lá nhỏ

## 6.3 Selective edge treatment

- Vùng focal: line rõ hơn
- Vùng foliage mềm / shadow / nền phụ: line ít hơn hoặc hòa vào shape
- Không dùng stroke đồng đều mọi nơi

---

## 7. Rendering & shading

## 7.1 Shading style

- Shading mềm
- Painterly
- Brush-like transitions nhẹ
- Không airbrush nặng
- Không harsh cell-shading

## 7.2 Light direction

Mặc định:

- ánh sáng từ **upper-left**
- shadow nhẹ và mềm
- ground shadow mềm, ngắn, dễ đọc

## 7.3 Tone count

- 1 base tone
- 1 highlight tone
- 1 shadow tone
- Có thể thêm 1 accent tone nếu cần focal emphasis

## 7.4 Specular

- Không dùng glossy white specular
- Fruit có thể có vùng sáng mềm nhưng không bóng nhựa

## 7.5 Texture

- Có texture nhẹ dạng brush / painterly irregularity
- Không texture quá mạnh
- Không noise bẩn
- Không grain nặng

---

## 8. Color system

## 8.1 Mục tiêu màu

- Tươi sáng nhưng cân bằng
- Dễ thương nhưng không chói
- Nostalgic hơn modern neon casual

## 8.2 Color behavior

- Focal object được bão hòa hơn nền
- Background/environment nhẹ hơn
- Màu phải đồng nhất giữa các asset

## 8.3 Palette principles

### Greens

- Nhiều sắc xanh lá, nhưng hơi ấm và vui
- Green base không quá lạnh
- Có sự phân tầng:
  - foliage light
  - foliage base
  - foliage shadow
  - grass light
  - grass base
  - grass shadow

### Browns

- Wood/trunk dùng tông nâu ấm
- Tránh nâu xám quá nặng
- Có:
  - wood light
  - wood base
  - wood shadow

### Fruit accents

- Mango / fruits dùng yellow-orange ấm
- Có thể thêm green tint gần cuống
- Accent vừa phải, không neon

### Outline darks

- Outline là dark chromatic, không pure black

## 8.4 Những gì tránh

- neon green
- over-saturated yellow
- black shadow nặng
- contrast quá gắt
- màu kiểu plastic mobile fantasy

---

## 9. Level of detail

## 9.1 Nguyên tắc

- **Structural detail > decorative detail**
- Thêm detail để giải thích cấu trúc
- Không thêm detail chỉ để “trông nhiều hơn”

## 9.2 Small-size readability

Asset phải vẫn đọc được ở kích thước nhỏ, ví dụ khoảng 64–160 px trên màn hình.

## 9.3 Không over-detail

Tránh:

- quá nhiều leaf veins
- quá nhiều cánh/scale nhỏ
- quá nhiều viền lặp
- quá nhiều texture vụn
- quá nhiều deco elements rời rạc

---

## 10. Plants spec

## 10.1 Mục tiêu

Plant phải:

- nhận ra species hoặc nhóm species
- readable trong farm context
- có cảm giác hand-painted casual
- hợp với world cũ kiểu browser farming

## 10.2 Plant construction

Ưu tiên thứ tự:

1. overall silhouette
2. mass grouping
3. branch logic
4. focal leaves / flowers / fruits
5. soft rendering

## 10.3 Foliage

- Foliage nên đi theo cụm
- Không vẽ từng lá đều nhau trên toàn cây
- Chỉ vài leaf clusters mang tính nhận diện được vẽ rõ hơn
- Phần còn lại là foliage mass painterly

## 10.4 Branch logic

- Nên thấy thân/cành nâng đỡ foliage
- Không để canopy như cục tròn cắm vào trunk
- Cây phải có cảm giác sinh học hợp lý

## 10.5 Fruits / flowers

- Số lượng vừa đủ để đọc species
- Thường khoảng **3–5 fruit visible** cho tree trung bình
- Hoa có thể thành cluster
- Không treo/decorate ngẫu nhiên vô nghĩa

## 10.6 Plant growth readability

Nếu có nhiều growth stages:

- stage phải đọc được tăng trưởng
- silhouette thay đổi rõ
- color/value thay đổi có kiểm soát
- không chỉ “scale up”

---

## 11. Mango tree spec

## 11.1 Identity

Cây xoài chuẩn mayhoa cần có:

- canopy lớn, mềm, organic
- nhiều foliage masses chồng nhẹ
- lá xoài dài chỉ xuất hiện ở vài vị trí focal
- trunk nâu ấm, có branch logic rõ
- 3–5 quả xoài dễ nhận ra
- shading mềm
- soft ground patch/shadow

## 11.2 Tránh

- canopy quá tròn như broccoli
- quá nhiều lá nhỏ chĩa ra ngoài
- fruit bóng như nhựa
- outline đen dày
- render quá vector-clean
- detail “hero art” quá mức

## 11.3 Mango mood

- nostalgic
- hand-painted
- cozy
- cheerful
- phù hợp khi đặt trực tiếp vào farm scene

---

## 12. Animals spec

## 12.1 Mục tiêu

Animals phải:

- dễ thương
- readable ngay từ silhouette
- anatomy đơn giản nhưng đúng cảm giác
- hợp farm world

## 12.2 Construction priorities

1. body mass
2. head/body relation
3. legs/paws
4. ears/horns/tail
5. face accents

## 12.3 Rules

- Tỷ lệ cute nhẹ
- Head có thể hơi lớn hơn thực tế
- Limbs đơn giản, không nhiều chi tiết nhỏ
- Mắt/miệng đủ biểu cảm nhưng không anime hóa quá mức

## 12.4 Avoid

- realism
- quá nhiều fur detail
- anatomy nặng nề
- đổ bóng quá mạnh
- style chuyển sang mascot/vector sạch

---

## 13. Fish spec

## 13.1 Mục tiêu

Fish phải:

- rõ body/fin/tail
- silhouette flowing
- màu vui nhưng không neon
- hợp tổng thể farm game

## 13.2 Rules

- Simplified scales
- Fins rõ nhưng không quá nhiều chi tiết
- Có thể nhấn bằng accent color
- Không đi quá realistic aquatic rendering

---

## 14. Dragon spec

## 14.1 Mục tiêu

Dragon trong mayhoa là:

- cute fantasy creature
- không horror
- không dark fantasy
- vẫn hòa được vào farm world

## 14.2 Construction priorities

1. readable head
2. torso mass
3. tail
4. wings
5. horns / spikes nhẹ

## 14.3 Rules

- Shape mềm
- Biểu cảm thân thiện
- Scale detail tối giản
- Wing readable nhưng không quá phức tạp
- Palette phải hòa với world farm

## 14.4 Avoid

- quá ngầu, quá dữ, quá gothic
- black/red high-contrast fantasy style
- realistic reptile scales toàn thân
- chi tiết quá dày

---

## 15. Perspective & placement

## 15.1 World fit

Mọi asset phải có cảm giác:

- có thể đặt trực tiếp vào farm scene
- phù hợp góc nhìn browser farm
- không bị lệch style hoặc quá khác mức render

## 15.2 Grounding

Asset nên có:

- chân đế / ground patch / shadow nhẹ khi phù hợp
- cảm giác chạm đất rõ
- không trôi nổi

## 15.3 Scale consistency

- Asset cần consistent relative scale
- Cây, thú, crop, dragon phải có tỷ lệ hợp lý trong cùng thế giới

---

## 16. Production rules for generated assets

## 16.1 Runtime philosophy

Artwork final cho game sẽ dùng theo hướng:

- generate master art lớn
- sau đó optimize cho game
- runtime dùng raster sprite cho PixiJS

## 16.2 Asset output preference

Ưu tiên:

- transparent background
- object centered
- đủ breathing room
- clean silhouette
- không text
- không UI
- không background scene phức tạp nếu là asset đơn

## 16.3 Asset master sizes

Gợi ý asset master:

- small crop: 512 px
- medium plant / bush: 768 px
- tree / animal / fish / small dragon: 1024 px
- large hero asset: 1536 px hoặc hơn nếu cần

## 16.4 Runtime sizes gợi ý

- small crop: 64–128 px
- medium crop: 128–192 px
- tree: 256–384 px source
- animal: 128–256 px source
- fish: 96–192 px source
- small dragon: 256–384 px source

## 16.5 Optimization

- crop transparent padding
- pack sprite atlas
- dùng WebP hoặc PNG tùy pipeline
- nếu cần scale lớn hơn: cân nhắc compressed textures

---

## 17. PixiJS compatibility spec

Phong cách này phù hợp với PixiJS nếu dùng:

- transparent raster sprites
- atlas-based loading
- shared textures
- resize theo scale game
- lazy bundle loading

Nguyên tắc:

- không đưa thẳng master 1K/2K vào gameplay nếu object hiển thị nhỏ
- dùng sprite sheet/atlas để batching tốt hơn
- giữ nhất quán naming và grouping

---

## 18. Workflow chuẩn khi generate asset mới

## 18.1 Bước 1 — Xác định asset

Ví dụ:

- mango tree
- apple tree
- cow
- koi fish
- baby green dragon

## 18.2 Bước 2 — Áp spec mayhoa

Tất cả asset phải mặc định bám:

- nostalgic hand-painted farm sprite
- browser-farm nostalgia
- soft painterly rendering
- cheerful pastel palette
- selective outlines
- readable silhouette

## 18.3 Bước 3 — Generate master

Generate 1 hoặc vài version với:

- transparent background nếu cần asset runtime
- centered composition
- clean isolated asset

## 18.4 Bước 4 — QC

Kiểm theo checklist:

- đúng species/identity?
- đúng style mayhoa?
- silhouette rõ?
- màu hợp?
- có bị modern vector quá không?
- có bị over-detail không?
- có hòa vào farm world không?

## 18.5 Bước 5 — Export runtime

- resize
- atlas
- integrate vào PixiJS

---

## 19. Feedback / iteration protocol

Khi chỉnh asset, feedback nên ở dạng delta rõ ràng.

Ví dụ tốt:

- giữ silhouette, giảm saturation 15%
- giữ canopy, làm foliage mềm hơn
- ít outline hơn ở phần lá
- trunk nhỏ hơn 10%
- thêm 1 quả xoài, không đổi palette

Không nên dùng feedback mơ hồ như:

- làm đẹp hơn
- chi tiết hơn
- premium hơn
- nghệ hơn

---

## 20. Prompting rules cho các lần generate sau

Mỗi prompt generate cho mayhoa nên ngầm hoặc explicit chứa các ý sau:

- nostalgic browser farming game style
- soft painterly cartoon sprite
- cheerful pastel palette
- selective outlines
- readable silhouette
- cozy hand-painted feel
- suitable for a classic farm game world
- modern consistency, not glossy, not photorealistic
- no heavy black outlines
- no neon colors
- no over-detail

---

## 21. Hard “Do Not”

Tuyệt đối tránh các hướng sau:

- photoreal
- glossy mobile casual style
- vector-flat infographic style
- heavy black outlines
- neon palette
- harsh cel shading
- excessive gradients
- over-detail micro texture
- random decorative leaves/scales
- black heavy shadows
- hyper-clean symmetry
- mixed rendering styles in one asset
- dark fantasy dragon style
- horror monster style
- AI-looking decorative clutter

---

## 22. Acceptance checklist

Một asset được coi là đạt chuẩn mayhoa khi:

- Đúng identity / species / creature type
- Đọc tốt ở kích thước nhỏ
- Có silhouette rõ
- Giữ soft painterly feel
- Có nostalgic farm-game vibe
- Không bị vector-clean quá mức
- Không quá nhiều detail
- Palette vui, sáng, cân bằng
- Outline có chọn lọc, không quá đen
- Hòa được vào cùng world với các asset khác
- Có thể dùng trong PixiJS sau khi optimize

---

## 23. Default style directive cho mayhoa

Từ nay, nếu không có chỉ định khác, mọi asset cho mayhoa mặc định dùng directive sau:

> Generate in the agreed **Mayhoa nostalgic hand-painted farm sprite style**:
> inspired by classic browser/social farming games, with soft painterly rendering, cheerful pastel colors, readable silhouettes, selective dark-chromatic outlines, gentle shading, cozy nostalgic mood, and consistency for use inside a farming game world.
> Avoid glossy rendering, modern vector-clean style, neon colors, heavy black shadows, and over-detailed clutter.

---

## 24. Ghi chú vận hành

Tài liệu này là spec art chuẩn đang được thống nhất cho mayhoa.

Nếu sau này cần mở rộng, có thể tách thêm các sub-spec:

- Plants pack spec
- Animals pack spec
- Fish pack spec
- Dragons pack spec
- UI spec
- Environment tiles spec
- Animation spec
- PixiJS integration spec

Nhưng mọi sub-spec đều phải giữ nguyên **core style DNA** của tài liệu này.

## 25. Chốt định danh style

**Official working style name:**

> **Mayhoa Nostalgic Hand-Painted Farm Sprite**

Đây là style mặc định cho artwork của project mayhoa.
