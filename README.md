# Personal Brand Publishing Toolkit

An AI-assisted blog publishing workflow powered by [Claude Code](https://claude.ai/code).

## The Concept

Traditional blog publishing is tedious: write content, format it, find or create images, upload everything, set metadata, publish. Each step requires context-switching between different tools and interfaces.

This project flips that workflow. Instead of clicking through WordPress admin panels, I describe what I want to Claude Code and it handles the execution:

```
"Create a cyberpunk-style hero image for my new blog post about AI cooking apps,
crop it to 16:9, upload it to WordPress, convert my markdown draft to Gutenberg
blocks, and publish with the featured image attached."
```

One conversation. Full publish pipeline.

## How It Works

### The Problem

WordPress has an MCP (Model Context Protocol) server, but it's limited—no media uploads, no featured image support. Claude Code can create posts but can't handle the full publishing workflow out of the box.

### The Solution

Custom CLI tools that extend Claude Code's capabilities:

**`wp-media-upload.py`** - WordPress REST API wrapper
- Upload images and get media IDs
- Create posts with featured images
- Set featured images on existing posts

**`image-crop.py`** - Image processing utility
- Crop to specific aspect ratios (16:9, 4:3, 1:1)
- Convert PNG → JPG with quality control
- Centered cropping that preserves the focal point

### Image Generation

[Nano Banana Pro](https://github.com/buildatscale/nano-banana-pro) is a Claude Code plugin that adds AI image generation via Google's Gemini model. Install it with:

```bash
claude plugins:install buildatscale/nano-banana-pro
```

Then generate images conversationally: "Create a cyberpunk-style hero image for my blog post about cooking apps."

### The Workflow

1. **Draft** - Write blog posts in markdown (`wordpress-posts/*.md`)
2. **Generate** - Create hero images with AI (Gemini via Nano Banana Pro)
3. **Process** - Crop and convert images to web-optimized formats
4. **Convert** - Transform markdown to WordPress Gutenberg blocks
5. **Publish** - Upload media, create post, attach featured image

All orchestrated through natural language conversation with Claude Code.

## Usage

### Prerequisites

- [uv](https://github.com/astral-sh/uv) - Python package runner
- WordPress site with REST API enabled
- WordPress Application Password ([how to create](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/#application-passwords))
- [Nano Banana Pro](https://github.com/buildatscale/nano-banana-pro) - Claude Code plugin for AI image generation (uses Google Gemini)

### Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and configure:

```bash
WP_SITE_URL=https://www.yourdomain.com
WP_USERNAME=your-username
WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
GEMINI_API_KEY=your-gemini-key  # Optional, for image generation
```

### CLI Tools

```bash
# Upload an image
uv run wp-media-upload.py upload --image ./hero.jpg --title "Post Hero Image"

# Create and publish a post with featured image (saves metadata)
uv run wp-media-upload.py create-post \
  --title "My Blog Post" \
  --file ./post-content.html \
  --status publish \
  --featured-media 1234 \
  --save-meta ./posts/2026-01-13-my-post/

# Fetch metadata for existing post
uv run wp-media-upload.py fetch-meta --post-id 1234 --output ./posts/2026-01-13-my-post/

# Crop image to 16:9 aspect ratio
uv run image-crop.py hero.png --aspect 16:9 --output hero.jpg
```

### With Claude Code

The real power comes from conversational publishing:

```
You: "Publish my save-cooking draft with a cyberpunk kitchen hero image"

Claude: [Generates image] → [Crops to 16:9] → [Converts to JPG] →
        [Uploads to WordPress] → [Converts markdown to blocks] →
        [Creates post with featured image] → [Returns published URL]
```

## Project Structure

```
├── posts/                              # Blog posts organized by date
│   ├── YYYY-MM-DD-post-slug/           # Each post in its own folder
│   │   ├── content.md                  # Markdown source
│   │   ├── featured.jpg                # Featured image (optimized)
│   │   ├── *.png                       # Original generated images
│   │   ├── *-blocks.html               # Gutenberg blocks (generated)
│   │   └── meta.json                   # WordPress metadata (post ID, SEO, etc.)
│   └── ...
├── wp-media-upload.py                  # WordPress publishing CLI
├── image-crop.py                       # Image processing CLI
├── .env                                # Credentials (not committed)
└── CLAUDE.md                           # Claude Code context file
```

Post folders are named `YYYY-MM-DD-slug` for chronological sorting. The `meta.json` file stores WordPress post ID, slug, dates, and SEO metadata for future edits.

## Why This Approach?

**Speed** - Publishing a full post with custom imagery takes minutes, not hours.

**Consistency** - Same workflow every time. No forgetting to set alt text or featured images.

**Extensibility** - Adding new capabilities means writing a Python function, not learning another tool's UI.

**AI-Native** - Built for how AI assistants work—text in, actions out.

## Related

- [Claude Code First Development](https://www.mattwarren.co/2026/01/claude-code-first-development/) - Building systems that AI can operate
- [save.cooking](https://save.cooking) - A side project built entirely with AI assistance

## License

MIT
