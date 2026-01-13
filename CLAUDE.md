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

# Create post with featured image
uv run wp-media-upload.py create-post --title "Post Title" --file ./content.html --status publish --featured-media 1234

# Set featured image on existing post
uv run wp-media-upload.py set-featured --post-id 1234 --media-id 5678
```

**Required Environment Variables (.env):**
- `WP_SITE_URL` - Must use `https://www.mattwarren.co` (www required for auth)
- `WP_USERNAME` - WordPress username
- `WP_APP_PASSWORD` - Application password (with spaces, can be quoted)

### Content Format

Blog posts are stored in `wordpress-posts/`:
- `.md` files: Source markdown drafts
- `-blocks.html` files: Gutenberg block format for WordPress publishing

Post content must be converted to Gutenberg blocks before publishing. Key block types:
- `<!-- wp:paragraph -->` for text
- `<!-- wp:heading -->` or `<!-- wp:heading {"level":3} -->` for headings
- `<!-- wp:code -->` for code blocks
- `<!-- wp:list -->` for bullet lists

### Image Generation

Hero images use the nano-banana-pro skill with Gemini. For 16:9 images:
1. Generate with `--aspect landscape`
2. Crop to exact 16:9 with PIL if needed
3. Convert to JPG for smaller file size

## MCP Integration

WordPress MCP server is available but lacks media upload and featured image support. Use `wp-media-upload.py` to work around these limitations.
