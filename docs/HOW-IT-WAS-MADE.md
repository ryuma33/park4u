# How the park4u prototype was made

A beginner's guide to `index.html`. The line numbers point to that file, so open it in VS Code next to this guide (it's in the main project folder) (press `Ctrl+G` in VS Code to jump to a line).

---

## 1. The big idea: one file, three languages

The whole app is **one HTML file**. A browser understands three languages, and this file uses all three:

| Language | What it does | Where in the file |
|---|---|---|
| **HTML** | The *things* on the screen: text, buttons, input boxes | the `<section>` blocks (from line ~272) |
| **CSS** | How those things *look*: colours, sizes, rounded corners, animations | inside `<style>` (lines ~14–260) |
| **JavaScript (JS)** | What things *do*: clicking, switching screens, the timer, saving data | inside `<script>` (from line 544) |

Think of a house: HTML is the walls and furniture, CSS is the paint and decoration, and JavaScript is the electricity that makes things work.

There's **no server, no database and no app store**. The browser runs everything. That's why it's called a *prototype*: it looks and feels like the app, but nothing real happens behind it.

---

## 2. How it was rebuilt from your old video

1. **The video had no screenshots**, so I used a Python library called **OpenCV** to pull pictures (frames) out of `park4u.mp4`. The script compared each frame with the one before it and saved a picture whenever the screen changed a lot. The script is `tools/extract_frames.py`. The pictures it made stay on your computer (in `frames/` and `screens/`) and aren't uploaded to GitHub, because they're large.
2. I looked at every frame and wrote down each screen and which button leads where. That list is `docs/SCREENS.md`.
3. You confirmed the list, and I built each screen in HTML and copied the text and sample data (D 777, AED 8, Etisalat, 61161…) from the frames.
4. Then came three rounds of design changes you asked for: a nicer look, removing the fingerprint, and the iPhone style.

**Lesson:** start from a *screen list + navigation map* before writing any code. It's the plan for the whole app.

---

## 3. HTML: every screen is a `<section>`

Each screen of the app is one block like this (the login screen is at line 272):

```html
<section class="screen" id="login">
  ... the things on the login screen ...
</section>
```

- `id="login"` is the screen's **name**, so JavaScript can find it.
- `class="screen"` is a **label** that lets CSS style all screens the same way.

All 19 screens sit in the file at the same time, stacked on top of each other. **Only one is visible at once.** CSS hides all of them (`display:none`, line 46), and the visible one gets an extra class `on` that shows it.

Inside a screen you'll see normal HTML tags:

```html
<label class="cell inp"><span class="k">Username</span><input id="lpUser" placeholder="Required"></label>
<button class="btn" id="lpBtn">Sign In</button>
```

- `<input>` is a box you can type in, and `placeholder` is the grey hint text.
- `<button>` is something you can click.
- `id="lpBtn"` lets JavaScript say "when *this* button is clicked, do something".
- Some buttons have `data-go="signup"`. That's a little note to JavaScript meaning "open the signup screen" (more in section 5).

---

## 4. CSS: making it look like an iPhone

### Colour variables (line 15)
At the top of the CSS, all the colours are given names:

```css
:root{
  --bg:#000;        /* black background */
  --g1:#1c1c1e;     /* grey of the rounded boxes */
  --tint:#ff375f;   /* the pink accent colour */
}
```

Everywhere else uses `var(--tint)` instead of typing `#ff375f`. **Change one line here and the whole app's pink changes.** Try it: set `--tint` to `#0a84ff` (blue) and refresh.

These exact colours come from Apple's iOS dark-mode colours, which is a big part of why it feels like an iPhone.

### Classes are reusable styles
`.btn` (line 91) styles every big pink button. `.group` (line 73) makes the rounded grey boxes from iPhone Settings. Write a style once and reuse it on many elements.

### Flexbox lays things out
You'll see `display:flex` a lot. It lines things up in a row or column and spaces them out. For example, a screen is a column: nav bar on top, scrolling content in the middle, buttons at the bottom.

### The iPhone frame (line 32) vs a real phone (line 38)
`.phone` draws the rounded iPhone shape with the Dynamic Island. Then this rule:

```css
@media (max-width:500px){ ... }
```

means "**if the screen is narrower than 500px** (a real phone), make the app full-screen and hide the fake frame". This is called **responsive design**: one file looks right on a laptop *and* a phone.

### Animations
`@keyframes pushIn` slides a screen in from the right, just like iOS. `@keyframes pop` makes the green tick "pop" in. An animation just says what the element looks like `from` the start `to` the end, and the browser draws the frames in between.

### Fonts (line 13)
Google Fonts loads **Inter**. The font list `-apple-system, ..., Inter` means "use Apple's own font on iPhones and Macs; otherwise use Inter".

---

## 5. JavaScript: making it work

### Finding things: `$('#lpBtn')`
Near the top there's a tiny helper, `$`. `$('#lpBtn')` means "find the element whose id is lpBtn". The `#` means "id".

### Reacting to clicks (line 739)
```js
$('#lpBtn').onclick = async () => {
  if (!$('#lpUser').value.trim() || !$('#lpPass').value) return toast('Enter your username and password.');
  await busy(600);       // show the spinning wheel for 0.6 s
  goRoot('home');        // go to the map screen
};
```
In plain English: *when Sign In is clicked, check both boxes are filled; if not, show a message; if yes, show a spinner, then open Home.* That's the core idea of all front-end code: **wait for an event → check something → change the screen**.

