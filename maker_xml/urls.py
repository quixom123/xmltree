from django.conf.urls import patterns , url
from maker_xml.views import XmlViewer, create_folder , delete_xml_file , showfilehtml, pass_data , delete_xml_folder ,create_xml , add_record, tree_view , show_data, update_xml, list_out, get_child_tree , delete_xml
urlpatterns = patterns('',
	url(r'^create/$' , create_xml , name='create'),
	url (r'^$', XmlViewer , name='XmlViewer'),
	url (r'^Add_Record/$', add_record , name='add record'),
	url (r'^showdata/$', show_data , name='show data'),
	url (r'^updatexml/$', update_xml , name='update xml'),
	url (r'^listout/$', list_out , name='listout xml'),
        	url(r'^tree/$' , tree_view , name='Tree'),
        	url(r'^getchild/$' , get_child_tree , name='get_child_tree'),
        	url(r'^delete_xml/$' , delete_xml , name='Delete-item'),
        	url(r'^create_folder/$' , create_folder , name='Create_folder'),
        	url(r'^delete_xml_file/$' , delete_xml_file , name='delete_xml_file'),
        	url(r'^delete_xml_folder/$' , delete_xml_folder , name='delete_xml_folder'),
        	url(r'^showfilehtml/$' , showfilehtml , name='showfilehtml'),
        	url(r'^passdata/$' , pass_data , name='pass_data'),
	)
