#!/usr/bin/python -u

import sys
import cStringIO
import urllib
from nevow import tags as t
from nevow.flat import flatten
import ribbonator
import optparse

from twisted.web import server, resource
from twisted.internet import reactor, endpoints

PAGE_SCRIPT = """
moon_parents = {}

function changedSOI(name)
{
    soi = document.getElementById(name + '_soi');
    div = document.getElementById(name + '_div');
    if (soi == null)
        return;
    if (div == null)
        return;
    if (soi.checked)
        div.style.display = 'block';
    else
        div.style.display = 'none';
    for (var moon in moon_parents) {
        if (moon_parents[moon] == name) {
            mfs = document.getElementById(moon + '_fs');
            if (mfs != null)
                mfs.style.display = div.style.display;
        }
    }
}

"""

for b in ribbonator.bodies:
    if isinstance(b, ribbonator.Moon):
        PAGE_SCRIPT += 'moon_parents[%r] = %r\n'%(b.name, b.parent.name)

def gen_checks(b, allmerits):
    merits = allmerits.get(b.name, [])
    groups = []
    soi_string = 'Reached SOI'
    if isinstance(b, ribbonator.Asteroid):
        soi_string = 'Visited (within 2.2km)'
        group = []
        have_mb = any(m.startswith('mb_') for m in merits)
        for mb in ribbonator.bodies:
            if isinstance(mb, (ribbonator.Star, ribbonator.Planet)):
                v = 'checked' if 'mb_' + mb.name in merits or (mb == ribbonator.earth and not have_mb) else None
                group.extend((t.input(type='radio', name='%s_mainbody'%(b.name,), value=mb.name, checked=v), mb.name))
        groups.append(t.fieldset[t.legend['MainBody'],
                                 group,
                                 ])
    lhgroup = []
    for d in 'oeprgnAX': # left-hand devices
        if b.permit(d):
            v = 'checked' if d in merits else None
            lhgroup.extend((t.input(type='checkbox', name='%s_%s'%(b.name, d), checked=v), ribbonator.devices[d]))
    groups.append(t.fieldset[t.legend['Left-Hand Devices'], lhgroup])
    rhgroup = []
    for c in sorted(ribbonator.craft_devices, key=lambda c:ribbonator.devices[c]): # right-hand devices
        if b.permit(c):
            v = 'checked' if c in merits else None
            rhgroup.extend((t.input(type='radio', name='%s_craft'%(b.name,), value=c, checked=v), ribbonator.devices[c]))
    groups.append(t.fieldset[t.legend['Right-Hand ("Craft") Devices'],
                             rhgroup,
                             t.input(type='radio', name='%s_craft'%(b.name), value=''), 'Clear',
                             ])
    other = []
    for d in '?|+^':
        if b.permit(d):
            v = 'checked' if d in merits else None
            other.extend((t.input(type='checkbox', name='%s_%s'%(b.name, d), checked=v), ribbonator.devices[d]))
    if b.permit('W'):
        v = 'checked' if 'W' in merits else None
        other.extend((t.input(type='checkbox', name='%s_W'%(b.name,), checked=v), 'Challenge Wreath: ', b.wreath))
    v = 'checked' if 'soi' in merits else None
    if isinstance(b, ribbonator.Moon):
        p = 'soi' in allmerits.get(b.parent.name, [])
    else:
        p = True;
    groups.append(t.fieldset[t.legend['Other Devices'], other])
    content = [t.legend[b.name],
               t.input(type='checkbox', name='%s_soi'%(b.name,), checked=v, onchange='changedSOI(%r)'%(b.name,), id='%s_soi'%(b.name,)), soi_string,
               t.div(id='%s_div'%(b.name,), style='display:%s;'%('block' if v else 'none',))[groups],
               ]
    return t.fieldset(id='%s_fs'%(b.name,), style='display:%s;'%('block' if p else 'none',))[content]

def gen_job(b, merits):
    if any(m.startswith('mb_') for m in merits):
        mb = [m for m in merits if m.startswith('mb_')][0][3:]
        b = '%s-%s'%(b, mb)
    return (b, ''.join(urllib.quote(m) for m in merits if len(m) == 1))

def parse_merits(kwargs):
    merits = {}
    for k,v in kwargs.items():
        k = urllib.unquote(k)
        v = urllib.unquote(''.join(v))
        b,_,c = k.partition('_')
        b,_,mb = b.partition('-')
        merits.setdefault(b, [])
        if c == 'craft':
            merits[b].append(v)
        elif c == 'mainbody':
            if v:
                merits[b].append('mb_'+v)
        elif c:
            merits[b].append(c)
        else: # Job Card format
            merits[b].append('soi')
            merits[b].extend(v)
            if mb:
                merits[b].append('mb_'+mb)
    return merits

def page_body(kwargs):
    merits = parse_merits(kwargs)
    checks = [gen_checks(b, merits) for b in ribbonator.bodies]
    job = '?' + '&'.join('='.join(gen_job(b, merits[b])) for b in merits if 'soi' in merits[b])
    print 'serving index', job
    return [t.script(type='text/javascript')[PAGE_SCRIPT],
            t.h1['RSS Ribbonator - Clumsy Web Interface'],
            t.p["Generator and RSS Ribbons by Edward Cree.  Based on the KSP Ribbons by Unistrut.  'Inspired' by ", t.a(href='http://www.kerbaltek.com/ribbons')["Ezriilc's Ribbon Generator"], "."],
            t.p[t.a(href="https://github.com/ec429/ribbonator")["Source Code"]],
            t.p["Select your achievements with the checkboxes and radiobuttons, and click Submit to generate the ribbon image URL.  This will also generate a Ribbonator 'job card' URL; bookmark this if you want to be able to update your ribbons later."],
            t.p["Moons will only appear when their parent planet's 'Reached SOI' is selected."],
            t.p["The Ribbonator does not store any user data.  Instead, the ribbon contents are encoded in the URL of the image, using the same 'job card' format."],
            t.p["I recommend against linking directly to the generated image.  Download it, then upload to some other hosting; that way your image won't break if the Ribbonator moves, dies, or has bandwidth troubles."],
            t.img(src='gen.png'+job, alt="Generated ribbons"),
            t.p[t.a(href=job)["Job Card URL - bookmark this"] if len(job) > 1 else ''],
            t.form(method='GET')[t.ul[checks],
                                 t.input(type='submit', value='Submit')
                                 ],
            ]

def gen_image(kwargs):
    merits = parse_merits(kwargs)
    job = [' '.join(gen_job(k, v)) for k,v in merits.items()]
    print 'serving gen.png', ', '.join(job)
    image = ribbonator.generate(map(urllib.unquote, job))
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
    x = optparse.OptionParser()
    x.add_option('-p', '--port', type=int, default=8080)
    opts, args = x.parse_args()
    assert not args, args
    endpoints.serverFromString(reactor, "tcp:%d"%(opts.port,)).listen(server.Site(root))
    reactor.run()
