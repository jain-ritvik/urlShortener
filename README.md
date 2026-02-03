# Flask URL Shortener

A simple URL shortener application built using Flask. It allows users to enter a long URL and receive a shortened version that redirects to the original URL.

## Features

- Shortens long URLs into a 6-character code
- Redirects short URLs to original URLs
- Validates URLs to ensure they start with http:// or https://
- Lightweight and easy to understand

## Technologies Used

- Python 3
- Flask
- HTML (Jinja2 Templates)

## How It Works

- User submits a URL from the home page
- A random 6-character short code is generated
- The shortened URL is displayed
- Visiting the short URL redirects to the original URL

## Limitations

- URLs are stored in memory and might be lost when the app restarts
- No database integration
- Made for learning purpose and currently not suitable for production use
