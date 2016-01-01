#!/usr/bin/python

import sys
import cStringIO
from nevow import tags as t, url
from nevow.flat import flatten
import ribbonator

from twisted.web import server, resource
from twisted.internet import reactor, endpoints

def gen_checks(b, merits):
    devices = []
    if isinstance(b, ribbonator.Asteroid):
        return '' # Not supported yet!
    for d in 'oeprgnAX': # left-hand devices
        if b.permit(d):
            v = 'checked' if d in merits else None
            devices.append(t.li[t.input(type='checkbox', name='%s_%s'%(b.name, d), checked=v), ribbonator.devices[d]])
    for c in sorted(ribbonator.craft_devices, key=lambda c:ribbonator.devices[c]): # right-hand devices
        if b.permit(c):
            v = 'checked' if c in merits else None
            devices.append(t.li[t.input(type='radio', name='%s_craft'%(b.name,), value=c, checked=v), ribbonator.devices[c]])
    for d in '?|+^':
        if b.permit(d):
            v = 'checked' if d in merits else None
            devices.append(t.li[t.input(type='checkbox', name='%s_%s'%(b.name, d), checked=v), ribbonator.devices[d]])
    if b.permit('W'):
        v = 'checked' if 'W' in merits else None
        devices.append(t.li[t.input(type='checkbox', name='%s_W'%(b.name,), checked=v), 'Challenge Wreath: ', b.wreath])
    v = 'checked' if 'soi' in merits else None
    return t.fieldset[t.legend[b.name],
                      t.input(type='checkbox', name='%s_soi'%(b.name,), checked=v), 'Reached SOI',
                      t.ul[devices],
                      ]

def gen_job(b, merits):
    return '%s=%s'%(b, ''.join(m for m in merits if len(m) == 1))

def parse_merits(kwargs):
    merits = {}
    for k,v in kwargs.items():
        v = ''.join(v)
        b,_,c = k.partition('_')
        merits.setdefault(b, [])
        if c == 'craft':
            merits[b].append(v)
        elif c:
            merits[b].append(c)
        else: # Job Card format
            merits[b].append('soi')
            merits[b].extend(v)
    return merits

def page_body(kwargs):
    merits = parse_merits(kwargs)
    checks = [gen_checks(b, merits.get(b.name, [])) for b in ribbonator.bodies]
    job = '?' + '&'.join(gen_job(b, merits[b]) for b in merits if 'soi' in merits[b])
    return [t.h1['RSS Ribbonator - Clumsy Web Interface'],
            t.p["Generator and RSS Ribbons by Edward Cree.  Based on the KSP Ribbons by Unistrut.  'Inspired' by ", t.a(href='http://www.kerbaltek.com/ribbons')["Ezriilc's Ribbon Generator"], "."],
            t.p["Select your achievements with the checkboxes and radiobuttons, and click Submit to generate the ribbon image URL.  This will also generate a Ribbonator 'job card' URL; bookmark this if you want to be able to update your ribbons later."],
            t.p["The Ribbonator does not store any user data.  Instead, the ribbon contents are encoded in the URL of the image, using the same 'job card' format."],
            t.p["Note: Asteroid ribbons are not supported yet."],
            t.img(src='gen.png'+job, alt="Generated ribbons"),
            t.p[t.a(href=job)["Job Card URL - bookmark this"]],
            t.form(method='GET')[t.ul[checks],
                                 t.input(type='submit', value='Submit')
                                 ],
            ]

def gen_image(kwargs):
    merits = parse_merits(kwargs)
    image = ribbonator.generate('%s %s'%(k, ''.join(m for m in v if len(m) == 1)) for k,v in merits.items())
    out = cStringIO.StringIO()
    image.save(out, format='png')
    return out.getvalue()

class GenImg(resource.Resource):
    isLeaf = True
    
    def render_GET(self, request):
        request.setHeader("content-type", "image/png")
        return gen_image(request.args)

class Index(resource.Resource):
    isLeaf = True
    
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        content = page_body(request.args)
        page = t.html[t.head[t.title['RSS Ribbonator']],
                      t.body[content]]
        return flatten(page)

root = resource.Resource()
root.putChild('', Index())
root.putChild('index.htm', Index())
root.putChild('gen.png', GenImg())

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(root))
    reactor.run()
