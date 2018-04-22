import oauth2 as oauth
import json
import sys

from access2 import *
# from __future__ import print_function

import re
import csv
import xlsxwriter, StringIO

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)


# with open("resp.json", "w") as fl:
# 	json.dump(tweets, fl)

# output = StringIO.StringIO()
# workbook = xlsxwriter.Workbook(output)
# worksheet = workbook.add_worksheet('Sheet1')
header_line = "ID"
header_line = header_line + "," + "Label"
header_line = header_line + "," + "Source"
header_line = header_line + "," + "Type"
header_line = header_line + "," + "Text"
header_line = header_line + "," + "Retweet_count"
header_line = header_line + "," + "Favorite_count"
header_line = header_line + "," + "Hashtags_count"
header_line = header_line + "," + "Urls_count"
header_line = header_line + "," + "Mentions_count"
header_line = header_line + "," + "Media_count"
header_line = header_line + "," + "Symbols_count"
header_line = header_line + "," + "Possibly_sensitive"
header_line = header_line + "," + "Location"
header_line = header_line + "," + "URL"
header_line = header_line + "," + "Description_len"
header_line = header_line + "," + "Verified"
header_line = header_line + "," + "Ff_ratio"
header_line = header_line + "," + "Follower_count"
header_line = header_line + "," + "Friend_count"
header_line = header_line + "," + "Statuses_count"
header_line = header_line + "," + "Favourites_count"
header_line = header_line + "," + "Listed_count"
header_line = header_line + "," + "Account_age"
header_line = header_line + "," + "Default_profile"
header_line = header_line + "," + "Default_profile_image"
header_line = header_line + "\n"
# print header_line

fl = open("test500.csv", "w")
fl.write(header_line)

in_fl = open("initdata.csv", "r")
in_fl.readline()

endpoint = "https://api.twitter.com/1.1/statuses/show.json?id="

err_tw = 0
ff_tw = 0
# for x in xrange(1,7700):
# 	in_fl.readline()

for x in xrange(1,500):
	inp_str = in_fl.readline()
	inp_id = inp_str.split(",")[0]

	req_url = endpoint + inp_id
	resp, data = client.request(req_url)
	tweets = json.loads(data)
	print "\r Tweets Done: " + str(x),
	sys.stdout.flush()

	if "errors" not in tweets:
		twid = tweets["id"]

		dataline = str(twid)

		inp_label = inp_str.split(",")[1]
		dataline = dataline + "," + str(inp_label)
		
		source = tweets["source"]
		source = source.encode("utf-8")
		source = source.replace(",", " ")
		source = source.replace("\"", " ")

		if len(source) > 0:
			src = re.split("<|>", source)[2]
		else:
			src = ""

		dataline = dataline + "," + str(src)
		

		tw_text = tweets["text"]
		tw_text = tw_text.encode("utf-8")
		tw_text = tw_text.replace(",", " ")
		tw_text = tw_text.replace(";", " ")
		tw_text = tw_text.replace("\"", " ")
		
		t_type = "null"

		if tw_text[0] is "@":
			t_type = "reply"
		elif "RT" in tw_text and "@" in tw_text:
			t_type = "retweet"
		elif "@" in tw_text:
			t_type = "mention"
		else:
			t_type = "regular"

		dataline = dataline + "," + str(t_type)
		dataline = dataline + "," + str(tw_text)
		
		retw_cnt = tweets["retweet_count"]
		dataline = dataline + "," + str(retw_cnt)
		
		fav_cnt = tweets["favorite_count"]
		dataline = dataline + "," + str(fav_cnt)
		
		hash_cnt = len(tweets["entities"]["hashtags"])
		dataline = dataline + "," + str(hash_cnt)
		
		url_cnt = len(tweets["entities"]["urls"])
		dataline = dataline + "," + str(url_cnt)
		
		men_cnt = len(tweets["entities"]["user_mentions"])
		dataline = dataline + "," + str(men_cnt)
		
		# media_cnt = len(tweets["entities"][""])	media count
		media_cnt = 0
		dataline = dataline + "," + str(media_cnt)

		symb_cnt = len(tweets["entities"]["symbols"])
		dataline = dataline + "," + str(symb_cnt)

		if "possibly_sensitive" not in tweets:
			poss_sens = 0
		else:
			if tweets["possibly_sensitive"] is False:
				poss_sens = 0
			else:
				poss_sens = 1
		dataline = dataline + "," + str(poss_sens)

		location = tweets["user"]["location"]
		location = location.encode("utf-8")
		location = location.replace(",", " ")
		dataline = dataline + "," + str(location)

		if tweets["user"]["url"] is not None:
			url_pres = 1
		else:
			url_pres = 0
		dataline = dataline + "," + str(url_pres)
		# print "url :"+ str(url)
		descp_len = len(tweets["user"]["description"])
		dataline = dataline + "," + str(descp_len)

		if tweets["user"]["verified"] is True:
			verif = 1
		else:
			verif = 0
		dataline = dataline + "," + str(verif)

		fol_cnt = int(tweets["user"]["followers_count"])

		frnd_cnt = int(tweets["user"]["friends_count"])

		ff_ratio = (fol_cnt+1)/ float(frnd_cnt+1)
		
		dataline = dataline + "," + str(ff_ratio)
		dataline = dataline + "," + str(fol_cnt)
		dataline = dataline + "," + str(frnd_cnt)

		stat_cnt = tweets["user"]["statuses_count"]
		dataline = dataline + "," + str(stat_cnt)

		usr_fav_cnt = tweets["user"]["favourites_count"]
		dataline = dataline + "," + str(usr_fav_cnt)

		lis_cnt = tweets["user"]["listed_count"]
		dataline = dataline + "," + str(lis_cnt)

		acc_create = tweets["user"]["created_at"]
		acc_year = acc_create.split(" ")[5]
		acc_age = 2018 - int(acc_year)
		dataline = dataline + "," + str(acc_age)

		if tweets["user"]["default_profile"] is False:
			def_prof = 0
		else:
			def_prof = 1
		dataline = dataline + "," + str(def_prof)

		if tweets["user"]["default_profile_image"] is False:
			def_prof_img = 0
		else:
			def_prof_img = 1
		dataline = dataline + "," + str(def_prof_img)

		dataline = dataline.replace("\n", "")
		dataline = dataline + "\n"

		fl.write(dataline)

	else:
		print str(x)
		print tweets["errors"]
		err_tw = err_tw +1

print "\nError Tweets: " + str(err_tw)
print "FF: " + str(ff_tw)
fl.close()