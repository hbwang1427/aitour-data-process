import io
import psycopg2 as pg
import numpy as np 
import os
import glob,json
import struct
from pprint import pprint

def read_raw_path_from_index(path):

	match_raw_path= open(path)
	raw_path=[]
	for item in match_raw_path.readlines():
		item=item.split('-->')[0]
		item=item.rsplit('/',1)[0]
		raw_path.append(item)
	# print(raw_path)
	return raw_path

def read_art_detail_from_json(start_path,json_path):
	art_detail=[]
	json_path=start_path+json_path
	filenam=glob.glob(json_path+'/*.json')
	#print("path is",start_path,json_path,filenam)
	with open(filenam[0]) as f:
		data=json.load(f)
	artist_name=data['artist']
	class_name=data['class']
	date=data['date']
	department=data['department']
	img=data['img']
	location=data['location']
	medium=data['medium']
	title=data['title']
	art_detail=[artist_name,class_name,date,department,img,location,medium,title]
	return art_detail

def read_all_art_features(fileDir,rel_path,is_mobile_feature=False):
	abs_file_path = os.path.join(fileDir, rel_path)
	art_feature_file= open(abs_file_path)
	art_features={}
	for item in art_feature_file.readlines():
		items=item.split(',')
		if is_mobile_feature:
			key=items[0][11:17]
			print (key)
			if key in art_features:
				print("duplicate",key)
			#if key=='000001':
				#print("csv line is ",item)
				#print("&&&&")
				#print("itmes is",items[1:])
		else:
			key=items[0][18:24]

		#convert feature to bytearray
		value = []
		for fv in items[1:]:
			value.extend(list(struct.pack("f", float(fv))))
		#print("feature len:", len(value))
		art_features[key] = bytearray(value)
	return art_features
	
def convert_to_string(number):
	six_string=str(number)
	while(len(six_string)<6):
		six_string='0'+six_string
	return six_string

def find_paths(fileDir,rel_path,art_id_str,filetype,is_description):
	audio_paths=[]
	description_dic={}

	path=fileDir+rel_path+art_id_str+filetype
	
	for item in glob.glob(path):
		key=item.split('/')[-1]

		if(is_description):
			description= open(item,'r')
			value=description.read()
			description_dic[key]=value.strip()
		else:
			audio_paths.append(key)

	if is_description:
		return description_dic
	else:
		return audio_paths


if __name__ == '__main__':
	conn = pg.connect(dbname="aitour_test", user="aitour",
			password="aitour", host="127.0.0.1", port="5432")
	#cur = conn.cursor()

	fileDir = os.path.dirname(os.path.realpath('__file__'))

	museum_id=1
	museum_name='MET'
	language_id=1
	'''
	# #insert data to museum,language
	cur.execute("insert into ai_museum (museum_id,lat,lng) values (%s,%s,%s)", 
		(museum_id, 40.816841, -73.956736))
	conn.commit()
	cur.execute("insert into ai_language (language_id,language_name) values (%s,%s)", 
		(language_id, 'English'))
	cur.execute("insert into ai_language (language_id,language_name) values (%s,%s)", 
		(2, 'Chinese'))
	conn.commit()
	cur.execute("insert into ai_museum_information (museum_id,language_id,name, city, country ) values (%s,%s,%s,%s,%s)", 
		(museum_id,language_id, museum_name,'new york','USA'))
	conn.commit()
	'''
