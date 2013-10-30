# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MManUser'
        db.create_table('mmanapp_mmanuser', (
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True, db_index=True)),
            ('skey', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('avatar', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('upload_pics_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reg_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('first_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('money', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('intro', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('mmanapp', ['MManUser'])

        # Adding model 'MManPic'
        db.create_table('mmanapp_mmanpic', (
            ('pic_id', self.gf('django.db.models.fields.CharField')(max_length=512, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmanapp.MManUser'], null=True, blank=True)),
            ('imagedata', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('comments_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('like_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal('mmanapp', ['MManPic'])

        # Adding model 'MManComment'
        db.create_table('mmanapp_mmancomment', (
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('avatar', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True, db_index=True)),
            ('pic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmanapp.MManPic'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=512)),
        ))
        db.send_create_signal('mmanapp', ['MManComment'])


    def backwards(self, orm):
        # Deleting model 'MManUser'
        db.delete_table('mmanapp_mmanuser')

        # Deleting model 'MManPic'
        db.delete_table('mmanapp_mmanpic')

        # Deleting model 'MManComment'
        db.delete_table('mmanapp_mmancomment')


    models = {
        'mmanapp.mmancomment': {
            'Meta': {'ordering': "['time']", 'object_name': 'MManComment'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmanapp.MManPic']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True', 'db_index': 'True'})
        },
        'mmanapp.mmanpic': {
            'Meta': {'ordering': "['pic_id', 'like_num', 'comments_num']", 'object_name': 'MManPic'},
            'comments_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'imagedata': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'like_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pic_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmanapp.MManUser']", 'null': 'True', 'blank': 'True'})
        },
        'mmanapp.mmanuser': {
            'Meta': {'object_name': 'MManUser'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'reg_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'skey': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'upload_pics_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['mmanapp']