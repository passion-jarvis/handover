import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Sequence,
} from "remotion";

// ─── Safe zones (1080×1920) ───────────────────────────────────────────────
// Instagram/TikTok: top UI ~250px, bottom UI ~340px
const SAFE_TOP = 260;
const SAFE_BOTTOM = 350;
const SAFE_H = 1920 - SAFE_TOP - SAFE_BOTTOM; // 1310px usable
const PAD_X = 72;

// ─── Palette ──────────────────────────────────────────────────────────────
const C = {
  bg: "#070B0F",
  yellow: "#D4FF00",
  cyan: "#00E5FF",
  purple: "#BF5AF2",
  white: "#FFFFFF",
  dim: "rgba(255,255,255,0.55)",
  gridLine: "rgba(255,255,255,0.06)",
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
    config: { damping: 14, stiffness: 180, ...cfg },
  });
}

// ─── Animated grid background ─────────────────────────────────────────────
function GridBG() {
  const frame = useCurrentFrame();
  const scrollY = interpolate(frame, [0, 450], [0, -160]);

  return (
    <AbsoluteFill style={{ background: C.bg, overflow: "hidden" }}>
      {/* Scrolling grid */}
      <div
        style={{
          position: "absolute",
          inset: "-200px",
          backgroundImage: `
            linear-gradient(${C.gridLine} 1px, transparent 1px),
            linear-gradient(90deg, ${C.gridLine} 1px, transparent 1px)
          `,
          backgroundSize: "90px 90px",
          transform: `translateY(${scrollY}px)`,
        }}
      />
      {/* Top cyan bloom */}
      <div
        style={{
          position: "absolute",
          top: -300,
          left: "50%",
          width: 900,
          height: 700,
          transform: "translateX(-50%)",
          background:
            "radial-gradient(ellipse, rgba(0,229,255,0.14) 0%, transparent 70%)",
        }}
      />
      {/* Bottom purple bloom */}
      <div
        style={{
          position: "absolute",
          bottom: -200,
          left: "30%",
          width: 700,
          height: 600,
          background:
            "radial-gradient(ellipse, rgba(191,90,242,0.10) 0%, transparent 70%)",
        }}
      />
    </AbsoluteFill>
  );
}

// ─── Scanline overlay ─────────────────────────────────────────────────────
function Scanlines() {
  return (
    <AbsoluteFill
      style={{
        backgroundImage:
          "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.08) 3px, rgba(0,0,0,0.08) 4px)",
        pointerEvents: "none",
      }}
    />
  );
}

// ─── SCENE 1: Hook (0–90 frames = 3 s) ────────────────────────────────────
function HookScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Stutter flash at start
  const flash = lerp(frame, [0, 6], [0.7, 0]);

  // "FREE" smashes in
  const freeScale = spr(frame, fps, 0, { stiffness: 280, damping: 10 });
  const freeScale2 = interpolate(freeScale, [0, 1], [4, 1]);
  const freeOpacity = lerp(frame, [0, 4], [0, 1]);

  // Glitch offset flicker
  const glitchX = frame < 12 ? Math.sin(frame * 47) * 8 : 0;

  // Badge drop
  const badgeY = spr(frame, fps, 8, { stiffness: 200, damping: 16 });
  const badgeY2 = interpolate(badgeY, [0, 1], [-80, 0]);
  const badgeOp = lerp(frame, [8, 20], [0, 1]);

  // Sub-line slides up
  const subY = spr(frame, fps, 18, { damping: 18 });
  const subY2 = interpolate(subY, [0, 1], [50, 0]);
  const subOp = lerp(frame, [18, 34], [0, 1]);

  // Neon underline draws in
  const lineW = lerp(frame, [30, 60], [0, 920]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 0,
      }}
    >
      {/* Flash */}
      <AbsoluteFill style={{ background: "white", opacity: flash }} />

      {/* Badge */}
      <div
        style={{
          opacity: badgeOp,
          transform: `translateY(${badgeY2}px)`,
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: C.cyan,
          color: C.bg,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 30,
          padding: "6px 22px",
          letterSpacing: 4,
          textTransform: "uppercase",
          marginBottom: 24,
        }}
      >
        ⚡ DEV CHEAT CODE
      </div>

      {/* FREE */}
      <div
        style={{
          opacity: freeOpacity,
          transform: `scale(${freeScale2}) translateX(${glitchX}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 240,
          color: C.yellow,
          letterSpacing: -6,
          lineHeight: 0.9,
          textShadow: `0 0 100px rgba(212,255,0,0.7), 0 0 30px rgba(212,255,0,0.4)`,
          textAlign: "center",
        }}
      >
        FREE
      </div>

      {/* Neon underline */}
      <div
        style={{
          width: lineW,
          height: 4,
          background: `linear-gradient(90deg, ${C.yellow}, ${C.cyan})`,
          marginTop: 8,
          marginBottom: 24,
          boxShadow: `0 0 20px ${C.cyan}`,
        }}
      />

      {/* Sub-line */}
      <div
        style={{
          opacity: subOp,
          transform: `translateY(${subY2}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 700,
          fontSize: 54,
          color: C.white,
          textAlign: "center",
          padding: `0 ${PAD_X}px`,
          lineHeight: 1.15,
        }}
      >
        Claude Code skills{" "}
        <span style={{ color: C.cyan }}>on GitHub</span>
        <br />
        that actually work
      </div>
    </AbsoluteFill>
  );
}

