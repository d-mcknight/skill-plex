# skill-plex.d-mcknight

An MVP for playing music from [Plex](https://plex.tv) on your Neon or OpenVoice OS device via [OVOS Common Play (OCP)](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin).

## Usage

Since this is an OCP skill, your music voice requests will automatically search your Plex music library. You can also search from the GUI on the OCP dashboard.

Please note that precedence matters in OCP - by default, this skill will not be highest precedence. If you want to search your Plex library before other OCP skills you'll need to configure it to have higher precedence. See the OCP documentation for more details.

Also, due to the way OCP handles intent matching, the Plex skill will return more confident results if you ask for a media type explicitly. For example you might say "play the movie Ghostbusters" to make sure you get back a movie result instead of a soundtrack or TV show. This skill also significantly boosts its confidence score if you include the word Plex in your request: "play music by Charles Mingus on Plex."

_Note: The assumption with users of the Plex skill is that they would want to default Plex, so the base confidence score is 75/100. Asking for Plex specifically boosts that base score to 90._

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

Edit `docker/config/neon.yaml` and add a default skill:

```yaml
skills:
  default-skills:
    - https://github.com/d-mcknight/skill-plex
```

Restart the `neon-skills` container, then edit `docker/xdg/config/neon/skills/skill-plex.d-mcknight/settings.json`. Add a `token` entry per the Mark 2 instructions above.
