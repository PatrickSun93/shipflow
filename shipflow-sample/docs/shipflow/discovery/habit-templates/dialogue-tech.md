# Discover dialogue — tech persona

## Round 1

- Templates are seed data for the existing `Habit` model — no schema
  change beyond a small `HabitTemplate` table (name, cadence, icon).
- Question: does picking a template pre-fill and let the user edit
  before saving, or create the habit immediately?

## Round 2

- Read ux + business notes. Pre-fill-then-edit avoids a second write
  path — the create form still does one insert, just pre-populated.
