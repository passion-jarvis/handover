import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Sequence,
} from "remotion";

// ─── Safe zones (1080×1920) ───────────────────────────────────────────────
const SAFE_TOP = 260;
const SAFE_BOTTOM = 340;
const PAD_X = 72;

// ─── Brand palette ────────────────────────────────────────────────────────
const C = {
  bg: "#080808",
  yellow: "#D4FF00",
  white: "#FFFFFF",
  dim: "rgba(255,255,255,0.55)",
  dimMore: "rgba(255,255,255,0.28)",
  grid: "rgba(255,255,255,0.05)",
  redAccent: "#FF3B3B",
};

// ─── Helpers ─────────────────────────────────────────────────────────────
function lerp(frame, [f0, f1], [v0, v1]) {
  return interpolate(frame, [f0, f1], [v0, v1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
}
function spr(frame, fps, delay = 0, cfg = {}) {
  return spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 15, stiffness: 180, ...cfg },
  });
}

// ─── Shared background ────────────────────────────────────────────────────
function Background() {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 450], [0, -180]);

  return (
    <AbsoluteFill style={{ background: C.bg, overflow: "hidden" }}>
      {/* Scrolling grid */}
      <div
        style={{
          position: "absolute",
          inset: "-200px",
          backgroundImage: `
            linear-gradient(${C.grid} 1px, transparent 1px),
            linear-gradient(90deg, ${C.grid} 1px, transparent 1px)
          `,
          backgroundSize: "100px 100px",
          transform: `translateY(${drift}px)`,
        }}
      />
      {/* Yellow top bloom */}
      <div
        style={{
          position: "absolute",
          top: -300,
          left: "50%",
          transform: "translateX(-50%)",
          width: 1000,
          height: 700,
          background:
            "radial-gradient(ellipse, rgba(212,255,0,0.10) 0%, transparent 65%)",
        }}
      />
      {/* Vignette */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.75) 100%)",
        }}
      />
    </AbsoluteFill>
  );
}

