#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///
"""
WordPress CLI Tools

Manage WordPress posts, media, and metadata from the command line.

Commands:
    upload        - Upload media to WordPress
    create-post   - Create a new post with optional featured image
    set-featured  - Set featured image on existing post
    fetch-meta    - Fetch metadata for an existing post

Usage:
    uv run wp-media-upload.py upload --image /path/to/image.png --title "Image Title"
    uv run wp-media-upload.py create-post --title "Post Title" --file content.html --status publish
    uv run wp-media-upload.py fetch-meta --post-id 1234 --output ./posts/2026-01-13-my-post/

Environment variables (can be set in .env):
    WP_SITE_URL - WordPress site URL (e.g., https://www.mattwarren.co)
    WP_USERNAME - WordPress username
    WP_APP_PASSWORD - WordPress application password
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


def upload_media(site_url: str, username: str, app_password: str, image_path: str, title: str | None = None) -> dict:
    """Upload an image to WordPress and return the media details."""

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Determine content type
    suffix = image_path.suffix.lower()
    content_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    content_type = content_types.get(suffix, 'application/octet-stream')

    # Prepare the upload
    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/media"

    filename = image_path.name
    if title is None:
        title = image_path.stem.replace('-', ' ').replace('_', ' ').title()

    # Create explicit Basic auth header
    credentials = f"{username}:{app_password}"
    token = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
    }

    # Verify auth works first
    auth_check = requests.get(
        f"{site_url.rstrip('/')}/wp-json/wp/v2/users/me",
        headers=headers,
        timeout=30,
    )
    if auth_check.status_code != 200:
        try:
            err_detail = auth_check.json().get('message', auth_check.text[:200])
        except:
            err_detail = auth_check.text[:200]
        raise Exception(f"Authentication failed ({auth_check.status_code}): {err_detail}")
    print(f"Authenticated as: {auth_check.json().get('name', 'unknown')}", file=sys.stderr)

    # Use multipart form data upload
    with open(image_path, 'rb') as f:
        files = {
            'file': (filename, f, content_type),
        }
        form_data = {
            'title': title,
            'alt_text': title,
        }

        response = requests.post(
            api_url,
            headers=headers,
            files=files,
            data=form_data,
            timeout=120,
        )

    # Debug output
    print(f"Response status: {response.status_code}", file=sys.stderr)
    print(f"Response type: {response.headers.get('content-type', 'unknown')}", file=sys.stderr)

    if response.status_code == 201:
        data = response.json()
        return {
            'id': data['id'],
            'url': data['source_url'],
            'title': data['title']['rendered'],
            'slug': data['slug'],
        }
    else:
        # Try to parse error message
        try:
            err = response.json()
            msg = err.get('message', response.text[:500])
        except:
            msg = response.text[:500]
        raise Exception(f"Upload failed ({response.status_code}): {msg}")


def create_post(site_url: str, username: str, app_password: str, title: str, content: str, status: str = 'draft', featured_media: int | None = None) -> dict:
    """Create a WordPress post."""

    credentials = f"{username}:{app_password}"
    token = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
    }

    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"

    payload = {
        'title': title,
        'content': content,
        'status': status,
    }
    if featured_media:
        payload['featured_media'] = featured_media

    response = requests.post(
        api_url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    if response.status_code == 201:
        data = response.json()
        return {
            'id': data['id'],
            'title': data['title']['rendered'],
            'status': data['status'],
            'link': data['link'],
            'slug': data['slug'],
            'featured_media': data.get('featured_media', 0),
            'date': data['date'],
            'date_gmt': data['date_gmt'],
            'modified': data['modified'],
            'modified_gmt': data['modified_gmt'],
            'excerpt': data['excerpt']['rendered'].strip(),
            'author': data.get('author'),
            'categories': data.get('categories', []),
            'tags': data.get('tags', []),
        }
    else:
        try:
            err = response.json()
            msg = err.get('message', response.text[:500])
        except:
            msg = response.text[:500]
        raise Exception(f"Failed to create post ({response.status_code}): {msg}")


def set_featured_image(site_url: str, username: str, app_password: str, post_id: int, media_id: int) -> dict:
    """Set the featured image for a WordPress post."""

    credentials = f"{username}:{app_password}"
    token = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
    }

    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"

    response = requests.post(
        api_url,
        headers=headers,
        json={'featured_media': media_id},
        timeout=30,
    )

    if response.status_code == 200:
        data = response.json()
        return {
            'post_id': data['id'],
            'featured_media': data['featured_media'],
            'title': data['title']['rendered'],
        }
    else:
        try:
            err = response.json()
            msg = err.get('message', response.text[:500])
        except:
            msg = response.text[:500]
        raise Exception(f"Failed to set featured image ({response.status_code}): {msg}")


def fetch_post_metadata(site_url: str, username: str, app_password: str, post_id: int) -> dict:
    """Fetch full metadata for a WordPress post."""

    credentials = f"{username}:{app_password}"
    token = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
    }

    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"

    response = requests.get(
        api_url,
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        try:
            err = response.json()
            msg = err.get('message', response.text[:500])
        except:
            msg = response.text[:500]
        raise Exception(f"Failed to fetch post ({response.status_code}): {msg}")

    data = response.json()

    # Extract and structure the metadata
    metadata = {
        'wordpress': {
            'post_id': data['id'],
            'slug': data['slug'],
            'status': data['status'],
            'link': data['link'],
            'featured_media_id': data.get('featured_media', 0),
            'author_id': data.get('author'),
            'categories': data.get('categories', []),
            'tags': data.get('tags', []),
        },
        'content': {
            'title': data['title']['rendered'],
            'excerpt': data['excerpt']['rendered'].strip(),
        },
        'dates': {
            'created': data['date'],
            'modified': data['modified'],
            'created_gmt': data['date_gmt'],
            'modified_gmt': data['modified_gmt'],
        },
        'seo': {
            'meta_title': data.get('meta', {}).get('_seopress_titles_title', ''),
            'meta_description': data.get('meta', {}).get('_seopress_titles_desc', ''),
            'og_title': '',
            'og_description': '',
        },
        'meta_updated': datetime.utcnow().isoformat() + 'Z',
    }

    return metadata


def save_post_metadata(metadata: dict, output_path: Path) -> Path:
    """Save post metadata to a JSON file."""
    meta_file = output_path / 'meta.json'
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    return meta_file


def get_credentials():
    """Get WordPress credentials from environment."""
    load_dotenv()

    site_url = os.getenv('WP_SITE_URL', '').strip('"\'')
    username = os.getenv('WP_USERNAME', '').strip('"\'')
    app_password = os.getenv('WP_APP_PASSWORD', '').strip('"\'')

    missing = []
    if not site_url:
        missing.append('WP_SITE_URL')
    if not username:
        missing.append('WP_USERNAME')
    if not app_password:
        missing.append('WP_APP_PASSWORD')

    if missing:
        print(f"Error: Missing required configuration: {', '.join(missing)}", file=sys.stderr)
        print("\nSet these in your .env file.", file=sys.stderr)
        sys.exit(1)

    return site_url, username, app_password


def main():
    parser = argparse.ArgumentParser(
        description='WordPress CLI tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload media to WordPress')
    upload_parser.add_argument('--image', '-i', required=True, help='Path to image file')
    upload_parser.add_argument('--title', '-t', help='Title for the media (optional)')

    # Set featured image command
    featured_parser = subparsers.add_parser('set-featured', help='Set featured image for a post')
    featured_parser.add_argument('--post-id', '-p', type=int, required=True, help='Post ID')
    featured_parser.add_argument('--media-id', '-m', type=int, required=True, help='Media ID')

    # Create post command
    post_parser = subparsers.add_parser('create-post', help='Create a WordPress post')
    post_parser.add_argument('--title', '-t', required=True, help='Post title')
    post_parser.add_argument('--content', '-c', help='Post content (or use --file)')
    post_parser.add_argument('--file', '-f', help='Read content from file')
    post_parser.add_argument('--status', '-s', default='draft', choices=['draft', 'publish', 'pending'], help='Post status')
    post_parser.add_argument('--featured-media', '-m', type=int, help='Featured image media ID')
    post_parser.add_argument('--save-meta', help='Directory to save meta.json file')

    # Fetch metadata command
    fetch_parser = subparsers.add_parser('fetch-meta', help='Fetch metadata for existing post')
    fetch_parser.add_argument('--post-id', '-p', type=int, required=True, help='WordPress post ID')
    fetch_parser.add_argument('--output', '-o', required=True, help='Output directory for meta.json')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    site_url, username, app_password = get_credentials()

    try:
        if args.command == 'upload':
            result = upload_media(site_url, username, app_password, args.image, args.title)
            print(f"Upload successful!")
            print(f"  Media ID: {result['id']}")
            print(f"  URL: {result['url']}")
            print(f"  Title: {result['title']}")

        elif args.command == 'set-featured':
            result = set_featured_image(site_url, username, app_password, args.post_id, args.media_id)
            print(f"Featured image set!")
            print(f"  Post ID: {result['post_id']}")
            print(f"  Media ID: {result['featured_media']}")
            print(f"  Post Title: {result['title']}")

        elif args.command == 'create-post':
            content = args.content
            if args.file:
                with open(args.file, 'r') as f:
                    content = f.read()
            if not content:
                print("Error: Must provide --content or --file", file=sys.stderr)
                sys.exit(1)
            result = create_post(site_url, username, app_password, args.title, content, args.status, args.featured_media)
            print(f"Post created!")
            print(f"  Post ID: {result['id']}")
            print(f"  Title: {result['title']}")
            print(f"  Status: {result['status']}")
            print(f"  Link: {result['link']}")
            if result['featured_media']:
                print(f"  Featured Media: {result['featured_media']}")

            # Save metadata if requested
            if args.save_meta:
                metadata = {
                    'wordpress': {
                        'post_id': result['id'],
                        'slug': result['slug'],
                        'status': result['status'],
                        'link': result['link'],
                        'featured_media_id': result['featured_media'],
                        'author_id': result['author'],
                        'categories': result['categories'],
                        'tags': result['tags'],
                    },
                    'content': {
                        'title': result['title'],
                        'excerpt': result['excerpt'],
                    },
                    'dates': {
                        'created': result['date'],
                        'modified': result['modified'],
                        'created_gmt': result['date_gmt'],
                        'modified_gmt': result['modified_gmt'],
                    },
                    'seo': {
                        'meta_title': '',
                        'meta_description': '',
                        'og_title': '',
                        'og_description': '',
                    },
                    'meta_updated': datetime.utcnow().isoformat() + 'Z',
                }
                meta_path = save_post_metadata(metadata, Path(args.save_meta))
                print(f"  Metadata: {meta_path}")

        elif args.command == 'fetch-meta':
            metadata = fetch_post_metadata(site_url, username, app_password, args.post_id)
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            meta_path = save_post_metadata(metadata, output_dir)
            print(f"Metadata saved!")
            print(f"  Post ID: {metadata['wordpress']['post_id']}")
            print(f"  Title: {metadata['content']['title']}")
            print(f"  File: {meta_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
