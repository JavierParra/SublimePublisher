import os
import sys
import sublime
import sublime_plugin

# __file__ = os.path.normpath(os.path.abspath(__file__))
# __path__ = os.path.dirname(__file__)

# libs_path = os.path.join(__path__, 'lib')
# if libs_path not in sys.path:
# 	print('inserting');
# 	sys.path.insert(0, libs_path);
# from PublisherConfig import Config



class PublisherCommand(sublime_plugin.EventListener):
	conf={}
	tracker = False
	lst = False
	def __init__(self):
		#self.conf = Config("sftp-config.json");
		
		self.tracker = PublisherChangesTracker();
		

	def run(self, edit):
		print("'sup?", sys.path);

	def on_post_save(self, view):
		print(view.file_name() + ' is modified');
		self.tracker.fileChanged(view.window().id(), view.file_name());
	
	def on_window_command(self, window, command, args):
		if(command != 'publish_changes'):
			return;

		dirty = self.tracker.getDirtyFiles(window.id());
		if(not dirty):
			sublime.message_dialog('No files to publish');
			return False;
		self.generateFileList(dirty);
		self.folder = window.extract_variables()['folder'];
		self.window = window;
		
		lst = self.renderFileList();
		window.show_quick_panel(lst, self.filesSelected);

	def generateFileList(self, dirty):
		self.lst = [];
		for i in dirty:
			print(i);
			self.lst.append({'path': i, 'selected': True});

	def renderFileList(self):
		printableList = [['     Upload selected files', ''], ['     Clear selected files', '']];
		for i in self.lst:
			if(i['selected']):
				checkmark = '[x]';
			else:
				checkmark ='[-]';
				
			printableList.append([checkmark+' '+i['path'].split('/').pop(), i['path'].replace(self.folder, '')]);

		print(printableList);
		return printableList;

	def filesSelected(self, index):
		print (index);
		if(index >= 2):
			lstItem = self.lst[index-2];
			lstItem['selected'] = not lstItem['selected'];
			lst = self.renderFileList();
			self.window.show_quick_panel(lst, self.filesSelected);
			return;
		
		# Eliminamos la opción de Upload All listed files porque es redundante y confusa.
		# if(index == 0):
		# 	return self.uploadAll();

		if(index == 0):
			return self.uploadSelected();
		
		if(index == 1):
			return self.clearSelected();

	def uploadAll(self):
		lst = list((item['path'] for item in self.lst));
		print(lst);
		self.window.run_command('sftp_upload_file', {"paths": lst});
		self.cleanFiles(lst);

	def uploadSelected(self):
		lst = list((item['path'] for item in self.lst if item['selected']));
		print(lst);
		self.window.run_command('sftp_upload_file', {"paths": lst});
		self.cleanFiles(lst);

	def clearSelected(self):
		lst = list((item['path'] for item in self.lst if item['selected']));
		print(lst);
		self.cleanFiles(lst);

	def cleanFiles(self, files):
		for i in files:
			self.tracker.cleanFile(self.window.id(), i);



class PublishChangesCommand(sublime_plugin.WindowCommand):
	def run(self):
		print('Delegating', self.window.id());
		# tracker = self.tracker;
		# tracker.getDirtyFiles(self.window.id());


class PublisherChangesTracker:
	modified = {};
	def fileChanged(self, group, path):
		if self.modified.get(group, 0) == 0:
			self.modified[group] = set();

		self.modified[group].add(path);
	
	def getDirtyFiles(self, group):
		if self.modified.get(group, 0) == 0:
			return False;
		return self.modified[group];

	def cleanFile(self, group, path):
		if self.modified.get(group, 0) == 0:
			return False;
		print(self.modified[group]);
		self.modified[group] = self.modified[group] - {path};
		print(self.modified[group]);