### Switching screens: `render`, `go` and `back` (lines 607–620)
- `render('home')` hides every screen and adds the class `on` to the one called `home`.
- `go('cards')` *remembers* where you were (in a list called `stack`) and then shows the new screen.
- `back()` goes back to the previous screen in the `stack`.
- `history.pushState` + the `popstate` listener (line 619) make your **phone's back button / swipe** work too.

The click listener at line 620 is a shortcut. Instead of wiring every button by hand, it watches *all* clicks, and if the clicked thing has `data-go="xyz"` it calls `go('xyz')`. That's why adding `data-go="summary"` to a button is enough to make it open the Summary screen.

### Doing setup when a screen opens: `enter`
`enter` (line 726) is a list of "things to do when screen X opens". For example, `enter.timer` starts the countdown and `enter.cards` draws your cards. `render()` calls these automatically.

### Data: `state` and `localStorage` (lines 572–590)
All the app's data lives in one object called `state`: your account, cards, parking history and the current parking session.

```js
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){} }
```
**localStorage** is a small storage box inside the browser. `JSON.stringify` turns the data into text so it can be stored there. This is why your account details and parking history are still there after you refresh. It's wrapped in `try/catch` because some browsers (private mode) block it, and then the app just keeps the data in memory instead of crashing.

### The parking spots (line 592)
`SPOTS` is a list (an *array*) of objects, one per parking place:
```js
{ id:61161, name:'Sheikh Zayed Rd', price:4, op:'Etisalat', dist:'3mins', x:.74, y:.20 }
```
`x` and `y` say where the pin sits on the map (0.74 = 74% from the left). The map pins, search results and route screen are all built from this one list. **Add an object here and a new pin appears.**

### Building HTML from data
Lists like Activity are made with code. For example, `renderActivity` (line 799) loops over your parking history and builds one row per item using **template strings** (text in backticks with `${...}` holes):
```js
`<span class="grow">${a.place}<small>${a.detail}</small></span>`
```
`esc()` is used on text that users type, so a name like `<b>` can't break the page. (This is a basic security habit.)

### The maps and QR codes are drawn with code
No map images are used. `homeMapSVG` (line 653) and `routeMapSVG` (line 686) build **SVG**, which is a way to draw shapes (lines, circles, text) with code. The streets are drawn by a loop with a "random" generator that has a fixed **seed**, so the "random" map comes out the same every time. `qrSVG` (line 715) draws a QR-*looking* pattern the same way (it can't actually be scanned).

### Timers: the drive and the countdown
- **Driving** (`enter.nav`, line 863): `setInterval` runs a small function every 120 ms that moves the blue car dot a bit along the route and updates "290 m / 2 min". When it reaches the end, it opens "Destination Reached".
- **Time Left** (`tick`, line 910): runs every second, works out `end time − now`, and shows it as `HH:MM:SS`. The pink ring shrinks using `stroke-dashoffset`, which controls how much of the circle's outline is drawn.

### The fake payment (line 896)
`payBtn` shows a spinner, adds the parking to your history, starts a 2-hour session and opens "Payment Done". **No money and no card details go anywhere.** A real app would send this to a payment company's server instead.

---

## 6. Ideas to practise (easy → harder)

1. Change the pink colour by editing `--tint` (line 19).
2. Change the text "Find parking with the help of cameras." on the login screen.
3. Add a new parking spot to `SPOTS` with your own name, price and `x`/`y`, then find its pin on the map.
4. Change the parking length from 2 hours: look for `PARK_HOURS` (line 604).
5. Make "Forgot Password?" open a new screen: copy a small `<section>` such as `thanks`, give it a new `id`, and add `data-go="yourId"` to the button.
6. Harder: add a 4th option "4 hr" to the Extend buttons on the Time Left screen.

**Tips:**
- Right-click the page → **Inspect** opens the browser's developer tools. The **Elements** tab shows the HTML and CSS live, so you can change colours there to experiment. The **Console** tab shows JavaScript errors.
- After editing, save the file and refresh the browser.
- If something breaks, the Console usually tells you the line number.

---

## 7. Words you'll hear

| Word | Meaning |
|---|---|
| **Prototype** | A clickable model of an app that looks real but has no real backend |
| **Front-end** | What runs on the phone or browser (this file) |
| **Back-end / server** | The computer on the internet that stores real data and does real work (cameras, payments). This project doesn't have one yet |
| **Element** | One HTML thing, e.g. a button |
| **Class / id** | Labels on elements. A class is shared by many elements; an id is unique to one |
| **Event** | Something that happens, like a click or a key press |
| **Function** | A named set of steps you can run again and again |
| **Array / object** | A list of things / a thing with named properties |
| **localStorage** | A small storage box in the browser |
| **SVG** | Pictures drawn with code (shapes) instead of pixels |
| **Responsive** | Adjusts to different screen sizes |

---

## 8. Next steps toward a real app

- **Real map:** swap the drawn SVG maps for a map library such as **Leaflet** (free) or **Google Maps**.
- **Real accounts and data:** a back-end like **Firebase** or **Supabase** (both have free tiers) for logins and saving parking history.
- **The camera part (the heart of park4u):** cameras send pictures to a server, and an AI model such as **YOLO** (the same kind you used for weapon detection) decides whether each parking space is free or taken. The app then asks the server "which spots are free?" and draws those pins.
- **Android/iPhone app:** wrap this web app with **Capacitor** to get an installable app, or rebuild it in **Flutter** later.
