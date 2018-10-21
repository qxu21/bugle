from flask import render_template, flash, redirect, url_for, session, request, g, abort, send_static_file
from app import app#, db, lm
from .forms import InputForm
from subprocess import call
from temp import createMidiFile
from uppercase import asciiUppercase
from lowercase import asciiLowercase
import string
from random import random
from math import floor

@app.route('/', methods=['GET','POST'])
def index():
    form=InputForm()
    if form.validate_on_submit():
        s = ""
        for l in form.data.data:
            if l in string.ascii_lowercase:
                s += asciiLowercase(l)
            elif l in string.ascii_uppercase:
                s += asciiUppercase(l)
            else:
                s += l
        createMidiFile(s)
        fn = 'out_{}.mp3'.format(floor(10000*random()))
        call('timidity out.mid -Ow -o - | ffmpeg -i - -ab 128k {}'.format(fn),shell=True)
        return send_static_file(fn)
    return render_template('index.html',form=form)

@app.errorhandler(404)
def error_404(error):
    return redirect(url_for("index"))

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500