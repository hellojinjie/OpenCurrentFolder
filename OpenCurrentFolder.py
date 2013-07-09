import sublime
import sublime_plugin
import os

class ProjectFolderListener(sublime_plugin.EventListener):


	def on_activated_async(self, view):
		dir_name = self.get_dir_name(view)
		self.add_folder_to_project(dir_name)


	def on_close(self, view):
		project_data = sublime.active_window().project_data();
		try:
			folders = project_data['folders']
			print(folders)
			new_folders = [f for f in folders if f['path'] != self.get_dir_name(view)]
			print(new_folders)
			project_data['folders'] = new_folders
			sublime.active_window().set_project_data(project_data)
		except:
			pass


	def get_dir_name(self, view):
		return os.path.dirname(view.file_name())


	def add_folder_to_project(self, dir_name):
		folder = {
				'follow_symlinks': True, 
				'path': dir_name, 
				'folder_exclude_patterns': ['.*'],
				# maybe, we need to edit .gitignore, 
				# so do not exclude files that it's name begin with dot
				# 'file_exclude_patterns': ['.*'],		
		}
		project_data = sublime.active_window().project_data();
		try:
			folders = project_data['folders']
			for f in folders:
				if f['path'] == dir_name:
					return
			folders.append(folder)
		except:
			folders = [folder]
			if project_data is None:
				project_data = {}
			project_data['folders'] = folders
		sublime.active_window().set_project_data(project_data)

