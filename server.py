import web, subprocess, shlex

# pretty stupid seven-segment display ocr web service. 
# needs web.py and ssocr to run. ssocr binary must be in local folder
# local folder also needs a "tmp.jpg" file
# run with 'python server.py', access on port 8080.

urls = ('/upload', 'Upload')

class Upload:
	def GET(self):
		return """<html><head><title>For testing an' shit</title></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="uploadedfile" /><input type="submit" />
</form></body></html>"""
	
	# give us an image, save it to our temp file, then ocr that shit
	def POST(self):
		SSOCR_DIR = "."
		request = web.input(uploadedfile={}) # 'uploadedfile' is what AW's code uses
		tmpimg = open(SSOCR_DIR + "/tmp.jpg","w")
		tmpimg.write(request['uploadedfile'].file.read())
		tmpimg.close()
		
		digits = 250
		result = ""
		while True:
			cmd ="%s/ssocr -t 50 -d %d -n 20 -i 10 tmp.jpg" % (SSOCR_DIR, digits) # TODO: tailor this
			args = shlex.split(cmd)
	
			p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

			#web.debug("out: " + str(p))

			# if we get a result, it will come on stdout, which we store in p[0]. if there's
			# an error, we are assuming it's because we've detected the wrong number of digits
			# and further that we've detected too many (note, this may not be the case! but it
			# probably is because we should detect the 'right' number of digits the second 
			# iteration). the error message should say "found only 5 of 250 digits" or something
			# like that, so we grab the third space delimited field and look for that many digits
			# next time around. 

			result = p[0]
			if p[1]:
				digits = int(p[1].split(" ")[2])
			else:
				break
	
		# now that we have a result return it
		result = result[:-1] 	# strip dat trailing newline
		web.debug(result)
		return result
		raise web.seeother('/upload')
		

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
