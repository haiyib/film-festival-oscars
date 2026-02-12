import pandas as pd

# Read data
oscars = pd.read_csv('oscars.csv', sep='\t')
merged_film = pd.read_csv('merged_film_dataset.csv', low_memory=False)

# Get festival IMDB IDs
festival_imdb_ids = set(merged_film['imdb.id'].dropna())

# Count nominations per film
nominations = oscars.groupby(['Film', 'FilmId']).agg({
    'Category': 'count',
    'Winner': lambda x: x.fillna(False).astype(bool).sum()
}).reset_index()

nominations.columns = ['Film', 'FilmId', 'Nominations', 'Wins']

# Sort by most nominations
nominations = nominations.sort_values('Nominations', ascending=False)

# Explode FilmId to check festival attendance
def check_festival(film_ids):
    if pd.isna(film_ids) or film_ids == '':
        return False
    ids = [id.strip() for id in str(film_ids).split('|')]
    return any(id in festival_imdb_ids for id in ids)

nominations['In_Festival'] = nominations['FilmId'].apply(check_festival)

# Get festival details for films that attended
def get_festival_info(film_ids):
    if pd.isna(film_ids) or film_ids == '':
        return ''
    ids = [id.strip() for id in str(film_ids).split('|')]
    for id in ids:
        match = merged_film[merged_film['imdb.id'] == id]
        if len(match) > 0:
            festivals = match['fest'].unique()
            return ', '.join(festivals)
    return ''

nominations['Festivals'] = nominations['FilmId'].apply(get_festival_info)

# Display results
print("=" * 80)
print("TOP 30 MOST NOMINATED FILMS (All Time)")
print("=" * 80)
print(f"{'Film':<45} {'Noms':>5} {'Wins':>5} {'Festival?':<10} {'Which Festivals'}")
print("-" * 80)

for _, row in nominations.head(30).iterrows():
    festival_status = "Yes" if row['In_Festival'] else "No"
    print(f"{row['Film'][:44]:<45} {row['Nominations']:>5} {row['Wins']:>5} {festival_status:<10} {row['Festivals'][:30]}")

# Summary stats
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
total_films = len(nominations)
in_festival = nominations['In_Festival'].sum()
print(f"Total unique films with Oscar nominations: {total_films}")
print(f"Films that attended festivals in dataset: {in_festival} ({in_festival/total_films*100:.1f}%)")

# Top nominated films that went to festivals
print("\n" + "=" * 80)
print("TOP NOMINATED FILMS THAT ATTENDED FILM FESTIVALS")
print("=" * 80)
festival_films = nominations[nominations['In_Festival']].head(20)
print(f"{'Film':<45} {'Noms':>5} {'Wins':>5} {'Festivals'}")
print("-" * 80)
for _, row in festival_films.iterrows():
    print(f"{row['Film'][:44]:<45} {row['Nominations']:>5} {row['Wins']:>5} {row['Festivals'][:30]}")

# Save full results
nominations.to_csv('most_nominated_films.csv', index=False)
print(f"\nFull results saved to: most_nominated_films.csv")
