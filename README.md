# Mood Analyser
Analyses personal mood tracker on Excel with intuitive data visualisations.

### Visualisation Examples:
<img width="49%" height="400" alt="Mood_Grid_View" src="https://github.com/user-attachments/assets/bbad9a29-1f00-42cf-b9d4-ee7d7d61297e" />
<img width="49%" height="800" alt="Word_plot" src="https://github.com/user-attachments/assets/63fff94d-e8a5-4f72-bab4-f69e95e47307" />

### Centralised approach: 
- `Mood_Analyser.py`: Using pandas DataFrame as one central data structure, visualisation and data processing are based off `mood_df`.
- Performance: slower data structure construction, but has efficient large-scale operations on numerical data.

### Modularised approach:
- `Excel_to_Json.py`: Scraping Excel worksheet, storing Python dictionary as local JSON file.
- `TinyDB_of_Mood.py`: Converting JSON file into noSQL database for easy query.
- `Visualise_Mood.py`: Visualisation with the aid of TinyDB queries.
- Performance: fast initial extraction and easy string handling, but relies on naive operations on numerical data.
