# Electrochemistry / Body-Use Risk Research Notes

Use when a user asks about DIY electrically treated water, milk, “charged” liquids, electrodes, or body-contact/spray/ingestion safety.

## Core framing

Separate three layers:

1. **Anecdotal effect reports** — subjective benefits, forum posts, self-experiment logs.
2. **Established electrochemistry** — ion migration, pH/ORP changes, water splitting, chlorine/hypochlorite formation if chloride is present, electrode dissolution/leaching.
3. **Medical evidence** — clinical or toxicology literature for ingestion/topical/aerosol exposure. Usually much thinner than the electrochemistry literature.

Do not dismiss the user's experience, but do not treat “felt good” as proof of safety.

## Safety triage pattern

Ask/answer around exposure route and substrate:

- Route: drank, sprayed/inhaled, topical only, wound/eye/mucosa exposure.
- Amount: drops, teaspoons, cups, liters; number of days.
- Liquid: distilled vs tap/mineral/salted water vs milk/food.
- Electrode/contact: inert electrode vs alligator clip/copper/steel/unknown plating touching liquid.
- Symptoms: respiratory, GI, neurologic, mouth/throat burning, dizziness/fainting.

Immediate rule of thumb:

- Unknown metal touched liquid under voltage → treat batch as experimental electrolysis liquid, not body-use liquid.
- Do not spray unknown electrolysis liquids: aerosol inhalation can be higher risk than intact-skin contact.
- If severe symptoms or significant ingestion concern: recommend Poison Control / urgent care.

## Physics estimates

Use Faraday's law to estimate an upper-bound metal dissolution mass:

`mass = Q * M / (n * F)`

Where:

- `Q` = total charge in coulombs
- `M` = molar mass in g/mol
- `n` = electrons per ion
- `F` = 96485 C/mol

Approximate metal released per 1 C if dissolution is efficient:

- Fe²⁺: ~0.289 mg/C
- Cu²⁺: ~0.329 mg/C
- Zn²⁺: ~0.339 mg/C
- Ni²⁺: ~0.304 mg/C
- Cr³⁺: ~0.180 mg/C

In 250 mL, 1 C of Cu²⁺ equivalent is ~1.3 mg/L — around the EPA copper action level. Real values depend on current, time, water chemistry, passivation, electrode area, and sparks/particulates.

## Literature anchors to search/cite

Search terms:

- `electrolyzed water hypochlorous acid safety review`
- `electrolyzed water food safety applications`
- `electrocoagulation sacrificial electrode dissolution Faraday law`
- `stainless steel anodic dissolution chromium nickel electrolysis`
- `direct electrochemical oxidation proteins conductive diamond electrodes`
- `milk protein electrochemical oxidation`

Useful adjacent citations found in prior work:

- “Electrolyzed water as a disinfectant: A systematic review of factors affecting the production and efficiency of hypochlorous acid” — DOI: `10.1016/j.jwpe.2021.102228`
- “Electrolyzed Water: Food Safety Applications” — DOI: `10.1081/e-eafe2-120048421`
- “Electrolyzed hypochlorous acid water exhibits potent disinfectant activity…” — DOI: `10.3389/fmicb.2023.1284274`
- “Electrochemical dissolution of aluminium in electrocoagulation experiments” — DOI: `10.1007/s10008-016-3195-6`
- “Effects of Thiocyanate on Anodic Dissolution of Iron, Chromium, Nickel and Type 304 Stainless Steel” — DOI: `10.1149/2.068211jes`
- “Direct electrochemical oxidation of proteins at conductive diamond electrodes” — DOI: `10.1016/j.jelechem.2007.09.027`
- “On the electrochemical oxidation of methionine residues of proteins” — DOI: `10.1016/j.jelechem.2023.117209`

## Synthesis template

When responding:

1. Start with a clear risk conclusion in plain language.
2. Acknowledge subjective effects without validating safety.
3. Explain mechanisms: electric field/polarization, electrochemistry, electrode contamination.
4. Quantify plausible magnitude with Faraday's law when current/charge can be estimated.
5. Separate medical literature from non-medical adjacent literature.
6. Give practical safer alternatives: distilled water, known inert electrodes, clips dry/outside liquid, pH/ORP/conductivity checks, avoid spray/ingestion until characterized.
