import { Channel } from '../types';

export const CHANNELS: Channel[] = [
  {
    id: 'genius-junkie',
    name: 'Genius Junkie',
    tagline: 'Canva & small business tutorials for creators',
    color: '#FF6B35',
    accentDark: '#7C2D12',
    strategy: {
      contentPillars: [
        'Canva tutorials & walkthroughs',
        'Small business tools & software',
        'Digital templates & products',
        'Freelancer workflows & systems',
        'Social media design & branding',
      ],
      contentFormats: [
        'Step-by-step tutorial',
        'Tool comparison / review',
        'Template showcase',
        'Quick tip (Short)',
        'Deep-dive walkthrough',
        'Common mistakes / what not to do',
      ],
      targetAudience:
        'Small business owners, freelancers, and creators aged 25–45 who want practical design and workflow help',
      toneAndStyle:
        'Practical, friendly, actionable, relatable — like a knowledgeable friend explaining over shoulder',
      shortsCriteria: [
        'Single Canva trick or tip under 60 seconds',
        'Before/after design transformation',
        'Template reveal with clear value',
        'Quick workflow hack with immediate payoff',
        'Common mistake + fast fix',
      ],
      repurposingRules: [
        'Blog/Pinterest: step-by-step written version with screenshots — great for SEO and Pinterest traffic',
        'Email: "Tutorial of the Week" with direct link and one key takeaway',
        'Community post: poll asking their biggest design challenge (seeds next video)',
        'Instagram/TikTok Short: 30-second clip of the single best tip',
        'Lead magnet: offer the template from the video as a free download',
      ],
      avoidTopics: [
        'Enterprise or developer-focused software (too complex for audience)',
        'Advanced coding or technical development',
        'Topics unrelated to design, tools, or small business workflows',
        'Political or controversial commentary',
        'Highly saturated generic content without a unique Genius Junkie angle',
      ],
      keyPhrases: [
        'canva', 'template', 'small business', 'freelance', 'design',
        'tutorial', 'workflow', 'tools', 'branding', 'client',
        'social media', 'graphic', 'create', 'brand kit', 'mockup',
      ],
    },
  },
  {
    id: 'shipshop-tv',
    name: 'ShipShopTV',
    tagline: 'Authority-driven documentary content — power, loyalty, collapse',
    color: '#8B5CF6',
    accentDark: '#3B0764',
    strategy: {
      contentPillars: [
        'Business power dynamics & hierarchy',
        'Relationship psychology (loyalty, betrayal, trust)',
        'Corporate & empire collapse stories',
        'Status signaling & social currency',
        'Historical business & dynasty case studies',
      ],
      contentFormats: [
        'Mini-documentary (15–30 min)',
        'Story-driven essay with narration',
        'Case study breakdown',
        'Interview or deposition analysis',
        'Long-form explainer with cinematic packaging',
      ],
      targetAudience:
        'Ambitious professionals, entrepreneurs, and business-minded viewers aged 25–40 who want depth over entertainment',
      toneAndStyle:
        'Authoritative, investigative, cinematic, thought-provoking — serious, not sensational',
      shortsCriteria: [
        'Emotionally loaded single moment or revelation from the main video',
        'Shocking statistic or fact with immediate visceral impact',
        'Power quote that stands alone without context',
        'Suspenseful setup that leaves the viewer needing the long form to resolve it',
      ],
      repurposingRules: [
        'Shorts: extract the single most emotionally powerful 60-second moment',
        'Community post: thought-provoking question raised by the video (drives discussion)',
        'Twitter/X thread: 10-point framework or key takeaways from the video',
        'Newsletter: companion deep-dive piece with extra context and links',
        'LinkedIn: business lessons angle — reframe the story as a professional lesson',
      ],
      avoidTopics: [
        'Lifestyle, vlog, or personal daily content',
        'Tutorial or how-to instructional content',
        'Trending meme or reaction content',
        'Light entertainment without analytical substance',
        'Gossip-adjacent content without intellectual framing',
      ],
      keyPhrases: [
        'power', 'loyalty', 'betrayal', 'collapse', 'dynasty',
        'relationship', 'status', 'empire', 'documentary', 'hierarchy',
        'control', 'trust', 'strategy', 'influence', 'legacy',
      ],
    },
  },
  {
    id: 'ultra-health',
    name: 'UltraHealth',
    tagline: 'Trust-building educational health content with evergreen authority',
    color: '#10B981',
    accentDark: '#064E3B',
    strategy: {
      contentPillars: [
        'Evidence-based nutrition & diet science',
        'Fitness, performance & recovery protocols',
        'Mental health, cognition & sleep',
        'Longevity, biohacking & optimization',
        'Health myths debunked with research',
      ],
      contentFormats: [
        'Educational explainer with research backing',
        'Research paper breakdown (accessible)',
        'Expert framework or protocol walkthrough',
        'Myth-busting with cited evidence',
        'Practical implementation guide',
      ],
      targetAudience:
        'Health-conscious individuals, biohackers, and performance-focused viewers aged 28–50 who want evidence over hype',
      toneAndStyle:
        'Educational, trustworthy, evidence-based, empowering — credible without being cold or clinical',
      shortsCriteria: [
        'Single surprising health fact with cited source',
        'Quick myth bust — claim vs. what research actually shows',
        'Simple actionable tip with an immediate payoff',
        'Alarming statistic with measured, hopeful context',
      ],
      repurposingRules: [
        'Blog post: SEO-optimized long-form article with inline citations — high evergreen value',
        'Email newsletter: "Health Insight of the Week" with one key actionable takeaway',
        'Instagram carousel: infographic-style breakdown of the main framework',
        'Community post: health poll or question that seeds the next video topic',
        'Pinterest: evergreen health tip boards linked back to blog post',
      ],
      avoidTopics: [
        'Unverified or unsubstantiated medical claims',
        'Dangerous diet advice without research backing',
        'Sensationalized fear-based content with no solution',
        'Trending health fads not supported by peer-reviewed evidence',
        'Supplement recommendations that could be construed as medical advice',
      ],
      keyPhrases: [
        'health', 'nutrition', 'fitness', 'research', 'evidence',
        'longevity', 'recovery', 'protocol', 'science', 'study',
        'optimize', 'performance', 'gut', 'sleep', 'inflammation',
      ],
    },
  },
];

export const getChannel = (id: string) =>
  CHANNELS.find((c) => c.id === id) ?? CHANNELS[0];

export const PROMOTION_TEMPLATES: Record<string, string[]> = {
  'genius-junkie': [
    'Pin video thumbnail to Pinterest board',
    'Publish blog post version with screenshots',
    'Send "Tutorial of the Week" email',
    'Post community poll about biggest design challenge',
    'Upload 30-second Short clip',
    'Add template download link in description',
    'Share on Instagram Stories',
  ],
  'shipshop-tv': [
    'Extract best 60-second moment as Short',
    'Post thought-provoking community question',
    'Publish Twitter/X thread of key takeaways',
    'Send newsletter companion piece',
    'Reframe as LinkedIn business lesson post',
    'Pin video to relevant playlist',
  ],
  'ultra-health': [
    'Publish SEO blog post with citations',
    'Send "Health Insight of the Week" email',
    'Create Instagram carousel infographic',
    'Post community health poll',
    'Add to evergreen Pinterest health board',
    'Upload myth-bust Short clip',
    'Submit to relevant Reddit communities (r/nutrition, r/longevity)',
  ],
};
