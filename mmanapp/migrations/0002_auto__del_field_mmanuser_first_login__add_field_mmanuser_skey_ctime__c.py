# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MManUser.first_login'
        db.delete_column('mmanapp_mmanuser', 'first_login')

        # Adding field 'MManUser.skey_ctime'
        db.add_column('mmanapp_mmanuser', 'skey_ctime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


        # Changing field 'MManUser.reg_time'
        db.alter_column('mmanapp_mmanuser', 'reg_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'MManUser.last_login'
        db.alter_column('mmanapp_mmanuser', 'last_login', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Adding field 'MManUser.first_login'
        db.add_column('mmanapp_mmanuser', 'first_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'MManUser.skey_ctime'
        db.delete_column('mmanapp_mmanuser', 'skey_ctime')


        # Changing field 'MManUser.reg_time'
        db.alter_column('mmanapp_mmanuser', 'reg_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'MManUser.last_login'
        db.alter_column('mmanapp_mmanuser', 'last_login', self.gf('django.db.models.fields.DateTimeField')())

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
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'reg_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'skey': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skey_ctime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'upload_pics_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['mmanapp']