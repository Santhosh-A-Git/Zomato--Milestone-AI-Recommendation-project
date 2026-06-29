---
name: Culinary Intelligence System
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#5b403f'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#5c5c5c'
  on-tertiary: '#ffffff'
  tertiary-container: '#757474'
  on-tertiary-container: '#fefcfc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1b1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#e4e2e2'
  tertiary-fixed-dim: '#c8c6c6'
  on-tertiary-fixed: '#1b1c1c'
  on-tertiary-fixed-variant: '#474747'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 32px
  stack-gap-lg: 32px
  stack-gap-md: 24px
  stack-gap-sm: 16px
---

## Brand & Style

The design system is engineered for a high-performance AI restaurant recommendation engine. It balances the urgency of hunger with the precision of machine learning. The brand personality is professional, reliable, and appetizing—steering away from cluttered discount-driven layouts toward a refined, editorial food-discovery experience.

The design style is **Corporate Modern with a Consumer Polish**. It utilizes a "White Space First" philosophy to ensure high-quality food photography remains the focal point. The interface is characterized by clean lines, high-contrast text for immediate readability, and a structured hierarchy that guides users through AI-generated insights without cognitive overload. It evokes an emotional response of confidence and culinary excitement.

## Colors

The palette is anchored by a high-energy **Warm Red**, specifically chosen to stimulate appetite and signal primary actions. This is contrasted against a stark **Text Dark** for maximum legibility, exceeding WCAG AA standards.

- **Primary (#E23744):** Used for CTA buttons, active states, and brand-critical iconography.
- **Surface (White/Light Gray):** The primary page background is pure white to maintain a crisp aesthetic. Panel backgrounds use the light gray to differentiate secondary content areas, like sidebar filters or metadata containers.
- **Semantic Colors:** Success (Green), Warning (Amber), and Error (Red) should be used sparingly but with high saturation to ensure they are noticed against the neutral backdrop.

## Typography

This design system utilizes **Inter** exclusively to ensure a systematic, utilitarian feel that performs exceptionally well at small sizes (menus, tags). 

- **Headlines:** Use tighter letter spacing and heavy weights (700-800) to create a strong visual anchor.
- **Body:** Standard weight (400) is used for readability in descriptions. 
- **Labels:** Caps are used for metadata (e.g., "AI RECOMMENDATION" or "OPEN NOW") to provide a distinct visual texture compared to body copy.
- **Mobile Scaling:** Headlines must scale down significantly on mobile to prevent awkward word breaks in long restaurant names.

## Layout & Spacing

The layout follows a **Fluid Grid** model with strict adherence to an 8px square baseline, though internal padding and margins are primarily driven by the **24-32px "Generous" rhythm**.

- **Desktop:** A 12-column grid with 24px gutters. Use a maximum container width of 1280px to prevent excessive line lengths in AI reviews.
- **Mobile:** A 4-column grid with 16px margins.
- **Rhythm:** Vertical stacks should default to 32px between major sections (e.g., between "Top Rated" and "Recently Added") and 16px between elements within a card. This "breathable" spacing is critical for a premium feel.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and tonal shifts rather than heavy borders.

- **Level 0 (Background):** Pure #FFFFFF.
- **Level 1 (Cards/Panels):** Uses a very soft, diffused shadow: `0px 4px 20px rgba(0, 0, 0, 0.05)`. This makes restaurant cards feel like they are floating slightly above the map or feed.
- **Level 2 (Modals/Dropdowns):** A more pronounced shadow to indicate focus: `0px 12px 32px rgba(0, 0, 0, 0.12)`.
- **Interactive States:** On hover, cards should slightly lift (increase shadow spread) to provide tactile feedback.

## Shapes

The shape language is **Rounded**, conveying a friendly and approachable consumer vibe while maintaining professional structure. 

- **Standard Elements (Buttons, Inputs):** 0.5rem (8px) radius.
- **Featured Cards:** 1rem (16px) radius to soften the visual impact of large food images.
- **Search Bars:** Should utilize the `rounded-xl` (1.5rem) or pill-shape to distinguish the primary AI prompt area from other functional UI elements.

## Components

- **Buttons:** Primary buttons use the #E23744 background with white text. Use 16px horizontal and 12px vertical padding. Secondary buttons should be ghost-style with a 1px border of Text Dark or Gray.
- **Cards:** The core of the product. Imagery must occupy the top 60% of the card. Text content should be padded at 20px. Use a subtle shadow and no border.
- **AI Badges:** Use a subtle gradient or a specific icon (e.g., a sparkle) to denote AI-generated recommendations. These should use the `label-sm` typography.
- **Input Fields:** Search inputs should be large (48-56px height) with #F8F8F8 backgrounds and subtle internal shadows to appear "inset" and ready for typing.
- **Chips/Filters:** Use the `rounded-lg` (16px) shape. Inactive filters use a light gray background; active filters use the Primary Red with white text.
- **Lists:** Use 24px spacing between list items in search results to ensure each restaurant entry has sufficient "visual territory."