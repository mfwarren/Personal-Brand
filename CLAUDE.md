# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal brand content management workspace for mattwarren.co. It contains blog post drafts, generated images, and CLI tools for publishing to WordPress.

## WordPress Publishing Workflow

### CLI Tool: wp-media-upload.py

Run with `uv run wp-media-upload.py <command>`. Requires `.env` with WordPress credentials.

**Commands:**
```bash
# Upload image and get media ID
uv run wp-media-upload.py upload --image ./image.jpg --title "Image Title"

# Create post with featured image and save metadata
uv run wp-media-upload.py create-post --title "Post Title" --file ./content.html --status publish --featured-media 1234 --save-meta ./posts/2026-01-13-my-post/

# Set featured image on existing post
uv run wp-media-upload.py set-featured --post-id 1234 --media-id 5678

# Fetch metadata for existing post
uv run wp-media-upload.py fetch-meta --post-id 1234 --output ./posts/2026-01-13-my-post/
```

**Required Environment Variables (.env):**
- `WP_SITE_URL` - Must use `https://www.mattwarren.co` (www required for auth)
- `WP_USERNAME` - WordPress username
- `WP_APP_PASSWORD` - Application password (with spaces, can be quoted)

### Content Format

Blog posts are stored in `posts/YYYY-MM-DD-post-slug/` folders:
- `content.md` - Source markdown draft
- `featured.jpg` - Optimized featured image for WordPress
- `*.png` - Original generated images (high-res)
- `*-blocks.html` - Gutenberg block format for WordPress publishing
- `meta.json` - WordPress metadata (post ID, slug, dates, SEO fields)

Folder naming uses ISO date prefix for chronological sorting.

### Metadata Schema (meta.json)

```json
{
  "wordpress": {
    "post_id": 1234,
    "slug": "post-slug",
    "status": "publish",
    "link": "https://...",
    "featured_media_id": 5678,
    "author_id": 1,
    "categories": [1],
    "tags": []
  },
  "content": {
    "title": "Post Title",
    "excerpt": "..."
  },
  "dates": {
    "created": "2026-01-13T12:00:00",
    "modified": "2026-01-13T12:00:00"
  },
  "seo": {
    "meta_title": "",
    "meta_description": ""
  }
}
```

Post content must be converted to Gutenberg blocks before publishing. Key block types:
- `<!-- wp:paragraph -->` for text
- `<!-- wp:heading -->` or `<!-- wp:heading {"level":3} -->` for headings
- `<!-- wp:code -->` for code blocks
- `<!-- wp:list -->` for bullet lists

### Image Generation

Hero images use the nano-banana-pro skill with Gemini. For 16:9 images:
1. Generate with `--aspect landscape`
2. Crop to exact 16:9 and convert to JPG:

```bash
uv run image-crop.py hero.png --aspect 16:9 --output hero.jpg
```

**image-crop.py options:**
- `-a, --aspect` - Target ratio (default: 16:9)
- `-o, --output` - Output file (default: adds -WxH suffix, converts to .jpg)
- `-q, --quality` - JPEG quality 1-100 (default: 90)

## MCP Integration

WordPress MCP server is available but lacks media upload and featured image support. Use `wp-media-upload.py` to work around these limitations.