// ─── SCENE 2: Repos (90–240 = 5 s) ──────────────────────────────────────
const REPOS = [
  {
    name: "anthropics/claude-plugins-official",
    label: "OFFICIAL",
    desc: "30+ verified skills — /browse /qa /ship",
    color: C.cyan,
    icon: "🏛️",
  },
  {
    name: "gstack-dev/skills",
    label: "COMMUNITY",
    desc: "gstack suite — full browser + deploy stack",
    color: C.yellow,
    icon: "⚡",
  },
  {
    name: "awesome-claude-code",
    label: "CURATED",
    desc: "Community-maintained mega-list",
    color: C.purple,
    icon: "🔥",
  },
];

function RepoCard({ repo, delay }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const x = spr(frame, fps, delay, { stiffness: 160, damping: 18 });
  const x2 = interpolate(x, [0, 1], [-160, 0]);
  const op = lerp(frame, [delay, delay + 12], [0, 1]);

  return (
    <div
      style={{
        opacity: op,
        transform: `translateX(${x2}px)`,
        display: "flex",
        flexDirection: "column",
        gap: 6,
        background: "rgba(255,255,255,0.04)",
        border: `2px solid ${repo.color}`,
        borderLeft: `6px solid ${repo.color}`,
        borderRadius: 12,
        padding: "22px 26px",
        marginBottom: 18,
        boxShadow: `0 0 24px ${repo.color}22`,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <span style={{ fontSize: 30 }}>{repo.icon}</span>
        <span
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 22,
            color: repo.color,
            letterSpacing: 3,
            textTransform: "uppercase",
          }}
        >
          {repo.label}
        </span>
      </div>
      <div
        style={{
          fontFamily: "monospace",
          fontSize: 26,
          fontWeight: 700,
          color: C.white,
          letterSpacing: 0.5,
        }}
      >
        {repo.name}
      </div>
      <div
        style={{
          fontFamily: "'Barlow Condensed', sans-serif",
          fontSize: 26,
          color: C.dim,
          fontWeight: 500,
        }}
      >
        {repo.desc}
      </div>
    </div>
  );
}

function ReposScene() {
  const frame = useCurrentFrame();

  const titleY = interpolate(frame, [0, 20], [-40, 0], {
    extrapolateRight: "clamp",
  });
  const titleOp = lerp(frame, [0, 16], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        padding: `${SAFE_TOP}px ${PAD_X}px ${SAFE_BOTTOM}px`,
        justifyContent: "center",
        flexDirection: "column",
      }}
    >
      {/* Title */}
      <div
        style={{
          opacity: titleOp,
          transform: `translateY(${titleY}px)`,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 44,
          color: C.white,
          textTransform: "uppercase",
          letterSpacing: 2,
          marginBottom: 28,
        }}
      >
        Bookmark these repos →
      </div>

      {REPOS.map((r, i) => (
        <RepoCard key={r.name} repo={r} delay={i * 18} />
      ))}
    </AbsoluteFill>
  );
}

// ─── SCENE 3: Skills (240–390 = 5 s) ────────────────────────────────────
const SKILLS = [
  { cmd: "/browse", desc: "Headless browser QA", color: C.cyan },
  { cmd: "/qa", desc: "Test + fix bugs auto", color: C.yellow },
  { cmd: "/ship", desc: "PR → deploy 1 command", color: C.purple },
  { cmd: "/investigate", desc: "Root cause any bug", color: C.cyan },
  { cmd: "/cso", desc: "Full security audit", color: "#FF6B6B" },
];

