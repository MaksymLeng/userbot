# Telegram Channel UserBot

A lightweight **Telegram userbot** (based on [Telethon](https://github.com/LonamiWebs/Telethon)) that sits inside a channel **as an admin account**, greets every new member once with a custom text and/or media file, and points them to your manager.

> **Why a *user*‑bot?**  Telegram’s official Bot API can’t see join‑events in private channels, while a user account that’s promoted to *admin* can.  This project automates that account so you get the same onboarding flow you’d expect from a classic bot.

---

## ✨ Features

* **Multi‑account support** – spin up several userbots from a single process by listing them in `bots.json`.
* **Welcome message** – attach any *video / photo / animation* **or** plain text.
* **Smart spam‑protection** – keeps a small per‑channel cache so each member is greeted only once.
* **10‑second polling** – lightweight loop without webhooks or extra infra.
* **100 % Python 3.11 & async** – no external services or databases.

---

## 🔧 Requirements

| Requirement                                             | Tested version |
| ------------------------------------------------------- | -------------- |
| Python                                                  | **3.11**       |
| [Telethon](https://pypi.org/project/Telethon)           | 1.34 +         |
| [python‑dotenv](https://pypi.org/project/python-dotenv) | 1.0 +          |

Install the two libraries with:

```bash
pip install -r requirements.txt
```

`requirements.txt` (ready to commit):

```text
telethon>=1.34.0
python-dotenv>=1.0.0
```

---

## 📥 Installation

```bash
git clone https://github.com/MaksymLeng/userbot.git
cd userbot
python -m venv venv && source venv/bin/activate  # optional but recommended
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. **Create a Telegram *API ID* and *API Hash*.**  Follow the official guide [https://my.telegram.org/apps](https://my.telegram.org/apps).
2. **Log in once to create a session file.**  Either run `Telethon`’s interactive login or let the helper below do it.
3. **Populate `.env`** (not committed to Git):

   ```env
   API_ID=123456
   API_HASH=0123456789abcdef0123456789abcdef
   SESSION=my_session  # will become my_session.session
   ```
4. **Find your channel’s `channel_id` & `access_hash`.**

   ```bash
   python get_channels.py
   ```

   The script prints a table of channels the account can access; copy the two numbers you need.
5. **Edit `bots.json`.**  Use the template below – *one object per account*:

   ```json
   [
     {
       "session": "my_session",
       "api_id": 123456,
       "api_hash": "0123456789abcdef0123456789abcdef",
       "channel_id": 1000000000000,
       "access_hash": 1234567890123456789,
       "media": "assets/welcome_video.mp4",
       "text": "Hi! 👋 Please write to our manager within the next 5 minutes to unlock your first bonus.",
       "manager_url": "https://t.me/your_manager"
     }
   ]
   ```

   *Feel free to replace `media` with any local file – photo, video, GIF, etc.  Leave the field blank (`""`) to send only text.*

---

## 🚀 Running

```bash
python userbot_manager.py
```

The script will spin up every entry in `bots.json`, monitor their channels, and create / update `users_<session>.json` (a local cache of greeted members).

Run it inside `tmux`, `screen`, or a systemd service for uninterrupted operation.

---

## 🛠  Cleaning Sensitive Data (important!)

If you accidentally committed **real** API credentials or sessions, simply deleting them in a new commit is *not* enough – they stay visible in Git history.

### Rewriting history with **git‑filter‑repo** (recommended)

```bash
pip install git-filter-repo  # one-time

# From the root of your repo:
git filter-repo --path bots.json --replace-text <(echo 'dcb32f17553f7944cb59d1e764bc44b5==REDACTED')
# or, to strip the entire file from every commit:
# git filter-repo --path bots.json --invert-paths

git push --force  # WARNING: this rewrites the public history
```

Alternatively use [BFG Repo‑Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) if you prefer Java.

> After a force‑push, anyone who cloned the old history must re‑clone or run the same filter themselves.

---

## 🐞 Troubleshooting

| Symptom                          | Cause / Fix                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| `telethon.errors.FloodWaitError` | Telegram rate‑limited you. Increase the sleep interval in `userbot_manager.py` or wait. |
| `bots.json is malformed`         | Validate your JSON with an online linter – trailing commas are illegal.                 |
| Media not sent                   | Check `media` path and file type.                                                       |

---

## 🤝 Contributing

Have an idea or found a bug? Open an issue or PR – all constructive help is welcome.

---

## 📄 License

**No license specified.**  All rights reserved by the author.
