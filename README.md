# park4u 🅿️

**Find parking with the help of cameras.**

park4u is a mobile app idea from our school days: cameras watch parking spaces, and the app shows drivers where the free spots are, guides them there and lets them pay. The original prototype was lost, so it was rebuilt from the old demo video as a working, clickable prototype in iPhone style.

> ⚠️ This is a **prototype**. Maps and parking data are sample data, and **payments are fake**: no money moves and no card or UPI details are collected.

## ▶️ Try it

- **Online:** turn on GitHub Pages (see below), then open `https://ryuma33.github.io/park4u/`
- **On your computer:** download the project and double-click `index.html`. No installation needed.
- **On your phone:** open the GitHub Pages link. In Safari you can tap **Share → Add to Home Screen** to use it like a real app.

## ✨ Features

- 🗺️ **Map of camera-monitored parking** with prices on every pin
- 🔍 **Search** for a destination and see parking suggestions
- 🧭 **Route + parking info**: price, type, operator, distance, spot ID
- 🚗 **Simulated navigation** with a live distance and time countdown
- 💳 **Mock payment** with a saved card or UPI, then a QR receipt
- ⏱️ **Parking timer** with a countdown ring and an option to **extend** by 1–3 hours
- 👤 Account details, password change, saved cards (Wallet style), QR parking pass, monthly activity summary, feedback
- 💾 Data is saved in the browser (`localStorage`), so it's still there after a refresh

## 📱 Screens

Sign In · Create Account · Home map · Menu · Search · Route · Navigation · Destination Reached · Parking Reached · Summary · Payment Done · Time Left · Parking Extended · Account · Change Password · Activity · Cards · Verification Code · QR Code · Feedback · Thanks

The full list, with how each screen connects to the others, is in [docs/SCREENS.md](docs/SCREENS.md).

## 🛠️ Built with

- **HTML, CSS and JavaScript** in a single file ([index.html](index.html)), with no frameworks and no build step
- **SVG** drawn with code for the maps, icons and QR codes
- **Inter** font from Google Fonts (iPhones use Apple's own SF font)
- **Python + OpenCV** ([tools/extract_frames.py](tools/extract_frames.py)) to pull the original screens out of the demo video

## 📂 Project structure

```
park4u/
├── index.html              ← the whole app (HTML + CSS + JavaScript)
├── docs/
│   ├── HOW-IT-WAS-MADE.md  ← beginner guide to how the code works
│   └── SCREENS.md          ← every screen and how they connect
└── tools/
    └── extract_frames.py   ← pulls screens out of the demo video
```

## 🌐 Put it online with GitHub Pages (free)

1. On GitHub, open the repository → **Settings** → **Pages**.
2. Under **Branch**, choose `main` and `/ (root)`, then click **Save**.
3. Wait about a minute, and the app will be live at `https://ryuma33.github.io/park4u/`.

## 📖 Learn how it works

New to web development? Read **[docs/HOW-IT-WAS-MADE.md](docs/HOW-IT-WAS-MADE.md)**. It explains the code step by step and has practice exercises.

## 🚀 Roadmap: toward a real app

- [ ] Real maps (Leaflet or Google Maps) and GPS
- [ ] Back-end for accounts and parking history (Firebase or Supabase)
- [ ] **Camera detection:** a YOLO model that marks each parking space as free or taken and sends live counts to the app
- [ ] Real payments through a payment gateway (card + UPI)
- [ ] Android/iOS app using Capacitor, or a rebuild in Flutter

## 👥 Team (original school project)

- Althaf Nezam
- Atef Ul Hassan
- Hayden Jojo
- Sulthan Noushad
