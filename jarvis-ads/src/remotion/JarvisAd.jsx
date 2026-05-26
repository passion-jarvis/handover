import { AbsoluteFill, Img, Video, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

const BRAND = {
  yellow: "#D4FF00",
  black: "#000000",
  white: "#FFFFFF",
};

// Full-screen hook text overlay
function HookOverlay({ hook, subtext }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = spring({ frame, fps, from: 0, to: 1, config: { damping: 15 } });
  const translateY = interpolate(frame, [0, 15], [40, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "flex-start",
        padding: "60px 48px",
        background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 60%)",
      }}
    >
      <div style={{ opacity, transform: `translateY(${translateY}px)` }}>
        <div
          style={{
            fontFamily: "'Barlow Condensed', sans-serif",
            fontWeight: 800,
            fontSize: 64,
            lineHeight: 1.05,
            color: BRAND.white,
            textTransform: "uppercase",
            maxWidth: 900,
            marginBottom: 16,
            textShadow: "0 2px 20px rgba(0,0,0,0.8)",
          }}
        >
          {hook}
        </div>
        {subtext && (
          <div
            style={{
              fontFamily: "'Barlow Condensed', sans-serif",
              fontWeight: 600,
              fontSize: 36,
              color: BRAND.yellow,
              letterSpacing: 1,
            }}
          >
            {subtext}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
}

// Jarvis logo badge
function LogoBadge() {
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "flex-start", padding: 40 }}>
      <div
        style={{
          background: BRAND.yellow,
          color: BRAND.black,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 900,
          fontSize: 28,
          padding: "8px 20px",
          letterSpacing: 2,
          textTransform: "uppercase",
        }}
      >
        JARVIS
      </div>
    </AbsoluteFill>
  );
}

// CTA bar at bottom
function CTABar({ cta }) {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const startFrame = durationInFrames - fps * 2;
  const opacity = interpolate(frame, [startFrame, startFrame + 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 100 }}>
      <div
        style={{
          opacity,
          background: BRAND.yellow,
          color: BRAND.black,
          fontFamily: "'Barlow Condensed', sans-serif",
          fontWeight: 800,
          fontSize: 40,
          padding: "16px 48px",
          textTransform: "uppercase",
          letterSpacing: 2,
        }}
      >
        {cta}
      </div>
    </AbsoluteFill>
  );
}

// Main ad composition
export function JarvisAd({ videoSrc, imageSrc, hook, subtext, cta = "Book Free Call →", useVideo = false }) {
  return (
    <AbsoluteFill style={{ background: BRAND.black }}>
      {useVideo && videoSrc ? (
        <Video src={videoSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : imageSrc ? (
        <Img src={imageSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <AbsoluteFill style={{ background: "#111" }} />
      )}
      <HookOverlay hook={hook} subtext={subtext} />
      <LogoBadge />
      <CTABar cta={cta} />
    </AbsoluteFill>
  );
}