// ─── SCENE 1: Hook (0–80 = 2.7s) ─────────────────────────────────────────
function HookScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Flash
  const flash = lerp(frame, [0, 7], [0.85, 0]);

  // "TRAPPED" punches in
  const wordScale = spr(frame, fps, 0, { stiffness: 300, damping: 11 });
  const wordScale2 = interpolate(wordScale, [0, 1], [5, 1]);
  const wordOp = lerp(frame, [0, 5], [0, 1]);
  const glitchX = frame < 10 ? Math.sin(frame * 53) * 10 : 0;

  // Sub line
  const subOp = lerp(frame, [20, 38], [0, 1]);
  const subY = spr(frame, fps, 20, { damping: 18 });
  const subY2 = interpolate(subY, [0, 1], [50, 0]);

  // Yellow bar draws in
  const barW = lerp(frame, [30, 65], [0, 940]);

  // Badge
  const badgeOp = lerp(frame, [6, 20], [0, 1]);
  const badgeY = spr(frame, fps, 6, { damping: 16 });
  const badgeY2 = interpolate(badgeY, [0, 1], [-60, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
      <AbsoluteFill style={{ background: "white", opacity: flash }} />

      {/* Badge */}
      <div
        style={{
          opacity: badgeOp,
          transform: `translateY(${badgeY2}px)`,
          background: C.yellow,
          color: C.bg,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 28,
          padding: "7px 26px",
          letterSpacing: 4,
          textTransform: "uppercase",
          marginBottom: 20,
        }}
      >
        FOR E-COMMERCE FOUNDERS
      </div>

      {/* TRAPPED */}
      <div
        style={{
          opacity: wordOp,
          transform: `scale(${wordScale2}) translateX(${glitchX}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 200,
          color: C.yellow,
          letterSpacing: -5,
          lineHeight: 0.88,
          textShadow: `0 0 80px rgba(212,255,0,0.65)`,
          textAlign: "center",
        }}
      >
        TRAPPED
      </div>

      {/* Bar */}
      <div
        style={{
          width: barW,
          height: 5,
          background: C.yellow,
          marginTop: 14,
          marginBottom: 22,
          boxShadow: `0 0 24px ${C.yellow}`,
        }}
      />

      {/* Sub line */}
      <div
        style={{
          opacity: subOp,
          transform: `translateY(${subY2}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 700,
          fontSize: 50,
          color: C.white,
          textAlign: "center",
          padding: `0 ${PAD_X}px`,
          lineHeight: 1.2,
        }}
      >
        in your own business?
        <br />
        <span style={{ color: C.yellow }}>There's a fix.</span>
      </div>
    </AbsoluteFill>
  );
}

// ─── SCENE 2: The Problem (80–185 = 3.5s) ────────────────────────────────
const PAIN_LINES = [
  { text: "You're doing $10/hr tasks", em: false },
  { text: "with a $500/hr brain.", em: true },
  { text: "Every time you try to delegate —", em: false },
  { text: "it creates more work for you.", em: true },
];

function PainLine({ line, delay }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const x = spr(frame, fps, delay, { damping: 18, stiffness: 160 });
  const x2 = interpolate(x, [0, 1], [-120, 0]);
  const op = lerp(frame, [delay, delay + 12], [0, 1]);

  return (
    <div
      style={{
        opacity: op,
        transform: `translateX(${x2}px)`,
        fontFamily: "'Barlow Condensed', sans-serif",
        fontWeight: line.em ? 900 : 600,
        fontSize: line.em ? 60 : 50,
        color: line.em ? C.yellow : C.dim,
        lineHeight: 1.1,
        marginBottom: 10,
      }}
    >
      {line.text}
    </div>
  );
}

function ProblemScene() {
  const frame = useCurrentFrame();
  const titleOp = lerp(frame, [0, 14], [0, 1]);
  const titleY = interpolate(frame, [0, 14], [-30, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        padding: `${SAFE_TOP}px ${PAD_X}px ${SAFE_BOTTOM}px`,
        justifyContent: "center",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          opacity: titleOp,
          transform: `translateY(${titleY}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 34,
          color: C.dimMore,
          textTransform: "uppercase",
          letterSpacing: 4,
          marginBottom: 28,
        }}
      >
        Sound familiar?
      </div>

      {PAIN_LINES.map((line, i) => (
        <PainLine key={i} line={line} delay={i * 16} />
      ))}

      {/* Separator */}
      <div
        style={{
          width: lerp(frame, [70, 100], [0, 400]),
          height: 3,
          background: C.yellow,
          marginTop: 30,
        }}
      />
    </AbsoluteFill>
  );
}

// ─── SCENE 3: The Offer (185–335 = 5s) ───────────────────────────────────
const OFFER_ITEMS = [
  { num: "1", text: "AI-trained VA", detail: "Uses tools. Thinks. Executes." },
  { num: "2", text: "Pre-trained before Day 1", detail: "Zero onboarding time from you." },
  { num: "3", text: "No upfront payment", detail: "Pay only when work starts." },
  { num: "4", text: "Unlimited replacement", detail: "Wrong fit? We fix it. No cost." },
];

function OfferRow({ item, delay }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const y = spr(frame, fps, delay, { damping: 20, stiffness: 160 });
  const y2 = interpolate(y, [0, 1], [50, 0]);
  const op = lerp(frame, [delay, delay + 14], [0, 1]);

  return (
    <div
      style={{
        opacity: op,
        transform: `translateY(${y2}px)`,
        display: "flex",
        alignItems: "flex-start",
        gap: 18,
        marginBottom: 16,
      }}
    >
      <div
        style={{
          background: C.yellow,
          color: C.bg,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 26,
          width: 42,
          height: 42,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
          marginTop: 2,
        }}
      >
        {item.num}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 800,
            fontSize: 36,
            color: C.white,
            lineHeight: 1,
          }}
        >
          {item.text}
        </div>
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 500,
            fontSize: 26,
            color: C.dim,
          }}
        >
          {item.detail}
        </div>
      </div>
    </div>
  );
}

function OfferScene() {
  const frame = useCurrentFrame();
  const titleOp = lerp(frame, [0, 14], [0, 1]);
  const titleY = interpolate(frame, [0, 14], [-30, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        padding: `${SAFE_TOP}px ${PAD_X}px ${SAFE_BOTTOM}px`,
        justifyContent: "center",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          opacity: titleOp,
          transform: `translateY(${titleY}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 44,
          color: C.yellow,
          textTransform: "uppercase",
          letterSpacing: 2,
          marginBottom: 24,
        }}
      >
        What Jarvis delivers:
      </div>

      {OFFER_ITEMS.map((item, i) => (
        <OfferRow key={item.num} item={item} delay={i * 16} />
      ))}
    </AbsoluteFill>
  );
}

// ─── SCENE 4: Guarantee (335–415 = 2.7s) ─────────────────────────────────
const GUARANTEES = [
  "① No payment before your VA starts",
  "② Zero risk of wrong hire",
  "③ We replace until you get the right one",
];

function GuaranteeScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const starScale = spr(frame, fps, 0, { stiffness: 220, damping: 12 });
  const starScale2 = interpolate(starScale, [0, 1], [0, 1]);
  const starOp = lerp(frame, [0, 10], [0, 1]);

  const headOp = lerp(frame, [10, 24], [0, 1]);
  const headY = spr(frame, fps, 10, { damping: 18 });
  const headY2 = interpolate(headY, [0, 1], [30, 0]);

  const pulse = 1 + Math.sin(frame * 0.2) * 0.02;

  return (
    <AbsoluteFill
      style={{
        padding: `${SAFE_TOP}px ${PAD_X}px ${SAFE_BOTTOM}px`,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      {/* Star badge */}
      <div
        style={{
          opacity: starOp,
          transform: `scale(${starScale2})`,
          fontSize: 64,
          marginBottom: 10,
        }}
      >
        ★
      </div>

      {/* Headline */}
      <div
        style={{
          opacity: headOp,
          transform: `translateY(${headY2}px)`,
          textAlign: "center",
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 74,
          color: C.white,
          lineHeight: 0.95,
          textTransform: "uppercase",
          marginBottom: 32,
        }}
      >
        You're not taking{" "}
        <span style={{ color: C.yellow }}>a risk.</span>
        <br />
        We are.
      </div>

      {/* Guarantee lines */}
      {GUARANTEES.map((g, i) => {
        const op = lerp(frame, [26 + i * 14, 40 + i * 14], [0, 1]);
        const y = spr(frame, fps, 26 + i * 14, { damping: 18 });
        const y2 = interpolate(y, [0, 1], [30, 0]);
        return (
          <div
            key={i}
            style={{
              opacity: op,
              transform: `translateY(${y2}px)`,
              fontFamily: "'Barlow Condensed', sans-serif",
              fontWeight: 600,
              fontSize: 30,
              color: C.dim,
              marginBottom: 8,
              textAlign: "center",
            }}
          >
            {g}
          </div>
        );
      })}

      {/* Pulsing CTA */}
      <div
        style={{
          transform: `scale(${pulse})`,
          opacity: lerp(frame, [60, 72], [0, 1]),
          marginTop: 32,
          background: C.yellow,
          color: C.bg,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 40,
          padding: "16px 50px",
          letterSpacing: 2,
          textTransform: "uppercase",
          boxShadow: `0 0 36px rgba(212,255,0,0.55)`,
        }}
      >
        Book Free Call →
      </div>
    </AbsoluteFill>
  );
}

// ─── SCENE 5: CTA (415–450 = 1.2s) ──────────────────────────────────────
function CTAScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spr(frame, fps, 0, { stiffness: 200, damping: 13 });
  const scale2 = interpolate(scale, [0, 1], [0.75, 1]);
  const op = lerp(frame, [0, 10], [0, 1]);

  return (
    <AbsoluteFill
      style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", gap: 20 }}
    >
      <div
        style={{
          opacity: op,
          transform: `scale(${scale2})`,
          textAlign: "center",
          padding: `0 ${PAD_X}px`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 44,
            color: C.dim,
            textTransform: "uppercase",
            letterSpacing: 3,
          }}
        >
          gojarvis.ai
        </div>
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 80,
            color: C.white,
            lineHeight: 0.95,
            textTransform: "uppercase",
          }}
        >
          Your VA.
          <br />
          <span style={{ color: C.yellow }}>Zero risk.</span>
        </div>
        <div
          style={{
            background: C.yellow,
            color: C.bg,
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 44,
            padding: "18px 54px",
            letterSpacing: 2,
            textTransform: "uppercase",
            marginTop: 8,
            boxShadow: `0 0 40px rgba(212,255,0,0.5)`,
          }}
        >
          🔗 Link in Bio
        </div>
      </div>
    </AbsoluteFill>
  );
}

// ─── Master composition (450 frames = 15s @ 30fps) ────────────────────────
export function JarvisOffer() {
  return (
    <AbsoluteFill>
      <Background />

      {/* Scene 1 — Hook:      0–79   (2.7s) */}
      <Sequence from={0} durationInFrames={80}>
        <HookScene />
      </Sequence>

      {/* Scene 2 — Problem:   80–184  (3.5s) */}
      <Sequence from={80} durationInFrames={105}>
        <ProblemScene />
      </Sequence>

      {/* Scene 3 — Offer:     185–334 (5s) */}
      <Sequence from={185} durationInFrames={150}>
        <OfferScene />
      </Sequence>

      {/* Scene 4 — Guarantee: 335–414 (2.7s) */}
      <Sequence from={335} durationInFrames={80}>
        <GuaranteeScene />
      </Sequence>

      {/* Scene 5 — CTA:       415–449 (1.2s) */}
      <Sequence from={415} durationInFrames={35}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
}
