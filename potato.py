import fastf1 as ff1
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from fastf1 import plotting
from datetime import datetime as dt

current_year = dt.now().year

# Set the path to the F1 data
ff1.Cache.enable_cache('./cache')

RACE_TYPES = {
	'conventional': ['FP1', 'FP2', 'FP3', 'Q', 'R'],
	'sprint_qualifying': ['FP1', 'SQ', 'Sprint', 'Q', 'R'],
}

START_YEAR = 2018

def saveLaps(laps, location, year, session_type):
	print(laps.head())
	colms = ['year', 'session_type']
	for col in laps.columns:
		colms.append(col)
	_laps = pd.DataFrame(columns=colms)
	_laps = pd.concat([_laps, laps], ignore_index=True)
	print(f'Saving {len(_laps)} laps for {location} - {year} - {session_type}')
	_laps['year'] = year
	_laps['session_type'] = session_type
	updated_laps = _laps
	if os.path.exists(f'csv/{location}.csv'):
		previous_laps = pd.read_csv(f"csv/{location}.csv")
		updated_laps = pd.concat([previous_laps, _laps], ignore_index=True)
	# Appending new data to the existing data
	# Fixing the indexes
	updated_laps.reset_index(drop=True, inplace=True)
	updated_laps.to_csv(f'csv/{location}.csv', index=False)

def getYearData(year, start_race = ""):
	print(f'Processing year {year}')
	year_data = []
	event = None
	try:
		event = ff1.get_event_schedule(year)
	except Exception as e:
		print(f'Error on {year}')
		print(e)
		raise e
	start_key = 1
	if start_race != "":
		start_key = event[event['Location'] == start_race].index[0]
		print(f'Starting from {start_key}')
	for ind in range(start_key, len(event)):
		row_value = event.loc[ind]
		if not row_value['F1ApiSupport']:
			continue
		if row_value['EventFormat'] not in RACE_TYPES:
			print(f'Event format {row_value["EventFormat"]} not configured.')
			break
		print(f'\n\n\nProcessing {year} - {row_value["Location"]}')
		for session_type in RACE_TYPES[row_value['EventFormat']]:
			print(f'\n\n\nProcessing {year} - {row_value["Location"]} - {session_type}')
			try:
				session = ff1.get_session(year, row_value['Location'], session_type)
				session.load()
				saveLaps(session.laps, row_value['Location'], year, session_type)
				year_data.append({'session_data': session, 'Location': row_value['Location']})
			except Exception as e:
				print(f'Error on {year} - {row_value["Location"]} - {session_type}')
				print(e)
				break
			print(f'Processed {year} - {row_value["Location"]} - {session_type}')
		print(f'Processed {year} - {row_value["Location"]}\n\n\n')
	return year_data

try:
	data = getYearData(2019)
	# for race in data:
	# 	laps = {}
	# 	for lap in race['session_data']:
	# 		laps += lap.laps
	# 	laps['Year'] = START_YEAR
	# 	print(f'Processed {len(laps)} laps')
	# 	race['Lap'] = laps
	# 	if os.path.exists(f'csv/{race["Location"]}.csv'):
	# 		previous_races = pd.read_csv(f"csv/{race['Location']}.csv")
	# 	# Appending new data to the existing data
	# 	updated_races = pd.concat([previous_races, laps], ignore_index=True)
	# 	updated_races.to_csv(f'csv/{race["Location"]}.csv', index=False)
except Exception as e:
	print(e)
finally:
	text = (
		'8888888b.                            ',
		'888  "Y88b                           ',
		'888    888                           ',
		'888    888  .d88b.  88888b.   .d88b. ',
		'888    888 d88""88b 888 "88b d8P  Y8b',
		'888    888 888  888 888  888 88888888',
		'888  .d88P Y88..88P 888  888 Y8b.    ',
		'8888888P"   "Y88P"  888  888  "Y8888 '
	)
	for line in text:
		print(line)