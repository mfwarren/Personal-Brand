# How I Use AI to Write and Publish Blog Posts

This post is a bit meta. I'm using the exact workflow I'm about to describe to write and publish this very article.

Here's the setup: I speak my ideas out loud, an AI turns them into polished prose, another AI generates the hero image, and a set of scripts I built with AI assistance handles the publishing. The whole thing lives in a GitHub repository that you can clone and use yourself.

Let me walk you through how it works.

## The Problem With Writing

I have ideas. Lots of them. The bottleneck has never been coming up with things to write about—it's the friction between having a thought and getting it published.

Traditional blogging requires you to:
1. Sit down and type out your thoughts
2. Edit and format the content
3. Find or create images
4. Log into WordPress
5. Copy-paste everything into the editor
6. Set featured images, categories, meta descriptions
7. Preview, fix issues, publish

Each step is a context switch. Each context switch is an opportunity to abandon the post entirely. My drafts folder is a graveyard of half-finished ideas.

## Voice First

The breakthrough was realizing I don't need to type. I use [Wispr Flow](https://wispr.flow) for voice-to-text dictation. It runs locally on my Mac and transcribes speech with surprisingly good accuracy.

Now when I have an idea for a post, I just... talk. I ramble through my thoughts, explain the concept as if I'm telling a friend, and let the words flow without worrying about structure or polish.

The output is messy. It's conversational, full of "um"s and tangents. But it captures the core ideas in a way that staring at a blank page never did.

## AI as Editor

This is where Claude Code comes in. I take my raw dictation and ask Claude to transform it into a structured blog post. Not just grammar cleanup—actual restructuring, adding headers, tightening the prose, finding the narrative thread in my stream of consciousness.

The key is that I stay in control. Claude produces a markdown draft, and I review it. I keep what works, rewrite what doesn't, add details Claude couldn't know. The AI handles the tedious transformation from spoken word to written word. I handle the judgment calls about what's actually worth saying.

## The Publishing Pipeline

Here's where it gets interesting. I built a set of CLI tools that Claude Code can use to handle the entire publishing workflow.

When I'm ready to publish, I have a conversation like this:

```
Me: "Generate a cyberpunk-style hero image for this post about AI blogging workflows,
crop it to 16:9, and publish to WordPress with the featured image attached."

Claude: [Generates image with Gemini] → [Crops and converts to JPG] →
        [Uploads to WordPress] → [Converts markdown to Gutenberg blocks] →
        [Creates post with featured image] → Done. Here's your URL.
```

One conversation. Full pipeline. No clicking through WordPress admin panels.

## How the Tools Work

The publishing toolkit includes:

**Voice capture** - Wispr Flow transcribes my dictation to text

**Content transformation** - Claude Code converts raw transcription to structured markdown

**Image generation** - The Nano Banana Pro plugin generates hero images using Google's Gemini model

**Image processing** - A Python script crops images to 16:9 and converts to web-optimized JPG

**WordPress publishing** - Another Python script handles media uploads, post creation, and metadata via the WordPress REST API

**File organization** - Each post lives in its own dated folder with the markdown source, images, and a metadata JSON file for future edits

The WordPress MCP server that ships with Claude Code can create posts, but it can't upload media or set featured images. So I built CLI tools to fill those gaps. Claude Code runs them as needed during the publishing conversation.

## Everything in Git

The entire setup lives in a GitHub repository. Each blog post is a folder:

```
posts/
├── 2026-01-13-ai-powered-blog-workflow/
│   ├── content.md          # This post
│   ├── featured.jpg        # Hero image
│   ├── hero.png            # Original generated image
│   └── meta.json           # WordPress post ID, dates, SEO fields
```

Version control for blog posts. If I need to update something, I know exactly where to find it. The `meta.json` file stores the WordPress post ID so I can push updates to the live site.

## The Meta Part

Here's what's happening right now:
1. I dictated the concept for this post using Wispr Flow
2. I asked Claude Code to turn my rambling into a structured article
3. I reviewed and edited the markdown
4. I'll ask Claude to generate a hero image
5. Claude will crop it, upload it to WordPress, and publish

The workflow I'm describing is the workflow producing this description. It's turtles all the way down.

## Try It Yourself

The publishing toolkit is open source: [github.com/mfwarren/personal-brand](https://github.com/mfwarren/personal-brand)

You'll need:
- A WordPress site with REST API access
- An application password for authentication
- Claude Code with the Nano Banana Pro plugin for image generation
- Wispr Flow (or any voice-to-text tool) for dictation

Clone the repo, configure your credentials, and start talking. The gap between having an idea and publishing it has never been smaller.

---

*Written by dictation, edited by AI, published by CLI. The future of blogging is conversational.*