#step 1: read features
	rel_path = "MET/visual_features/rmac_index.csv"
	art_features=read_all_art_features(fileDir,rel_path)
	mobilenet_path = "MET/visual_features/mobilenet_index.csv"
	mobilenet_features=read_all_art_features(fileDir,mobilenet_path,True)
	# for li in mobilenet_features:
	# 	if li=='000001':
	# 		print("datbase is ",li, mobilenet_features[li])
	#raise SystemExit(0)
	print("mobilenet_features length is ", len(mobilenet_features))
	art_id=0
	artist_id=0#starts from 1
	for  artist_id in range(0,1):
		#for loop
		art_id+=1
		art_id_str=convert_to_string(art_id)
		print('&&&start',art_id_str)
		try:

			#step 2: read image path/audio/description dic(may have two)
			#image_path='MET/Images/'+art_id_str+'.jpg'
			#audio_paths=find_paths(fileDir,'/MET/Audio/',art_id_str,'*.mp3',False)
			#description_dic=find_paths(fileDir,'/MET/Description/',art_id_str,'*.txt',True)
			#print (audio_paths,description_dic)
		#											1000      2           3    4         5      6       7    8
			#step 3: get json art_detail art_detail=[artist_name,class_name,date,department,img,location,medium,title]
			#raw_path=read_raw_path_from_index("/home/pangolins/work/data/Museum/MET-image-index.txt")
			#print("raw_path is ",raw_path[0],art_id-1,raw_path[art_id-1])
			#art_detail=read_art_detail_from_json("/home/pangolins/work/data/",raw_path[art_id-1])
			#print(art_detail)
			#artist_name=art_detail[0].strip()
			#print ("artist_name ",artist_name)
			#print("art_features ",art_features)
			#image_feature=art_features[art_id_str]
		
			#feature=np.array(image_feature,  dtype=np.float32)
			#print ("keys name",keys[art_id-1],type(image_feature),image_feature)
		#insert artist/artist_information

			
			# if(len(artist_name)!=0):
			# 	try:
			# 		artist_id+=1
			# 		cur.execute("insert into ai_artist(artist_id,birth_year) values(%s,%s)", (artist_id,''))
			# 		cur.execute("insert into ai_artist_information(artist_id,language_id,first_name) values(%s,%s,%s)", (artist_id,1,artist_name))
			# 		cur.execute("insert into ai_art(art_id,museum_id,artist_id,creation_year) values(%s,%s,%s,%s)", (art_id,museum_id,artist_id,art_detail[2]))
			# 		conn.commit()
			# 	except Exception,e2:
			# 		print(e2)
			# 		print(art_id,"failed to insert ai_artist_information")
			# else:
			# 	try:
			# 		cur.execute("insert into ai_art(art_id,museum_id,creation_year) values(%s,%s,%s)", (art_id,museum_id,art_detail[2]))
			# 		conn.commit()
			# 	except Exception,e3:
			# 		print(e3)
			# 		print(art_id,"failed to insert ai_art")
			
		# insert art_information/reference_image
			# for item in description_dic:
			# 	if 'zh' in item:
			# 		language_id=2
			# 		audio_path=''
			# 		for audio_item in audio_paths:
			# 			if 'zh' in audio_item:
			# 				audio_path=audio_item

			# 		cur.execute("insert into ai_art_information(art_id,language_id,title,location,material,category,text,audio) values(%s,%s,%s,%s,%s,%s,%s,%s)", (art_id,language_id,art_detail[7],art_detail[5],art_detail[6],art_detail[3],description_dic[item],audio_path))
			# 		conn.commit()
				
			# 	else:
			# 		language_id=1
			# 		audio_path=""
			# 		for audio_item in audio_paths:
			# 			if 'en' in audio_item:
			# 				audio_path=audio_item
			# 		cur.execute("insert into ai_art_information(art_id,language_id,title,location,material,category,text,audio) values(%s,%s,%s,%s,%s,%s,%s,%s)", (art_id,language_id,art_detail[7],art_detail[5],art_detail[6],art_detail[3],description_dic[item],audio_path))
			# 		conn.commit()
			try:
				#print(mobilenet_features[art_id_str]) 
				cur = conn.cursor()
				cur.execute("insert into ai_reference_image(image_id,art_id,image_location,image_feature,mobilenet_feature) values(%s,%s,%s,%s,%s)",(art_id,art_id,art_id_str, pg.Binary(art_features[art_id_str]), pg.Binary(mobilenet_features[art_id_str])))
				conn.commit()
				cur.close()
			except Exception,e1:
				print(e1)
				print('store mobilenet feature failed for',art_id_str)
		except Exception,e:
			print (e)
			print(art_id,'failed to insert')
		#conn.commit()
	conn.close()
	











		



	# #select top museum id
	# museum_id = 0
	# cur.execute("select * from ai_museum limit 1")
	# rows = cur.fetchall()
	# for row in rows:
	# 	museum_id = row[0]
	# 	print(row)

	# #insert new record to ai_art if ai_art of museum is empty
	# cur.execute("select count(*) from ai_art where museum_id=%s", (museum_id,))
	# row = cur.fetchone()
	# if row[0] == 0:
	# 	cur.execute("insert into ai_art(museum_id,creation_year, title, category, price) values(%s,%s,%s,%s,%s)", 
	# 		(museum_id, '1982-01-01', 'xxxx', "porcelain", 1000))
	# 	conn.commit()


	# #select the art_id
	# cur.execute("select id from ai_art where museum_id=%s", (museum_id,))
	# row = cur.fetchone()
	# art_id = row[0]

	# cur.execute("select count(*) from ai_art_photo where art_id=%s", (art_id,))
	# row = cur.fetchone()
	# if row[0] == 0:
	# 	#store the np array into ai_art.feature column
	# 	feature = np.array([1,2,3], order='C', dtype=np.float32)
	# 	cur.execute("insert into ai_art_photo(art_id, url, feature, width, height) values(%s, %s, %s, %s, %s)", (art_id, "/art_photo/xxx.jpg", feature, 300, 400))
	# 	conn.commit()

	# #fetch the feature back
	# cur.execute("select feature from ai_art_photo where art_id=%s limit 1", (art_id,))
	# row = cur.fetchone()
	# print(row)

	
