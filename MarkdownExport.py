import os
import sublime
import sublime_plugin
import webbrowser
import codecs
import re
from .markdown import markdown

def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)

def load_utf8(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

class markdown_export_command(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            package_path = sublime.packages_path() + "/MarkdownExport/"

            settings = sublime.load_settings('MarkdownExport.sublime-settings')
            template_name = settings.get("template")
            html_template_name = settings.get("templates").get(template_name).get("html")

            md_path = self.view.window().active_view().file_name()

            if not os.path.splitext(md_path)[1] in [".md", ".MD", ".markdown", ".Markdown"]:
                sublime.error_message(md_path  + "\nis not a Markdown file\n\n")
                return 1

            html_template = load_utf8(package_path + "templates/" + html_template_name)
            depend = re.findall('<%- (.*?) -%>', html_template, re.DOTALL)
            insert = re.findall('<%= (.*?) =%>', html_template, re.DOTALL)
            md_name = os.path.splitext(os.path.basename(md_path))[0]
            selection = sublime.Region(0, self.view.size())
            md = self.view.substr(selection)

            html = markdown(md)

            out = html_template
            if 'TITLE' in insert:
                out = out.replace("<%= TITLE =%>", md_name)
            if 'HTML' in insert:
                out = out.replace("<%= HTML =%>", html)
            for item in depend:
                item_file_name = settings.get("templates").get(template_name).get(item)
                item_file = load_utf8(package_path + "templates/" + item_file_name)
                out = out.replace("<%- " + item + " -%>", item_file)

            out_path = os.path.splitext(md_path)[0] + '.html'
            save_utf8(out_path, out)

            webbrowser.open("file://" + out_path)
        except Exception as e:
            sublime.error_message("Error in MarkdownExport package:\n\n" + str(e))
