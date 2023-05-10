import os
import sublime
import sublime_plugin
import webbrowser
import codecs
from .markdown import markdown

package_path = sublime.packages_path() + "/MarkdownExport/"

settings = sublime.load_settings('MarkdownExport.sublime-settings')
template_name = settings.get("template")
html_template_name = settings.get("templates").get(template_name).get("html")

def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)

def load_utf8(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

class markdown_export_command(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            html_template = load_utf8(package_path + "templates/" + html_template_name)
            #css_template = load_utf8(package_path + "template.css")
            css_template = ""
            md_file = self.view.window().active_view().file_name()
            md_name = os.path.splitext(os.path.basename(md_file))[0]
            selection = sublime.Region(0, self.view.size())
            md = self.view.substr(selection)

            html = markdown(md)
            out = html_template.replace("<% TITLE %>", md_name).replace("<% HTML %>", html).replace("<% STYLE %>", css_template)

            html_file = os.path.splitext(md_file)[0] + '.html'
            #sublime.error_message(htmlfile)
            save_utf8(html_file, out)

            webbrowser.open("file://" + html_file)
        except Exception as e:
            sublime.error_message("Error in MarkdownExport package:\n\n" + str(e))
