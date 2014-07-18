from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
from django.contrib.auth.models import User
from lxml import etree
import os
from django.contrib.auth.decorators import login_required

MEDIA_DIR = settings.MEDIA_DIR
XML_DIR = settings.XML_DIR

#@login_required
def account_profile(request):
	return HttpResponseRedirect('/xmltree/listout/')

#@login_required
@csrf_exempt
def delete_xml_file(request):
	parent = request.POST.get('parent')
	file_xml = request.POST.get('file_is')
	print parent
	print file_xml
	f = os.path.join(XML_DIR, os.path.join(parent , file_xml))
	
	try:
		os.remove(f)
		return HttpResponse("ok")
	except Exception, e:
		return HttpResponse("fail")
	
#@login_required
@csrf_exempt
def delete_xml_folder(request):
	parent = request.POST.get('parent')
	file_xml = request.POST.get('file_is')
	print parent
	print file_xml

	f = os.path.join(XML_DIR,os.path.join(parent , file_xml))
	
	try:
		os.rmdir(f)
		return HttpResponse("ok")
	except Exception, e:
		return HttpResponse("fail")
#@login_required
@csrf_exempt
def create_folder(request):
	if request.method == "POST":
		parent_of_folder = request.POST.get('parent')
		folder_name = request.POST.get('folder_name')
		print parent_of_folder, folder_name, '###################'
		folder_path = os.path.join(XML_DIR, os.path.join(parent_of_folder, folder_name))
		print folder_path
		if os.path.exists(folder_path):
			return HttpResponse('fail')
		else:
			os.makedirs(folder_path)
			return HttpResponse('ok')

#@login_required
def tree_view(request):
	for path , dir ,files in os.walk(XML_DIR):
		
		return render(request,'tree.html',{'Path':path,'file':files})
#@login_required
def XmlViewer(request):
    return render(request,'CreateXml.html')
    #return render(request,'index.html', {'pos':pos,'info':info,})

#@login_required
#def add_record(request):
#	file_name_listout = request.POST.get('file_is')
#	return render(request,'Add_Item.html',{'file_name':file_name_listout,})


