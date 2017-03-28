#!/usr/bin/env python

import sys, os
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GTK_Main:

        # self.player = Gst.Pipeline.new("player")
        # source = Gst.ElementFactory.make("filesrc", "file-source")
        # decoder = Gst.ElementFactory.make("decodebin", "decider-bin")        
        # scale = Gst.ElementFactory.make("videoscale", "video-scaler")
        # caps = Gst.Caps.from_string("video/x-raw, width=400, height=200")
        # conv = Gst.ElementFactory.make("videoconvert", "colorspace-converter")
        # # alpha
        # box = Gst.ElementFactory.make("videobox", "video-box")
        # mixer = Gst.ElementFactory.make("videomixer", "video-mixer")
        # sink = Gst.ElementFactory.make("xvimagesink", "video-output")

        # self.player.add(source)
        # self.player.add(decoder)
        # self.player.add(scale)
        # self.player.add(conv)        
        # self.player.add(box)
        # self.player.add(mixer)        
        # self.player.add(sink)

        # source.link(decoder)
        # decoder.link(scale)
        # scale.link(conv)
        # conv.link(box)
        # box.link(mixer)
        # mixer.link(sink)    

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Videotestsrc-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)

        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)
        window.show_all()

        # self.player = Gst.Pipeline.new("player")
        # source = Gst.ElementFactory.make("videotestsrc", "video-source")
        # sink = Gst.ElementFactory.make("xvimagesink", "video-output")
        # caps = Gst.Caps.from_string("video/x-raw, width=320, height=230")
        # filter = Gst.ElementFactory.make("capsfilter", "filter")
        # filter.set_property("caps", caps)

        #gst-launch-1.0 filesrc location=speaker.MTS ! decodebin ! videoscale ! videoconvert ! videobox ! videomixer ! xvimagesink        

        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("filesrc", "file-source")
        decoder = Gst.ElementFactory.make("decodebin", "decode")  
        #decoder.connect("pad-added", self.demuxer_callback)      
        scale = Gst.ElementFactory.make("videoscale", "scale")
        #caps = Gst.Caps.from_string("video/x-raw, width=400, height=200")
        conv = Gst.ElementFactory.make("videoconvert", "convert")
        # alpha
        box = Gst.ElementFactory.make("videobox", "box")
        mixer = Gst.ElementFactory.make("videomixer", "mixer")
        sink = Gst.ElementFactory.make("xvimagesink", "output")

        # Ensure all elements were created successfully.
        if (not source or not decoder or not scale or not conv or 
            not box or not mixer or not sink):
            print ('Elements could not be linked.')
            exit(-1)        

        # self.player.add(source)
        # self.player.add(filter)
        # self.player.add(sink)

        self.player.add(source)
        self.player.add(decoder)
        self.player.add(scale)
        self.player.add(conv)        
        self.player.add(box)
        self.player.add(mixer)        
        self.player.add(sink)
        # for ele in [source, decoder, scale, audioconv, conv, box, mixer, sink]:
        #     self.player.add(ele)        

        # source.link(filter)
        # filter.link(sink)

        source.link(decoder)
        decoder.link(scale)
        scale.link(conv)
        conv.link(box)
        box.link(mixer)
        mixer.link(sink)      

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)        

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.get_by_name("file-source").set_property("location", "speaker.MTS")
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.movie_window.window.xid)

    # def demuxer_callback(self, demuxer, pad):
    #     tpl_property = pad.get_property("template")
    #     tpl_name = tpl_property.name_template
    #     print ('demuxer_callback: template name template: "%s"' % tpl_name)
    #     if tpl_name == "video_%02d":
    #         queuev_pad = self.queuev.get_pad("sink")
    #         pad.link(queuev_pad)
    #     elif tpl_name == "audio_%02d":
    #         queuea_pad = self.queuea.get_pad("sink")
    #         pad.link(queuea_pad)            

GObject.threads_init()
Gst.init(None)        
GTK_Main()
Gtk.main()