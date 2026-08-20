# Mayhoa Art Style Spec — Nostalgic Hand-Painted Farm Sprite

## 1. Goal

This document defines the canonical artwork style for the **mayhoa** game.

The goal is to create one consistent visual system for:

- Plants
- Animals
- Fish
- Dragons
- Farm props / environmental assets

The style should evoke:

- **nostalgia**
- **coziness**
- **casual charm**
- **cuteness**
- **the familiar feeling of old browser farming games**
- while remaining clean and consistent enough for a modern game

Overall direction:

> **Nostalgic Hand-Painted Farm Sprite**
> = browser farm game nostalgia (2008–2012) + modern consistency

---

## 2. North Star

Primary references for the style:

- classic browser/social farming games
- lightly illustrated, hand-painted feeling
- cheerful pastel palette
- clear silhouettes that read well in gameplay
- not overly modern-vector
- not photorealistic
- not glossy modern mobile fantasy

The visual spirit should feel:

- soft
- bright
- friendly
- digitally hand-painted
- not overly technical
- not overly polished or glossy

---

## 3. Style pillars

There are five mandatory pillars:

### 3.1 Soft painterly rendering

- Soft, slightly brushy rendering
- Light hand-painted texture
- No overly hard cel shading
- No harsh gradients
- No glossy white plastic-like highlights

### 3.2 Selective outlines

- Outlines may be present, but not every shape needs to be fully outlined
- Outlines should be soft and selective
- Prefer dark green / dark brown / dark chromatic lines
- Avoid pure black
- Avoid thick, uniform, rigid lines like vector icons

### 3.3 Readable silhouettes

- Assets must read quickly during gameplay
- Prioritize silhouette before detail
- The object type must remain recognizable at small sizes

### 3.4 Cheerful pastel palette

- Bright, cheerful, friendly colors
- Slightly more washed/pastel than modern mobile games
- No neon colors
- Do not oversaturate the entire asset
- Higher saturation should be reserved for focal parts

### 3.5 Classic browser-farm nostalgia

- Preserve the feeling of old farming games
- Familiar slight 2.5D / farm-view character
- Organic shapes
- Not as clean as vector infographic art
- Allow “beautiful imperfections” such as slightly messy foliage or subtle brush texture

---

## 4. Short style summary

> A cozy nostalgic farming-game art style inspired by classic browser/social farm games.
> Assets are soft painterly sprites with readable silhouettes, cheerful pastel colors, selective outlines, gentle shading, and a hand-painted cartoon feel.
> The art should feel warm, familiar, and nostalgic rather than sleek, glossy, or hyper-detailed.

---

## 5. Shape and silhouette

### 5.1 General principles

- Start with the large silhouette first
- Add detail only after the silhouette is clear
- Organic assets should not be overly symmetrical
- Shapes should be rounded, friendly, and soft

### 5.2 Number of primary masses

Each asset should generally be built from roughly:

- **3–7 primary masses** for small/medium assets
- **5–9 primary masses** for more complex assets such as large trees or dragons

### 5.3 Organic asymmetry

- Do not make objects too perfectly balanced
- Trees, bushes, and animals should have slight natural asymmetry
- Asymmetry makes assets feel alive and less “AI generic”

---

## 6. Outline system

### 6.1 Outer outline

- A light-to-medium outer outline may be used
- Outline color should be dark chromatic, never pure black by default
- Preferred colors:
  - dark olive
  - dark moss
  - dark bark brown
  - muted dark green-brown

### 6.2 Inner line

- Inner lines should be lighter than the outer outline
- Use fewer or no inner lines in soft foliage areas
- Do not outline every small leaf

### 6.3 Selective edge treatment

- Focal areas: clearer lines
- Soft foliage / shadow / secondary areas: fewer lines or edges blended into the shape
- Do not use the same stroke weight everywhere

---

## 7. Rendering & shading

### 7.1 Shading style

- Soft shading
- Painterly rendering
- Gentle brush-like transitions
- No heavy airbrushing
- No harsh cel shading

### 7.2 Light direction

Default:

- light from the **upper-left**
- soft, gentle shadows
- short, readable, soft ground shadows

### 7.3 Tone count

- 1 base tone
- 1 highlight tone
- 1 shadow tone
- Optionally 1 accent tone when focal emphasis is needed

### 7.4 Specular

- Do not use glossy white specular highlights
- Fruit may have a soft light area, but should never look plastic

### 7.5 Texture

- Use light brush texture / painterly irregularity
- Do not use strong texture
- No dirty noise
- No heavy grain

---

## 8. Color system

### 8.1 Color goals

- Bright but balanced
- Cute without becoming glaring
- More nostalgic than modern neon casual games

### 8.2 Color behavior

- Focal objects may be more saturated than the background
- Background/environment colors should be softer
- Colors must remain consistent across asset families

### 8.3 Palette principles

#### Greens

