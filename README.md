# skill-plex.d-mcknight

An MVP for playing music from [Plex](https://plex.tv) on your Neon or OpenVoice OS device via [OCP](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin).

## Usage

Since this is an OCP skill, your music voice requests will automatically search your Plex music library. You can also search from the GUI on the OCP dashboard.

Please note that precedence matters in OCP - by default, this skill will not be highest precedence. If you want to search your Plex library before other OCP skills you'll need to configure it to have higher precedence. See the OCP documentation for more details.

## Installation

### Neon Mark 2

```shell
cd ~/.config/.local/share/neon/skills
git clone https://github.com/d-mcknight/skill-plex
mv skill-plex skill-plex.d-mcknight

mkdir config/neon/skills/skill-plex.d-mcknight
touch ~/.config/neon/skills/skill-plex.d-mcknight/settings.json
cat <<EOF > ~/.config/neon/skills/skill-plex.d-mcknight/settings.json
{
    "__mycroft_skill_firstrun": false,
    "token": "REPLACE"
}
EOF
```

Visit https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/ for instructions on finding your Plex token.
It should look something like `ys738s6uPWXpwabc4sRYe`.
Enter your token in `~/.config/neon/skills/skill-plex.d-mcknight/settings.json` where it says `REPLACE`.

Finally, `sudo systemctl restart neon-skills`.

## Neon containers

Edit `docker/neon/neon.yaml` and add a default skill:

```
default-skills:
    - https://github.com/d-mcknight/skill-plex
```

Restart the `neon-skills` container, then edit `docker/xdg/config/neon/skills/skill-plex.d-mcknight/settings.json`. Add a `token` entry per the Mark 2 instructions above.
