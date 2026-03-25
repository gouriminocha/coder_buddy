# Personal Webpage Project

## Project Overview

This is a simple, responsive personal webpage that showcases a biography, skill set, and a portfolio of projects. It includes a light/dark theme toggle and is built using only static assets (HTML, CSS, and a tiny amount of JavaScript). The site is designed to be easy to host on any static‑site provider such as GitHub Pages, Netlify, or Vercel.

## Feature List

- **Responsive layout** – works on mobile, tablet, and desktop.
- **Theme toggle** – switch between light and dark modes; the preference is saved in `localStorage`.
- **Biography section** – a short intro with a profile picture.
- **Skills list** – displayed as badges.
- **Project cards** – each card contains an image, title, description, and links.
- **Easy customization** – all content is plain HTML; no build step required.
- **Static‑only** – no server‑side code, perfect for static hosting.

## Tech Stack & Rationale

| Technology | Reason for Choice |
|------------|-------------------|
| **HTML5** | Semantic markup, no framework needed. |
| **CSS3 (Flexbox & Grid)** | Provides a modern, responsive layout without extra libraries. |
| **Vanilla JavaScript** | Small amount of interactivity (theme toggle) without pulling in a heavy framework. |
| **Git** | Version control and easy deployment to static hosts. |

The stack keeps the project lightweight, fast to load, and simple to maintain.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository‑url>
   cd personalwebpage
   ```

2. **Folder Structure**
   ```
   personalwebpage/
   ├─ index.html          # Main page
   ├─ assets/             # Images, icons, etc.
   │   ├─ profile.jpg
   │   └─ project‑1.png
   ├─ styles/
   │   └─ style.css       # All CSS, including theme variables
   └─ README.md           # This documentation
   ```

   - **Images**: Place any new images inside the `assets/` folder and reference them with a relative path (e.g., `assets/my‑photo.jpg`).

3. **Open locally**
   - Simply open `index.html` in a web browser (double‑click the file or `open index.html` from the command line). No server is required.

## Deployment to Static Hosts

### GitHub Pages
1. Commit all changes to the `main` (or `master`) branch.
2. Create a `gh-pages` branch:
   ```bash
   git checkout -b gh-pages
   git push origin gh-pages
   ```
3. In the repository settings, enable **GitHub Pages** and set the source to the `gh-pages` branch.
4. Your site will be available at `https://<username>.github.io/<repo-name>/`.

### Netlify
1. Sign in to Netlify and click **New site from Git**.
2. Connect your repository and set the **build command** to `npm run build` (or leave blank) and the **publish directory** to `/`.
3. Netlify will automatically deploy the site on each push to the default branch.

### Vercel
1. Install the Vercel CLI (`npm i -g vercel`) or use the Vercel dashboard.
2. Run `vercel` in the project root and follow the prompts, selecting the root directory as the deployment source.
3. Vercel will host the site and provide a preview URL for every commit.

## Customizing Content

### Editing Biography Text
- Open `index.html` and locate the `<section id="about">` block. Replace the placeholder paragraph with your own biography.

### Adding / Removing Skills
- Skills are rendered as `<span class="skill-badge">Skill</span>` inside the `<div class="skills">` container. Add or delete `<span>` elements to modify the list.

### Adding Project Cards
1. Find the `<section id="projects">` container.
2. Copy the existing card markup:
   ```html
   <div class="project-card">
       <img src="assets/project‑1.png" alt="Project 1" />
       <h3>Project Title</h3>
       <p>Short description of the project.</p>
       <a href="#" class="btn">Live Demo</a>
       <a href="#" class="btn">Source Code</a>
   </div>
   ```
3. Paste it below the other cards and update the image path, title, description, and links.

### Updating Images
- Place new images in the `assets/` folder.
- Reference them with a relative path in the HTML (e.g., `src="assets/new‑image.png"`).
- For the profile picture, replace `assets/profile.jpg` with your own image and keep the same filename or update the `<img>` `src` attribute accordingly.

## Theme Toggle Implementation

The toggle button is defined in `index.html` and wired up by `script.js` (included at the bottom of the page). The script:
1. Reads the current theme from `localStorage`.
2. Adds either `data-theme="light"` or `data-theme="dark"` to the `<html>` element.
3. Updates the button label.

### Modifying Color Variables
All colors are defined as CSS custom properties in `styles/style.css` under the `[data-theme="light"]` and `[data-theme="dark"]` selectors. Example:
```css
[data-theme="light"] {
    --bg-color: #ffffff;
    --text-color: #222222;
    --primary-color: #0066ff;
}
[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #f0f0f0;
    --primary-color: #3399ff;
}
```
- Change the hex values to suit your branding.
- Adding new variables is safe; just reference them elsewhere with `var(--your-variable)`.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Contact

- **Name**: Your Name
- **Email**: your.email@example.com
- **GitHub**: https://github.com/your‑username

Feel free to open issues or submit pull requests for improvements!
