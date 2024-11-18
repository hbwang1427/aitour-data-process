psql -U aitour -d aitour_test -h localhost
Truncate table ai_art,ai_art_infomation,ai_artist,ai_artist_information,ai_reference_imagecascade;
python insert_data.py
