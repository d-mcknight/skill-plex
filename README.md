# skill-plex.d-mcknight

An MVP for playing music from [Plex](https://plex.tv) on your Neon or OpenVoice OS device via [OVOS Common Play (OCP)](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin).

## Usage

**NOTE**: This skill currently only supports the `simple` OCP audio plugin, which requires a GUI. If you are using it on a Mark 1 or other device without a GUI it will probably not work.

Since this is an OCP skill, your music voice requests will automatically search your Plex music library. You can also search from the GUI on the OCP dashboard.

Please note that precedence matters in OCP - by default, this skill will not be highest precedence. If you want to search your Plex library before other OCP skills you'll need to configure it to have higher precedence. See the OCP documentation for more details.

Also, due to the way OCP handles intent matching, the Plex skill will return more confident results if you ask for a media type explicitly. For example you might say "play the movie Ghostbusters" to make sure you get back a movie result instead of a soundtrack or TV show. This skill also significantly boosts its confidence score if you include the word Plex in your request: "play music by Charles Mingus on Plex."

_Note: The assumption with users of the Plex skill is that they would want to get Plex results by default, so the base confidence score is 75/100. Asking for Plex specifically boosts that base score to 90. While this will increase the chances of Plex results coming in first, other skills may also have high confidence scores, so results are not guaranteed._

## Examples

Music:
"Hey Mycroft, play Jimi Hendrix"
"Hey Mycroft, play music by Michael Jackson"
"Hey Mycroft, play The Who on Plex"

Movies:
"Hey Mycroft, play the movie Ghostbusters"
"Hey Mycroft, play the Ghostbusters movie on Plex"

TV (not recommended on Mark 2):
"Hey Mycroft, play the Scooby Doo series"
"Hey Mycroft, play the Ghostbusters TV show on Plex"

## Installation

### Neon Mark 2

#### Installation

Update `~/.config/neon/neon.yaml` to include the following:

```yaml
skills:
  default_skills:
    - git+https://github.com/mikejgray/skill-plex@feat-minor-improvements
```

Restart `neon-skills` with `sudo systemctl restart neon-skills` or restart Neon services from the GUI.

For pip installation instructions, see [the OVOS section](#OVOS).

#### Pairing

When it loads, you will see a screen asking you to visit https://plex.tv/link and enter a code. Note that you must be logged into the Plex instance you wish to use. Enter the code and you will authorize the Mark 2 to use your Plex server. You will only need to do this once.

If this is not working for some reason or you prefer to use a specific token, you can manually update the skill settings:

```shell
mkdir -p config/neon/skills/skill-plex.d-mcknight
touch ~/.config/neon/skills/skill-plex.d-mcknight/settings.json
cat <<EOF > ~/.config/neon/skills/skill-plex.d-mcknight/settings.json
{
    "__mycroft_skill_firstrun": false,
    "token": "REPLACE"
}
EOF
```

Visit [https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) for instructions on finding your Plex token.
It should look something like `ys738s6uPWXpwabc4sRYe`.
Enter your token in `~/.config/neon/skills/skill-plex.d-mcknight/settings.json` where it says `REPLACE`.

Finally, `sudo systemctl restart neon-skills`.

## Neon containers

Edit `docker/config/neon.yaml` and add a default skill:

```yaml
skills:
  default-skills:
    - git+https://github.com/mikejgray/skill-plex@feat-minor-improvements
```

Restart the `neon-skills` container, then edit `docker/xdg/config/neon/skills/skill-plex.d-mcknight/settings.json`. Add a `token` entry per the Mark 2 instructions above.

## OVOS

`pip install git+https://github.com/mikejgray/skill-plex@feat-minor-improvements`

If you're using containers, add the following to `~/ovos/config/skills.list`:

```config
git+https://github.com/mikejgray/skill-plex@feat-minor-improvements
```
