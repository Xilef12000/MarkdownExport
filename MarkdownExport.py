import os
import sublime
import sublime_plugin
import webbrowser
import codecs
import re
from .markdown import markdown
from .markdown.extensions.tables import TableExtension

def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)

def load_utf8(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

class markdown_export_command(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            package_path = sublime.packages_path() + "/MarkdownExport/"

            settings = sublime.load_settings('MarkdownExport.sublime-settings')
            template_inuse = settings.get("template")

            md_path = self.view.window().active_view().file_name()

            if not os.path.splitext(md_path)[1] in [".md", ".MD", ".markdown", ".Markdown"]:
                sublime.error_message(md_path  + "\nis not a Markdown file\n\n")
                return 1

            html_template = load_utf8(package_path + "templates/" + settings.get("templates").get(template_inuse).get("html"))
            template_load = re.findall('<%- (.*?) -%>', html_template, re.DOTALL)
            template_insert = re.findall('<%= (.*?) =%>', html_template, re.DOTALL)

            md = self.view.substr(sublime.Region(0, self.view.size()))

            out = html_template

            if 'TITLE' in template_insert:
                out = out.replace("<%= TITLE =%>", os.path.splitext(os.path.basename(md_path))[0])
            if 'HTML' in template_insert:
                out = out.replace("<%= HTML =%>", markdown(md, extensions=[TableExtension()]))
            while not template_load == []:
                for item in template_load:
                    item_file_name = settings.get("templates").get(template_inuse).get(item)
                    item_file = load_utf8(package_path + "templates/" + item_file_name)
                    out = out.replace("<%- " + item + " -%>", item_file)
                    template_load = remove_values_from_list(template_load, item)
                    template_load.extend(re.findall('<%- (.*?) -%>', out, re.DOTALL))

            out_path = os.path.splitext(md_path)[0] + '.html'
            save_utf8(out_path, out)

            webbrowser.open("file://" + out_path)

        except Exception as e:
            sublime.error_message("Error in MarkdownExport package:\n\n" + str(e))
