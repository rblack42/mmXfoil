# -*- coding: utf-8 -*-
"""
    sphinx_ext.tikzimage
    ~~~~~~~~~~~~~~~~~~~~

    Include TiKz diagram images in Sphinx documents

    :copyright: 2024 by Roie R. Black
    :license: BSD, see LICENSE for details
"""
from sphinx.errors import SphinxError
from sphinx.util.nodes import set_source_info
from docutils.parsers.rst import Directive
from docutils import nodes, utils
from docutils.parsers.rst import directives

import os
import shutil
import hashlib
import posixpath

BUILD_TMPDIR = os.path.join(os.getcwd(),'_build', 'tikz', 'images')
if not os.path.exists(BUILD_TMPDIR):
    os.makedirs(BUILD_TMPDIR)

class TikZImageExtError(SphinxError):
    '''custom error handler for tikzimage'''

    category = 'Tikz extension error'

    def __init__(self, msg, stderr=None, stdout=None):
        if stderr:
            msg += '\n[stderr]\n' + stderr.decode(sys_encoding, 'replace')
        if stdout:
            msg += '\n[stdout]\n' + stdout.decode(sys_encoding, 'replace')
        SphinxError.__init__(self, msg)
DOC_HEAD = r'''\documentclass[preview]{standalone}
\usepackage{tikz}
%s
'''

'''templates for tikz source file to be processed'''
DOC_BODY = r'''
\begin{document}
\tikzstyle{branch}=[fill,shape=circle,minimum size=3pt,inner sep=0pt]
\begin{tikzpicture}%s
%s
\end{tikzpicture}
\end{document}
'''

class RenderTikZImage(object):
    '''manager for processing tikz diagram into a png file'''
    
    def __init__(self, text, tikzopts, tikzlibs, builder, font_size=11):
        self.text = text
        self.tikzopts = tikzopts
        self.tikzlibs = tikzlibs
        self.builder = builder
        self.font_size = font_size
        self.imagedir = os.path.join(os.getcwd(),
        '_build','tikz','images')

    def render(self):
        '''return name of final rendered image file'''
        shasum = "%s.png" % hashlib.md5(self.text.encode('utf-8')).hexdigest()
        relfn = posixpath.join(self.builder.imgpath, 'tikz',shasum)
        outfn = os.path.join(self.builder.outdir, 
                             self.builder.imagedir, 
                             'tikz', shasum)
        print("outfn:",outfn)
        print("relfn:",relfn)
        # see if we already have generated this image
        if os.path.exists(outfn):
            return relfn, outfn

        # create temp file for running latex
        tempdir = BUILD_TMPDIR
        curpath = os.getcwd()
        os.chdir(tempdir)

        # create latex file to process
        self.wrap_text()

        # run pdflatex to build pdf file
        status = os.system('pdflatex --interaction=nonstopmode tikz')
        assert 0 == status

        # convert to png file
        status = os.system('convert -density 300 tikz.pdf -quality 90 tikz.png')

        # copy final image to image dir
        os.chdir(curpath)
        imagepath = os.path.join(os.path.abspath(self.imagedir),'tikz')
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)
        #print "Copying file to ", imagepath, outfn
        shutil.copyfile(os.path.join(tempdir, "tikz.png"), outfn)
        #shutil.rmtree(tempdir)
        return relfn, outfn

    def wrap_text(self):
        latex = DOC_HEAD % self.tikzlibs
        latex += (DOC_BODY) % (self.tikzopts, self.text)

        # write latex file
        f = open('tikz.tex','w')
        f.write(latex)
        f.close()


class tikzimage(nodes.General, nodes.Element):
    pass

class TikZImage(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'label': directives.unchanged,
        'name': directives.unchanged,
        'nowrap': directives.flag,
        'width': directives.unchanged,
        'align': directives.unchanged,
        'tikzopts': directives.unchanged,
        'tikzlibs': directives.unchanged,
    }

    def run(self):
        latex = '\n'.join(self.content)
        node = tikzimage()
        node['latex'] = latex
        node['label'] = None
        node['docname'] = self.state.document.settings.env.docname
        style = ''
        if 'width' in self.options:
            style += 'width=%s' % self.options['width']
        if 'align' in self.options:
            style += ' class="align-%s"' % self.options['align']
        node['style'] = style

        if 'tikzopts' in self.options:
            tikzopts = '[%s]' % self.options['tikzopts']
        else:
            tikzopts = ''

        node['tikzopts'] = tikzopts

        if 'tikzlibs' in self.options:
            tikzlibs = r'\usetikzlibrary{%s}' % self.options['tikzlibs']
        else:
            tikzlibs = ''
        node['tikzlibs'] = tikzlibs

        ret = [node]
        set_source_info(self,node)
        return ret

def html_visit_tikzimage(self, node):
    latex = node['latex']
    opts = node['tikzopts']
    libs = node['tikzlibs']
    try:
        imagedir = self.builder.imgpath
        fname, relfn = RenderTikZImage(latex, opts, libs, self.builder).render()
        #print "Rendered imge:", fname, relfn
    except TikZImageExtError  as exc:
        msg = unicode(str(exc), 'utf-8', 'replace')
        sm = nodes.system_message(msg, type='WARNING', level=2,
                backrefs=[], source=node['latex'])
        raise nodes.SkipNode
        sm.walkabout(self)
        self.builder.warn('display latex %r: ' % node['latex'] + str(exc))
        raise nodes.SkipNode
    if fname is None:
        # something failed -- use text-only as a bad substitute
        self.body.append('<span class="tikzimage">%s</span>' %
                         self.encode(node['latex']).strip())
    else:
         c = ('<img src="%s" %s' % (fname,node['style']))
         self.body.append( c + '/>')
    raise nodes.SkipNode

def latex_visit_tikzimage(self, node):
    self.body.append('$' + node['latex'] + '$')
    raise nodes.SkipNode

def latex_visit_displaytikzimage(self, node):
    self.body.append(node['latex'])
    raise nodes.SkipNode

def setup(app):
    app.add_node(tikzimage,
        latex=(latex_visit_tikzimage, None),
        html=(html_visit_tikzimage,None))
    app.add_directive('tikzimage', TikZImage)
