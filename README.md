# Super Smash Bros. Ultimate API

<p align="center">
  <img alt="Super Smash Bros. Ultimate Logo" src="https://github.com/user-attachments/assets/a2fc558a-1afe-49a1-802e-2651bd92b0e5" />
</p>

<p align="center">
    Unofficial Super Smash Bros. Ultimate RESTful API built with FastAPI<br>
    ⚠️ <b>Still in development!</b> ⚠️
</p>

## About

This project is an unofficial RESTful API for Super Smash Bros. Ultimate, developed with FastAPI. It is intended to provide easy access to various in-game data, including characters, stages, and items. Keep reading to learn more about the data provided by this API.

### Roster Slots (Fighters)

#### Description

Simply put, a *roster slot* is a playable fighter. However, there are some reasons as to why I decided to name it that way which might help you understand this choice.

The main reason for that decision is the fact that some fighters in Ultimate are not just one single *fighter*, but multiple condensed into one *roster slot*. I refer to Pokémon Trainer and Pyra/Mythra.

In Pokémon Trainer's case, Squirtle, Ivysaur, and Charizard are three *fighters* condensed into one *roster slot*, which is Pokémon Trainer. Similarly, Pyra and Mythra are two *fighters* condensed into the Pyra/Mythra *roster slot*.

I wanted to find a way to represent all playable characters – including the aforementioned special cases – while keeping the schema consistent, hence why I chose to treat them as *roster slots*.

Therefore, think of *roster slots* as the selectable squares that you see on the character selection screen. Each *roster slot* can contain one or more *fighters*. The Pokémon Trainer and Pyra/Mythra *roster slots* contain multiple, while the others contain only one.

#### Schema
`ids`: IDs of the fighters contained in the roster slot.

`name`: Name of the roster slot.

`slug`: Slugified version of the name.

`series`: Franchise or universe the roster slot comes from.

`availability`: Starter, unlockable, DLC, or custom (Miis).

`also_appears_in`: Other Smash games where the roster slot is playable.

`alts`: Alternative colors or costumes of the roster slot.

`variants`: Variations of character or costume among the alts (e.g. Male/Female, Olimar/Alph, Phantom Thief/Student Joker, etc.).

`tips`: In-game tips for the roster slot (found in the "Tips" section).
> **Note**: `tips` are already in the JSON, but their content is empty as the actual data was not yet imported.

`fighters`: Fighters contained in the roster slot.

### Stages

Not yet implemented.

### Items

Not yet implemented.

## Documentation

You can check out the API documentation at:
<table>
  <tr>
    <td>Swagger</td>
    <td>https://smash-ultimate-api.vercel.app/docs</td>
  </tr>
  <tr>
    <td>Redocly</td>
    <td>https://smash-ultimate-api.vercel.app/redoc</td>
  </tr>
</table>

## State of the Project

This project is in **development** and not yet released. Though it is already usable and can be played with, you would not want to rely on it for serious projects for now.