function SkillRow({ skill, index }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const delay = index * 12;

  const y = spr(frame, fps, delay, { damping: 20 });
  const y2 = interpolate(y, [0, 1], [60, 0]);
  const op = lerp(frame, [delay, delay + 14], [0, 1]);

  return (
    <div
      style={{
        opacity: op,
        transform: `translateY(${y2}px)`,
        display: "flex",
        alignItems: "center",
        gap: 20,
        marginBottom: 20,
      }}
    >
      <div
        style={{
          fontFamily: "monospace",
          fontSize: 30,
          fontWeight: 700,
          color: skill.color,
          background: `${skill.color}18`,
          border: `1.5px solid ${skill.color}55`,
          padding: "6px 18px",
          borderRadius: 8,
          minWidth: 230,
          textAlign: "center",
          boxShadow: `0 0 16px ${skill.color}22`,
        }}
      >
        {skill.cmd}
      </div>
      <div
        style={{
          fontFamily: "'Barlow Condensed', sans-serif",
          fontSize: 30,
          color: C.dim,
          fontWeight: 500,
        }}
      >
        — {skill.desc}
      </div>
    </div>
  );
}

function SkillsScene() {
  const frame = useCurrentFrame();

  const titleOp = lerp(frame, [0, 14], [0, 1]);
  const titleY = interpolate(frame, [0, 14], [-30, 0], {
    extrapolateRight: "clamp",
  });

  // Typing cursor blink
  const cursorOp = Math.floor(frame / 8) % 2 === 0 ? 1 : 0;

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
          fontFamily: "monospace",
          fontSize: 36,
          color: C.cyan,
          marginBottom: 8,
          letterSpacing: 1,
        }}
      >
        $ claude --list-skills
        <span style={{ opacity: cursorOp, color: C.cyan }}>█</span>
      </div>
      <div
        style={{
          width: 320,
          height: 2,
          background: `linear-gradient(90deg, ${C.cyan}, transparent)`,
          marginBottom: 28,
        }}
      />

      {SKILLS.map((s, i) => (
        <SkillRow key={s.cmd} skill={s} index={i} />
      ))}
    </AbsoluteFill>
  );
}

// ─── SCENE 4: CTA (390–450 = 2 s) ────────────────────────────────────────
function CTAScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spr(frame, fps, 0, { stiffness: 200, damping: 12 });
  const scale2 = interpolate(scale, [0, 1], [0.7, 1]);
  const op = lerp(frame, [0, 12], [0, 1]);

  // Pulsing CTA button
  const pulse = 1 + Math.sin(frame * 0.25) * 0.025;

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          opacity: op,
          transform: `scale(${scale2})`,
          textAlign: "center",
          padding: `0 ${PAD_X}px`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 88,
            color: C.white,
            lineHeight: 0.95,
            textTransform: "uppercase",
          }}
        >
          All free.
          <br />
          <span style={{ color: C.yellow }}>Right now.</span>
        </div>

        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontSize: 38,
            color: C.dim,
            fontWeight: 500,
            marginTop: 4,
          }}
        >
          No setup fee. No credit card.
        </div>

        <div
          style={{
            transform: `scale(${pulse})`,
            background: C.yellow,
            color: C.bg,
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 900,
            fontSize: 46,
            padding: "18px 56px",
            letterSpacing: 2,
            textTransform: "uppercase",
            marginTop: 12,
            boxShadow: `0 0 40px rgba(212,255,0,0.5)`,
          }}
        >
          🔗 Link in Bio
        </div>
      </div>
    </AbsoluteFill>
  );
}

// ─── Master composition ───────────────────────────────────────────────────
export function GithubSkillsVideo() {
  return (
    <AbsoluteFill>
      <GridBG />
      <Scanlines />

      {/* Scene 1 — Hook: frames 0–89 (3 s) */}
      <Sequence from={0} durationInFrames={90}>
        <HookScene />
      </Sequence>

      {/* Scene 2 — Repos: frames 90–239 (5 s) */}
      <Sequence from={90} durationInFrames={150}>
        <ReposScene />
      </Sequence>

      {/* Scene 3 — Skills: frames 240–389 (5 s) */}
      <Sequence from={240} durationInFrames={150}>
        <SkillsScene />
      </Sequence>

      {/* Scene 4 — CTA: frames 390–449 (2 s) */}
      <Sequence from={390} durationInFrames={60}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
}
