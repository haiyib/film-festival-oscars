import pandas as pd

# Read both CSV files
merged_film = pd.read_csv('merged_film_dataset.csv')
oscars = pd.read_csv('oscars.csv', sep='\t')  # oscars.csv is tab-separated

# Explode the FilmId column to handle multiple IDs (e.g., "tt0019217|tt0018253")
oscars['FilmId'] = oscars['FilmId'].fillna('')
oscars_exploded = oscars.assign(FilmId=oscars['FilmId'].str.split('|')).explode('FilmId')

# Clean up whitespace
oscars_exploded['FilmId'] = oscars_exploded['FilmId'].str.strip()

# Merge on IMDB ID
combined = merged_film.merge(
    oscars_exploded,
    left_on='imdb.id',
    right_on='FilmId',
    how='left'  # keeps all films, adds Oscar info where available
)

# Save the combined dataset
combined.to_csv('combined_film_oscars.csv', index=False)

print(f"Merged film dataset rows: {len(merged_film)}")
print(f"Oscars dataset rows: {len(oscars)}")
print(f"Combined dataset rows: {len(combined)}")
print(f"\nFilms with Oscar nominations: {combined['FilmId'].notna().sum()}")
print(f"\nSaved to: combined_film_oscars.csv")