def handle_uploaded_file(f):    
	with open( os.path.join(MEDIA_DIR, f.name), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return os.path.join(MEDIA_DIR, f.name)

#@login_required
@csrf_exempt
def add_record(request):
	xml_root = os.listdir(XML_DIR)
	print xml_root, 'xml_root'
	
	if request.POST:
		
		file_xml = request.POST.get('file_is')
		print "xml file--->>>>>>>>>>" , file_xml
		xml_file = os.path.join(XML_DIR, file_xml)

		item_title = request.POST.get('item_title')
		item_thumb = request.POST.get('item_thumbnail')
		sub_link = (request.POST.get('sublink')) 
		val = []
		if sub_link != "":
			sub_link = sub_link + ','
			
			name = ""
			for i in sub_link:
				if i == ",":
					val.append(name)
					name = ""
				else:
					name += i
		
			
		tree = etree.parse(xml_file)
		root = tree.getroot()
		
		item = etree.SubElement(root, 'item')
		etree.SubElement(item, 'title').text = item_title
		item_link = etree.SubElement(item, 'link')
		
		for i in val:
			print i, 'sub link'
			etree.SubElement(item_link, 'sublink').text = i
		
		
		etree.SubElement(item, 'thumbnail').text = item_thumb
		
		etree.ElementTree(root).write( xml_file, pretty_print=True)
	
		
	return render(request,'Add_Item.html', {'xml_root': xml_root})

@csrf_exempt
def add_record_dir(request):
	xml_root = os.listdir(XML_DIR)
	if request.POST:
		file_xml = request.POST.get('file_is')
		xml_file = os.path.join(XML_DIR, file_xml)
		item_title = request.POST.get('item_title')
		item_thumb = request.POST.get('item_thumbnail')
		link = (request.POST.get('link')) 
			
		tree = etree.parse(xml_file)
		root = tree.getroot()
		
		item = etree.SubElement(root, 'dir')
		etree.SubElement(item, 'title').text = item_title
		etree.SubElement(item,'link').text = link
		etree.SubElement(item, 'thumbnail').text = item_thumb
		
		etree.ElementTree(root).write( xml_file, pretty_print=True)
	
		
	return render(request,'add_dir_item.html', {'xml_root': xml_root})


#@login_required
@csrf_exempt		
def create_xml(request):
	xml_file_name = request.POST.get('xml_file_name')
	if xml_file_name.endswith('.xml'):
		file_name = os.path.join(XML_DIR , os.path.join(request.POST.get('parent') , xml_file_name))
	else:
		file_name = os.path.join(XML_DIR , os.path.join(request.POST.get('parent') , xml_file_name + '.xml'))
	flag1 = os.path.isfile(file_name)
	
	if flag1 == False:
		poster_name = request.POST.get('poster_name')
		poster_file = request.POST.get('poster_file')
		info_message = request.POST.get('info_message')
		info_thumb = request.POST.get('info_thumb')

		#create xml data
		root = etree.Element("data")   # Root element of XML document
		etree.SubElement(root, 'poster').text = poster_name
		etree.SubElement(root, 'fanart').text = poster_file
		info = etree.SubElement(root, 'info')
		etree.SubElement(info, 'message').text = info_message
		etree.SubElement(info, 'thumbnail').text = info_thumb
		
		etree.ElementTree(root).write( os.path.join(XML_DIR, file_name), pretty_print=True)

		return HttpResponse('successfully create xml file')
	else:
		return HttpResponse("file already exist")

#@login_required
def show_data(request):
	if request.method == 'GET':
		file_xml = request.GET.get('file_is')
		print "xml file" , file_xml
		xml_file = os.path.join(XML_DIR, file_xml)
		
		tree = etree.parse(xml_file)
		root = tree.getroot()
		
		base_info = {}
		base_info['poster'] = root.find('poster').text
		base_info['fanart'] = root.find('fanart').text
		base_info['message'] = root.find('info').find('message').text
		base_info['thumbnail'] = root.find('info').find('thumbnail').text

		items = []		
		for idx_item, item in enumerate(root.findall('item')):
			item_data = {}
			item_data['title'] = item.find('title').text
			item_data['thumbnail'] = item.find('thumbnail').text
			sublink_data = []
			for idx_sublink, sublink in enumerate( item.find('link').findall('sublink') ):
				sublink_data.append(sublink.text)
			item_data['link'] = sublink_data
			items.append(item_data)

		return render(request, 'show_data.html', {'items': items, 'base_info': base_info})

#@login_required
@csrf_exempt
def get_child_tree(request):
	if request.POST:
		parent = request.POST.get('parent')
		name_of_dir = request.POST.get('current_dir')
		print name_of_dir, parent
		path_of_link = os.path.join(XML_DIR , os.path.join(parent, name_of_dir))
		print path_of_link , ":path"
		directory = build(path_of_link)
		import json
		return HttpResponse(json.dumps(directory))

@login_required
@csrf_exempt		
def list_out(request):
	directory = build(os.path.join(XML_DIR, request.user.username ))
	return render(request, 'listout.html', {'tree': directory})

#@login_required
def build(root_path):
	directory = {}
	elem_list = os.listdir(root_path)
	print elem_list, 'elem_list'
	files = []
	dirs = []
	for obj in elem_list:
		if os.path.isfile(os.path.join(root_path, obj)):
			files.append(obj)
		directory['files'] = files
		if os.path.isdir(os.path.join(root_path, obj)):
			dirs.append(obj)
		directory['dirs'] = dirs

	return directory

#@login_required
def list_files(startpath):
	root = []
	dirs_arr = []
	files_arr = []

	for root, dirs, files in os.walk(startpath):
		level = root.replace(startpath, '').count(os.sep)
		print os.sep, 'sep'
		print startpath
		print root
		print root.replace(startpath, '')
		print level
		indent = ' ' * 4 * (level)
		print('{}{}/'.format(indent, os.path.basename(root)))
		subindent = ' ' * 4 * (level + 1)
		for f in files:
			file_dir = {}
			file_dir[os.path.basename(root)] = f
			files_arr.append(file_dir)
			print('{}{}'.format(subindent, f))
		
		if dirs:
			dirs_dir = {}
			dirs_dir[os.path.basename(root)] = dirs
			dirs_arr.append(dirs_dir)
	
	directory = {}
	directory['files'] = files_arr
	directory['dirs'] = dirs_arr
	print directory
	return directory

#@login_required
@csrf_exempt
def delete_xml(request):
	if request.method == 'GET':
		return HttpResponseRedirect('/xmltree/showdata/')


	import json
	data =  json.loads(request.body)

	xml_file = data['xml_file']
	tree = etree.parse(os.path.join(XML_DIR, xml_file))
	root = tree.getroot()

	update_type = data['type']

	if update_type == 'item':
		item_data = data['item_data']
		item_index = item_data['index']

		for item in root.findall('item['+item_index+']'):
			root.remove(item)
		
		etree.ElementTree(root).write( os.path.join(XML_DIR, xml_file), pretty_print=True)

		return HttpResponse('item successfully Delete')

#@login_required
@csrf_exempt
def update_xml(request):
	if request.method == 'GET':
		return HttpResponseRedirect('/xmltree/showdata/')


	import json
	data =  json.loads(request.body)

	xml_file = data['xml_file']
	tree = etree.parse(os.path.join(XML_DIR, xml_file))
	root = tree.getroot()

	update_type = data['type']

	if update_type == 'item':
		item_data = data['item_data']
		item_index = item_data['index']

		for item in root.findall('item['+item_index+']'):
			item.find('title').text = item_data['title']
			item.find('thumbnail').text = item_data['thumbnail']
			item_link = item.find('link')
			for sublink_index, sublink in enumerate(item_link.findall('sublink')):
				sublink.text = item_data['sublink'][sublink_index]
		
		etree.ElementTree(root).write( os.path.join(XML_DIR, xml_file), pretty_print=True)

		return HttpResponse('item successfully updated')

	elif update_type == 'base':
		base_info_data = data['base_info_data']
		root.find('poster').text = base_info_data['poster']
		root.find('fanart').text = base_info_data['fanart']
		root.find('info').find('message').text = base_info_data['message']
		root.find('info').find('thumbnail').text = base_info_data['thumbnail']

		etree.ElementTree(root).write( os.path.join(XML_DIR, xml_file), pretty_print=True)

		return HttpResponse('item successfully updated')

#@login_required
def showfilehtml(request):
	file_xml = request.GET.get('file_is')
	print "xml file" , file_xml
	xml_file = os.path.join(XML_DIR, file_xml)
	
	with open(xml_file) as f:
		data = f.read()
	print data
	return render(request, 'showfile.html', {'data': data})

#@login_required
@csrf_exempt
def pass_data(request):
	file_xml = request.POST.get('file_is')
	parent = request.POST.get('parent')
	xml_file = os.path.join(XML_DIR, os.path.join(parent, file_xml))

	data = request.POST.get('file_data')
	with open(xml_file, 'w') as f:
		f.write(data)
	return HttpResponse('ok')


class MyCustomRegistrationForm(RegistrationFormUniqueEmail):

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']



class MyRegistrationView(RegistrationView):

    form_class= MyCustomRegistrationForm
    
    def register(self, request, **cleaned_data):
        
        new_user= super(MyRegistrationView, self).register(request, **cleaned_data)
        # here create your new UserProfile object
        return new_user


from registration.signals import user_activated
from django.dispatch import receiver


@receiver(user_activated)
def my_callback(sender, user, request, **kwargs):
	try:
		user_dir = os.path.join(XML_DIR, user.username)
		print user_dir
		os.makedirs(user_dir)	
	except Exception, e:
		print e
		pass
	