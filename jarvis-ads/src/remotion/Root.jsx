import { Composition } from "remotion";
import { JarvisAd } from "./JarvisAd.jsx";
import { GithubSkillsVideo } from "./GithubSkillsVideo.jsx";
import { JarvisOffer } from "./JarvisOffer.jsx";

// Automation-focused ads — updated April 2026
const TOP5_ADS = [
  {
    id: "C1-AutomationMath",
    hook: "At $30K/month your rate is $180/hr",
    subtext: "Are you doing $10/hr tasks? Your VA automates them.",
    cta: "10 Seconds to Qualify →",
    imageSrc: "creatives/c2-10hr-trap-01.jpg",
  },
  {
    id: "C2-SystemsProblem",
    hook: "Doing $10K–$30K/month and still doing everything yourself?",
    subtext: "That's not a hustle problem. That's a systems problem.",
    cta: "Book Free Call →",
    imageSrc: "creatives/c1-time-prison-v-01.jpg",
  },
  {
    id: "C3-OtherVAs",
    hook: "Other VAs do the work. Ours automate it.",
    subtext: "So it never comes back to you.",
    cta: "See How It Works →",
    imageSrc: "creatives/c4-guarantee-01.jpg",
  },
  {
    id: "C4-NeverManage",
    hook: "Every VA I hired needed constant managing. Until Jarvis.",
    subtext: "Pre-trained. Automation-ready. Live in 60 minutes.",
    cta: "Get Your VA →",
    imageSrc: "creatives/c3-va-week-01.jpg",
  },
  {
    id: "C5-BeachAutomation",
    hook: "She's at the beach. Her VA is building automations right now.",
    subtext: "That's what $10K/month looks like with Jarvis.",
    cta: "Claim Your Spot →",
    imageSrc: "creatives/c1-time-prison-v-05.jpg",
  },
];

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="GithubSkills"
        component={GithubSkillsVideo}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="JarvisOffer"
        component={JarvisOffer}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
      />
      {TOP5_ADS.map((ad) => (
        <Composition
          key={ad.id}
          id={ad.id}
          component={JarvisAd}
          durationInFrames={150} // 5 seconds at 30fps
          fps={30}
          width={1080}
          height={1920}
          defaultProps={{
            hook: ad.hook,
            subtext: ad.subtext,
            cta: ad.cta,
            imageSrc: ad.imageSrc,
            useVideo: false,
          }}
        />
      ))}
    </>
  );
};