- Use multiple greens, but keep them slightly warm and cheerful
- Base green should not be too cold
- Maintain layers such as:
  - foliage light
  - foliage base
  - foliage shadow
  - grass light
  - grass base
  - grass shadow

#### Browns

- Wood/trunks use warm browns
- Avoid overly gray, heavy browns
- Maintain:
  - wood light
  - wood base
  - wood shadow

#### Fruit accents

- Mangoes / fruits use warm yellow-orange
- A green tint near the stem is acceptable
- Accents should be controlled, never neon

#### Outline darks

- Outlines are dark chromatic, not pure black

### 8.4 Avoid

- neon green
- oversaturated yellow
- heavy black shadows
- overly harsh contrast
- plastic-looking mobile-fantasy colors

---

## 9. Level of detail

### 9.1 Principle

- **Structural detail > decorative detail**
- Add detail to explain structure
- Do not add detail merely to make the asset look “busier”

### 9.2 Small-size readability

Assets must remain readable at small on-screen sizes, for example roughly 64–160 px.

### 9.3 Avoid over-detailing

Avoid:

- too many leaf veins
- too many tiny petals/scales
- too many repeated outlines
- too much fragmented texture
- too many disconnected decorative elements

---

## 10. Plants spec

### 10.1 Goal

Plants must:

- communicate the species or species group
- read clearly in a farm context
- feel casually hand-painted
- fit the classic browser-farming world

### 10.2 Plant construction

Priority order:

1. overall silhouette
2. mass grouping
3. branch logic
4. focal leaves / flowers / fruits
5. soft rendering

### 10.3 Foliage

- Build foliage in clusters
- Do not render every leaf equally across the entire plant
- Only a few identifying leaf clusters should be rendered more clearly
- The rest should read as painterly foliage masses

### 10.4 Branch logic

- Trunks/branches should visibly support the foliage
- Do not make the canopy look like a round ball stuck onto a trunk
- Trees should have believable biological structure

### 10.5 Fruits / flowers

- Use only enough to communicate the species
- A medium tree will often show roughly **3–5 visible fruits**
- Flowers may form clusters
- Do not hang or decorate fruits/flowers randomly without structural logic

### 10.6 Plant growth readability

If multiple growth stages exist:

- each stage must clearly communicate growth
- silhouette should change visibly
- color/value changes should be controlled
- do not merely “scale up” the same asset

---

## 11. Mango tree spec

### 11.1 Identity

The canonical Mayhoa mango tree should have:

- a large, soft, organic canopy
- multiple lightly overlapping foliage masses
- long mango leaves appearing only in a few focal locations
- a warm-brown trunk with clear branch logic
- 3–5 easily recognizable mangoes
- soft shading
- a soft ground patch/shadow

### 11.2 Avoid

- an overly round broccoli-like canopy
- too many small leaves sticking outward
- glossy plastic-looking fruit
- thick black outlines
- overly vector-clean rendering
- excessive “hero art” detail

### 11.3 Mango mood

- nostalgic
- hand-painted
- cozy
- cheerful
- suitable for direct placement in a farm scene

---

## 12. Animals spec

### 12.1 Goal

Animals must:

- be cute
- read immediately from silhouette
- use simplified anatomy while still feeling correct
- fit naturally into the farm world

### 12.2 Construction priorities

1. body mass
2. head/body relation
3. legs/paws
4. ears/horns/tail
5. face accents

### 12.3 Rules

- Use slightly cute proportions
- The head may be a little larger than realistic
- Keep limbs simple with minimal tiny detail
- Eyes/mouth should be expressive enough without becoming overly anime

### 12.4 Avoid

- realism
- excessive fur detail
- heavy anatomy
- overly strong shadows
- drifting into clean mascot/vector styling

---

## 13. Fish spec

### 13.1 Goal

Fish must have:

- clear body/fin/tail structure
- a flowing silhouette
- cheerful color without neon
- a visual fit with the overall farm game

### 13.2 Rules

- Simplified scales
- Clear fins without excessive detail
- Accent colors may be used selectively
- Avoid overly realistic aquatic rendering

---

## 14. Dragon spec

### 14.1 Goal

Dragons in Mayhoa are:

- cute fantasy creatures
- not horror
- not dark fantasy
- still visually compatible with the farm world

### 14.2 Construction priorities

1. readable head
2. torso mass
3. tail
4. wings
5. light horns / spikes

### 14.3 Rules

- Soft shapes
- Friendly expressions
- Minimal scale detail
- Wings should read clearly without being overly complex
- Palette must harmonize with the farm world

### 14.4 Avoid

- overly cool, aggressive, or gothic treatment
- black/red high-contrast fantasy styling
- realistic full-body reptile scales
- overly dense detail

---

## 15. Perspective & placement

### 15.1 World fit

Every asset should feel like it:

- can be placed directly into the farm scene
- fits the familiar browser-farm viewing angle
- does not break style or render-level consistency

### 15.2 Grounding

Assets should have, when appropriate:

