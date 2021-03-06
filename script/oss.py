# -*- coding: utf-8 -*-
import oss2
import os
import pickle
from datetime import datetime

#Bucket.get_object_meta('')

class Ossoperation:

	def __init__(self):
		self.endpoint = ''   #oss地址
		self.auth = oss2.Auth('', '')  #阿里云key
		self.Bucket = oss2.Bucket(self.auth, self.endpoint, 'gy-download-apk')


	def get_fileinfo(self):
		dir_files = {}
		try:
			for i in oss2.ObjectIterator(self.Bucket):
				dirname = i.key.split('/')[0]
				filename = i.key.split('/')[1]
				if filename:
					files_size = self.Bucket.get_object_meta(os.path.join(dirname,filename)).content_length
					files_lasttime = self.Bucket.get_object_meta(os.path.join(dirname,filename)).last_modified
					dates = datetime.utcfromtimestamp(files_lasttime).strftime("%Y-%m-%d %H:%M")
					dir_files.setdefault(dirname,[]).append({filename:[files_size,dates]})
		except Exception as e:
			raise e
		with open('oss_obj_info','w') as files:
			pickle.dump(dir_files,files)

	def upload_files(self,objname,localfile):
		oss2.resumable_upload(self.Bucket,objname,localfile,store=oss2.ResumableStore(root='/Users/root1/webdev/fileload'))



# a = Ossoperation()
# a.get_fileinfo()
