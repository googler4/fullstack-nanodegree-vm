import csv
from the_organizer.webapp import database as db
from the_organizer.models import Item, ItemAttribute, ItemImage, Group, GroupMap, AttributeMap
def runCSV():
	parts_csv = "the_organizer/static/parts.csv"
	images_csv = "the_organizer/static/images.csv"

	images = {}

	currentKey = ''
	currentTuple = []
	with open(images_csv, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:

				if(row[0] == currentKey):
					currentTuple.append(row[1])

				else:
					#Push Current Object Reset
					if(currentKey != ''):
						images.update({currentKey:currentTuple})
						
						currentKey = ''
						currentTuple = []
					# print row[0]
					currentKey = row[0]
					currentTuple=[row[1]]
	#Catch Last Row				
	images.update({currentKey:currentTuple})


	with open(parts_csv, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:
				#SH-PWS3,Voltage,El1,6Y6AL2Z7,1546966876940
				#Name, Group, Location, ID, Barcode

				try:
					#Find Group
					group_id = db.session.query(Group).filter(Group.attribute == str(row[1])).one()
					group_id = group_id.id
					# print group_id;
				except:
					#Create Group
					group_id = Group.add(None, row[1], '0', 1).insert()
				#title, headline, description, primary_key, url, amazon_url,thumbnail
				item_id = Item.add(
					row[0],
					row[2],
					'',
					row[3],
					'',
					'',
					'/static/'+images[row[3]][0]).insert()

				GroupMap.add(item_id, group_id, row[1], '0', 1).insert()

				for image in images[row[3]]:
					ItemImage.add(item_id, '/static/'+image).insert()

				short_id = AttributeMap.getID('short_id')
				ItemAttribute.add(item_id, short_id, 'short_id', row[3], 1).insert()

				barcode_id = AttributeMap.getID('barcode')
				ItemAttribute.add(item_id, barcode_id, 'barcode', row[4], 1).insert()

			

			