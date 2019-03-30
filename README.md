# ETB (name pending)
> A tournament organizer targeted mainly for Magic the Gathering players

Using:

- Server:
  - Node
  - Express.js
  - Docker
  - Knex.js
  - MySQL
  - AWS Elastic Beanstalk
- Client:
  - tbd

## Summary

## Feature Specs
	- Create a player
		- CRUD 
		- User can create an account
	- Create a leagues
		- CRUD
		- User can create a league
		- Tournaments can be created under leagues
	- Create a tournament
		- CRUD
		- User can create a tournament
			- Tournaments can be created on their own or as part of a league
		- Players can be added from a list of registered accounts or they can be manually
		  added.
	- Tournament Functionality
		- User can declare whether tournament is a draft or not
		
		- Players can input match scores.
		- Leaderboard can be viewed at any time.


## User Stories
	1. User wants to draft with his friends. 
	2. User creates a tournament with brackets. 
	3. User is prompted to input player names, and puts in 8 names total.
	4. User chooses to randomize draft seating over manually inputting them.
	5. User chooses swiss format over other formats.
	6. User chooses to randomize match-ups over other options.
	7. User inputs 50 minute match timer.
	8. User starts the draft.
	9. Players get seated based on the draft seating shown.
	10. After card selection part is done, User moves onto matches.
	11. Players sit in pairs based on matchmaking shown.
	12. As players finish their matches, they input their match scores.
	13. Once all players finish their matches, or time has run out for the round,
	14. User moves on to round 2.
	15. User repeats steps 12 through 14, moving onto round 3 instead of 2.
	16. User repeats steps 12 and 13 once again, then ends the tournament.
	17. Player rankings for the tournament are shown.

## Checklist

- [x] Create a model for the settings table
- [x] Add an Express server
- [x] Add resource routes for settings, paints, and schemes
- [ ] Create a migration to seed the settings table with dataone fields
- [ ] Handle pagination
- [ ] Handle validation of data
- [ ] Handle authentication/tokens
- [ ] Handle errors

### Server

#### Settings

- [x] Show all settings with GET /v1/settings
- [x] Show one setting with GET /v1/settings/:id
- [x] Delete a setting with DELETE /v1/settings/:id
- [x] Create a new setting with POST /v1/settings
- [ ] Update a setting with PUT /v1/settings/:id

#### Dataone Paint

- [x] Show all paints with GET /v1/paints
- [x] Show one paint with GET /v1/paints/:id

#### Dataone Paint Schemes

- [x] Show all schemes with GET /v1/schemes
- [x] Show one scheme with GET /v1/schemes/:id

#### Users

- [ ] tbd...
- [ ] CRUD

### Client

- [ ] tbd...