- a base / ground patch / light shadow
- clear contact with the ground
- no floating appearance

### 15.3 Scale consistency

- Maintain consistent relative scale
- Trees, animals, crops, and dragons must have believable proportions within the same world

---

## 16. Production rules for generated assets

### 16.1 Runtime philosophy

Final game artwork should follow this pipeline:

- generate large master art
- optimize afterward for the game
- use raster sprites at runtime in PixiJS

### 16.2 Asset output preference

Prefer:

- transparent background
- centered object
- enough breathing room
- clean silhouette
- no text
- no UI
- no complex background scene for standalone assets

### 16.3 Asset master sizes

Suggested master sizes:

- small crop: 512 px
- medium plant / bush: 768 px
- tree / animal / fish / small dragon: 1024 px
- large hero asset: 1536 px or larger if needed

### 16.4 Suggested runtime sizes

- small crop: 64–128 px
- medium crop: 128–192 px
- tree: 256–384 px source
- animal: 128–256 px source
- fish: 96–192 px source
- small dragon: 256–384 px source

### 16.5 Optimization

- crop transparent padding
- pack sprite atlases
- use WebP or PNG depending on the pipeline
- if larger scaling is needed, consider compressed textures

---

## 17. PixiJS compatibility spec

This style works well with PixiJS when using:

- transparent raster sprites
- atlas-based loading
- shared textures
- resizing to game scale
- lazy bundle loading

Principles:

- do not send 1K/2K master art directly into gameplay when the object is shown small
- use sprite sheets/atlases for better batching
- keep naming and grouping consistent

---

## 18. Standard workflow for generating a new asset

### 18.1 Step 1 — Identify the asset

Examples:

- mango tree
- apple tree
- cow
- koi fish
- baby green dragon

### 18.2 Step 2 — Apply the Mayhoa spec

All assets must default to:

- nostalgic hand-painted farm sprite
- browser-farm nostalgia
- soft painterly rendering
- cheerful pastel palette
- selective outlines
- readable silhouette

### 18.3 Step 3 — Generate the master

Generate one or several versions with:

- transparent background when needed for runtime assets
- centered composition
- clean isolated asset

### 18.4 Step 4 — QC

Check:

- correct species/identity?
- correct Mayhoa style?
- clear silhouette?
- suitable colors?
- too modern-vector?
- over-detailed?
- does it fit the farm world?

### 18.5 Step 5 — Export runtime asset

- resize
- atlas
- integrate into PixiJS

---

## 19. Feedback / iteration protocol

When revising assets, feedback should be expressed as clear deltas.

Good examples:

- keep the silhouette, reduce saturation by 15%
- keep the canopy, make foliage softer
- use fewer outlines in the leaves
- make the trunk 10% smaller
- add 1 mango, keep the palette unchanged

Avoid vague feedback such as:

- make it prettier
- make it more detailed
- make it more premium
- make it more artistic

---

## 20. Prompting rules for future generations

Every Mayhoa generation prompt should implicitly or explicitly include:

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

Strictly avoid:

- photorealism
- glossy mobile casual style
- vector-flat infographic style
- heavy black outlines
- neon palette
- harsh cel shading
- excessive gradients
- over-detailed micro texture
- random decorative leaves/scales
- black-heavy shadows
- hyper-clean symmetry
- mixed rendering styles within one asset
- dark fantasy dragon styling
- horror monster styling
- AI-looking decorative clutter

---

## 22. Acceptance checklist

An asset is considered Mayhoa-compliant when:

- Identity / species / creature type is correct
- It reads well at small sizes
- The silhouette is clear
- It preserves the soft painterly feel
- It carries the nostalgic farm-game vibe
- It is not overly vector-clean
- It is not over-detailed
- The palette is cheerful, bright, and balanced
- Outlines are selective and not too black
- It fits naturally into the same world as other assets
- It can be used in PixiJS after optimization

---

## 23. Default style directive for Mayhoa

Unless explicitly overridden, every Mayhoa asset should use this directive by default:

> Generate in the agreed **Mayhoa nostalgic hand-painted farm sprite style**:
> inspired by classic browser/social farming games, with soft painterly rendering, cheerful pastel colors, readable silhouettes, selective dark-chromatic outlines, gentle shading, cozy nostalgic mood, and consistency for use inside a farming game world.
> Avoid glossy rendering, modern vector-clean style, neon colors, heavy black shadows, and over-detailed clutter.

---

## 24. Operational note

This document is the canonical art specification currently agreed for Mayhoa.

If needed later, it can be extended into dedicated sub-specs:

- Plants pack spec
- Animals pack spec
- Fish pack spec
- Dragons pack spec
- UI spec
- Environment tiles spec
- Animation spec
- PixiJS integration spec

All sub-specs must preserve the **core style DNA** defined here.

## 25. Final style identity

**Official working style name:**

> **Mayhoa Nostalgic Hand-Painted Farm Sprite**

This is the default artwork style for the Mayhoa project.
