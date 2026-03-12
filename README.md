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

### Roster Slots

<!-- snippet:roster-slots-tag-description -->
Simply put, a *roster slot* is a playable fighter. However, there are some reasons as to why I decided to name it that way which might help you understand this choice.

The main reason for that decision is the fact that some fighters in Ultimate are not just one single *fighter*, but multiple condensed into one *roster slot*. I refer to Pokémon Trainer and Pyra/Mythra.

In Pokémon Trainer's case, Squirtle, Ivysaur, and Charizard are three *fighters* condensed into one *roster slot*, which is Pokémon Trainer. Similarly, Pyra and Mythra are two *fighters* condensed into the Pyra/Mythra *roster slot*.

I wanted to find a way to represent all playable characters – including the aforementioned special cases – while keeping the schema consistent, hence why I chose to treat them as *roster slots*.

Therefore, think of *roster slots* as the selectable squares that you see on the character selection screen. Each *roster slot* can contain one or more *fighters*. The Pokémon Trainer and Pyra/Mythra *roster slots* contain multiple, while the others contain only one.

#### Schema
`ids`: IDs of the fighters contained in the roster slot. The IDs follow the [fighter number](https://www.ssbwiki.com/Fighter_number) method of identification.

`name`: Roster slot name.

`slug`: Slugified version of the name.

`series`: Franchise or universe the roster slot comes from.

`availability`: `Starter`, `Unlockable`, `Paid DLC`, or `Custom` (Miis).

`also_appears_in`: Other Smash games where the roster slot is playable.

`order`: Integer representing the roster slot's position in the character selection screen.

`alts`: Alternative colors or costumes of the roster slot.
  - `slot`: Alt number.
  - `variant`: Name of the variant that the alt corresponds to.
  - `image`: Alt image.

`variants`: Variations of character or costume among the alts (e.g. Male/Female, Olimar/Alph, Phantom Thief/Student Joker, etc.).
  - `name`: Variant name.
  - `boxing_ring_title`: The title that appears in the Boxing Ring stage when the variant is selected.
  - `type`: `Default`, `Different character`, or `Same character`.

    > **Meaning of each type**
    >
    > `Default`: It is the variant of the default alt (e.g. Olimar, Bowser Jr.).
    > 
    > `Different character`: Variants that represent a different character than the default alt (e.g. Alph, Alex, Enderman, Wendy, Ludwig, Lemmy).
    > 
    > `Same character`: Variants that represent the same character as the default alt but with different appearances (e.g. Female/Male Inkling, Phantom Thief/Student Joker). If the roster slot has a variant of this type, the default alt is *not* of type `Default`, but of type `Same character` as well.

`tips`: In-game tips for the roster slot (found in the "Tips" section of the "Extras" menu).
  - `title`: Tip title.
  - `content`: Tip content.
  - `level`: `Beginner`, `Intermediate`, or `Advanced`.
  
    > **Meaning of each level**
    > 
    > `Beginner`: Tip can always appear.
    > 
    > `Intermediate`: Tip can only appear after seeing 200 tips.
    > 
    > `Advanced`: Tip can only appear after seeing 650 tips.

`fighters`: Fighters contained in the roster slot.
  - `id`: Fighter ID (follows the [fighter number](https://www.ssbwiki.com/Fighter_number) method of identification).
  - `name`: Fighter name.
  - `slug`: Slugified version of the name.
  - `also_appears_in`: Other Smash games where the fighter appears in.
<!-- /snippet -->

### Fighters

<!-- snippet:fighters-tag-description -->
Playable fighters in a Roster Slot. Read the Roster Slot docs to better understand the difference between a Roster Slot and a Fighter.

#### Schema
`id`: Fighter ID (follows the [fighter number](https://www.ssbwiki.com/Fighter_number) method of identification).

`name`: Fighter name.

`slug`: Slugified version of the name.

`also_appears_in`: Other Smash games where the fighter appears in.
<!-- /snippet -->

### Stages

<!-- snippet:stages-tag-description -->
Arenas where players fight against each other.

#### Schema
`id`: Stage ID (follows the stage selection screen order).

`name`: Stage name.

`slug`: Slugified version of the name.

`series`: Franchise or universe the stage comes from.

`availability`: `Starter`, `Free DLC`, or `Paid DLC`.

`also_appears_in`: Other Smash games where the stage appears in.

`image`: Stage image.

`is_original_or_new_version`: True if the stage is an Ultimate-original or is an old stage which received a new version in Ultimate.<!-- /snippet -->

### Items

<!-- snippet:items-tag-description -->
Objects that appear during a match which can be picked up and used by players.

#### Schema
`id`: Item ID (follows the item selection screen order).

`name`: Item name.

`slug`: Slugified version of the name.

`series`: Franchise or universe the item comes from.

`also_appears_in`: Other Smash games where the item appears in.

`image`: Item image.

`types`: Categories the item belongs to based on its attributes and effects.

`heavy`: True if the item limits who picks it up into walking slowly.

`notes`: Observations about the item (taken from the [Smash Wiki](https://www.ssbwiki.com/Item)).
<!-- /snippet -->

## Documentation

You can check out the API documentation at:
<table>
  <tr>
    <td>Redoc</td>
    <td>https://smash-ultimate-api.vercel.app/redoc</td>
  </tr>
  <tr>
    <td>Swagger</td>
    <td>https://smash-ultimate-api.vercel.app/docs</td>
  </tr>
</table>
I personally think that the Redoc version is more organized visually, but both contain the same information.

## State of the Project

This project is in **development** and not yet released. Though it is already usable and can be played with, you would not want to rely on it for serious projects for now.
