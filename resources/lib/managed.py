#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module contains the classes ManagedMovies and ManagedTV,
which provide dialog windows and tools for editing managed movies and tvshow items
'''

import xbmc
import xbmcgui
import xbmcaddon

from utils import get_items

class ManagedMovies(object):
    '''
    provides windows for displaying managed movies,
    and tools for manipulating the objects and managed file
    '''
    #TODO: pass around a "previous_view" function handle

    def __init__(self, mainmenu):
        self.addon = xbmcaddon.Addon()
        self.STR_ADDON_NAME = self.addon.getAddonInfo('name')
        self.mainmenu = mainmenu

    def view_all(self):
        '''
        displays all managed movies, which are selectable and lead to options.
        also provides additional options at bottom of menu
        '''
        STR_NO_MANAGED_MOVIES = self.addon.getLocalizedString(32008)
        STR_REMOVE_ALL_MOVIES = self.addon.getLocalizedString(32009)
        STR_MOVE_ALL_BACK_TO_STAGED = self.addon.getLocalizedString(32010)
        STR_BACK = self.addon.getLocalizedString(32011)
        STR_MANAGED_MOVIES = self.addon.getLocalizedString(32012)
        managed_items = get_items('managed.pkl')
        managed_movies = [x for x in managed_items if x.get_mediatype() == 'movie']
        if not managed_movies:
            xbmcgui.Dialog().ok(self.STR_ADDON_NAME, STR_NO_MANAGED_MOVIES)
            return self.mainmenu.view()
        lines = [str(x) for x in managed_movies]
        lines, managed_movies = (list(t) for t in zip(*sorted(zip(lines, managed_movies),
                                                              key=lambda x: x[0].lower())))
        lines += [STR_REMOVE_ALL_MOVIES, STR_MOVE_ALL_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select('{0} - {1}'.format(
            self.STR_ADDON_NAME, STR_MANAGED_MOVIES), lines)
        if not ret < 0:
            if ret < len(managed_movies):   # managed item
                for i, item in enumerate(managed_movies):
                    if ret == i:
                        return self.options(item)
            elif lines[ret] == STR_REMOVE_ALL_MOVIES:
                self.remove_all()
                return self.mainmenu.view()
            elif lines[ret] == STR_MOVE_ALL_BACK_TO_STAGED:
                self.move_all_to_staged()
                return self.mainmenu.view()
            elif lines[ret] == STR_BACK:
                return self.mainmenu.view()
        else:
            return self.mainmenu.view()

    def remove_all(self):
        ''' removes all managed movies from library '''
        STR_REMOVING_ALL_MOVIES = self.addon.getLocalizedString(32013)
        STR_ALL_MOVIES_REMOVED = self.addon.getLocalizedString(32014)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_REMOVING_ALL_MOVIES)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'movie':
                pDialog.update(0, line2=item.get_title())
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_MOVIES_REMOVED))

    def move_all_to_staged(self):
        ''' removes all managed movies from library, and adds them to staged '''
        STR_MOVING_ALL_MOVIES_BACK_TO_STAGED = self.addon.getLocalizedString(32015)
        STR_ALL_MOVIES_MOVED_TO_STAGED = self.addon.getLocalizedString(32016)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_MOVING_ALL_MOVIES_BACK_TO_STAGED)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'movie':
                pDialog.update(0, line2=item.get_title())
                item.add_to_staged_file()
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_MOVIES_MOVED_TO_STAGED))

    def options(self, item):
        ''' provides options for a single managed movie in a dialog window '''
        # TODO: add rename option
        # TODO: add reload metadata option
        # TODO: move back to staging
        # TODO: change item.show_title to item.get_show_title after I've rebuilt library
        STR_REMOVE = self.addon.getLocalizedString(32017)
        STR_MOVE_BACK_TO_STAGED = self.addon.getLocalizedString(32018)
        STR_BACK = self.addon.getLocalizedString(32011)
        STR_MANAGED_MOVIE_OPTIONS = self.addon.getLocalizedString(32019)
        lines = [STR_REMOVE, STR_MOVE_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select('{0} - {1} - {2}'.format(
            self.STR_ADDON_NAME, STR_MANAGED_MOVIE_OPTIONS, item.get_title()), lines)
        if not ret < 0:
            if lines[ret] == STR_REMOVE:
                item.remove_from_library()
                return self.view_all()
            elif lines[ret] == STR_MOVE_BACK_TO_STAGED:
                item.add_to_staged_file()
                item.remove_from_library()
                return self.view_all()
            elif lines[ret] == STR_BACK:
                return self.view_all()
        else:
            return self.view_all()

class ManagedTV(object):
    '''
    provides windows for displaying managed shows and episodes,
    and tools for manipulating the objects and managed file
    '''

    def __init__(self, mainmenu):
        self.addon = xbmcaddon.Addon()
        self.STR_ADDON_NAME = self.addon.getAddonInfo('name')
        self.mainmenu = mainmenu

    def view_shows(self):
        '''
        displays all managed tvshows, which are selectable and lead to options.
        also provides additional options at bottom of menu
        '''
        STR_NO_MANAGED_TV_SHOWS = self.addon.getLocalizedString(32020)
        STR_REMOVE_ALL_TV_SHOWS = self.addon.getLocalizedString(32021)
        STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED = self.addon.getLocalizedString(32022)
        STR_BACK = self.addon.getLocalizedString(32011)
        STR_MANAGED_TV_SHOWS = self.addon.getLocalizedString(32023)
        managed_items = get_items('managed.pkl')
        managed_tvshows = [x.get_show_title() for x in managed_items \
            if x.get_mediatype() == 'tvshow']
        if not managed_tvshows:
            xbmcgui.Dialog().ok(self.STR_ADDON_NAME, STR_NO_MANAGED_TV_SHOWS)
            return self.mainmenu.view()
        managed_tvshows = sorted(list(set(managed_tvshows)), key=str.lower)
        lines = ['[B]%s[/B]' % x for x in managed_tvshows]
        lines += [STR_REMOVE_ALL_TV_SHOWS, STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select('{0} - {1}'.format(
            self.STR_ADDON_NAME, STR_MANAGED_TV_SHOWS), lines)
        if not ret < 0:
            if ret < len(managed_tvshows):
                for show_title in managed_tvshows:
                    if managed_tvshows[ret] == show_title:
                        return self.view_episodes(show_title)
            elif lines[ret] == STR_REMOVE_ALL_TV_SHOWS:
                self.remove_all()
                return self.mainmenu.view()
            elif lines[ret] == STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED:
                self.move_all_to_staged()
                return self.mainmenu.view()
            elif lines[ret] == STR_BACK:
                return self.mainmenu.view()
        else:
            return self.mainmenu.view()

    def remove_all(self):
        ''' removes all managed tvshow items from library '''
        STR_REMOVING_ALL_TV_SHOWS = self.addon.getLocalizedString(32024)
        STR_ALL_TV_SHOWS_REMOVED = self.addon.getLocalizedString(32025)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_REMOVING_ALL_TV_SHOWS)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'tvshow':
                pDialog.update(0, line2=item.get_show_title(), line3=item.get_title())
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ', line3=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_TV_SHOWS_REMOVED))

    def move_all_to_staged(self):
        ''' removes all managed tvshow items from library, and adds them to staged '''
        STR_MOVING_ALL_TV_SHOWS_BACK_TO_STAGED = self.addon.getLocalizedString(32026)
        STR_ALL_TV_SHOWS_MOVED_TO_STAGED = self.addon.getLocalizedString(32027)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_MOVING_ALL_TV_SHOWS_BACK_TO_STAGED)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'tvshow':
                pDialog.update(0, line2=item.get_show_title(), line3=item.get_title())
                item.add_to_staged_file()
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ', line3=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_TV_SHOWS_MOVED_TO_STAGED))

    def view_episodes(self, show_title):
        '''
        displays all managed episodes in the specified show,
        which are selectable and lead to options.
        also provides additional options at bottom of menu
        '''
        STR_NO_MANAGED_x_EPISODES = self.addon.getLocalizedString(32028) % show_title
        STR_REMOVE_ALL_EPISODES = self.addon.getLocalizedString(32029)
        STR_MOVE_ALL_EPISODES_BACK_TO_STAGED = self.addon.getLocalizedString(32030)
        STR_BACK = self.addon.getLocalizedString(32011)
        STR_MANAGED_x_EPISODES = self.addon.getLocalizedString(32031) % show_title
        managed_items = get_items('managed.pkl')
        managed_episodes = [x for x in managed_items \
            if x.get_mediatype() == 'tvshow' and x.get_show_title() == show_title]
        if not managed_episodes:
            xbmcgui.Dialog().ok(self.STR_ADDON_NAME, STR_NO_MANAGED_x_EPISODES)
            return self.view_shows()
        lines = [str(x) for x in managed_episodes]
        lines, managed_episodes = (list(t) for t in zip(*sorted(zip(lines, managed_episodes),
                                                                key=lambda x: x[0].lower())))
        lines += [STR_REMOVE_ALL_EPISODES, STR_MOVE_ALL_EPISODES_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select('{0} - {1}'.format(
            self.STR_ADDON_NAME, STR_MANAGED_x_EPISODES), lines)
        if not ret < 0:
            if ret < len(managed_episodes):   # managed item
                for i, item in enumerate(managed_episodes):
                    if ret == i:
                        return self.episode_options(item)
            elif lines[ret] == STR_REMOVE_ALL_EPISODES:
                self.remove_episodes(show_title)
                return self.view_shows()
            elif lines[ret] == STR_MOVE_ALL_EPISODES_BACK_TO_STAGED:
                self.move_episodes_to_staged(show_title)
                return self.view_shows()
            elif lines[ret] == STR_BACK:
                return self.view_shows()
        else:
            return self.view_shows()

    def remove_episodes(self, show_title):
        ''' removes all episodes in specified show from library '''
        STR_REMOVING_ALL_x_EPISODES = self.addon.getLocalizedString(32032) % show_title
        STR_ALL_x_EPISODES_REMOVED = self.addon.getLocalizedString(32033) % show_title
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_REMOVING_ALL_x_EPISODES)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'tvshow' and item.get_show_title() == show_title:
                pDialog.update(0, line2=item.get_title())
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_x_EPISODES_REMOVED))

    def move_episodes_to_staged(self, show_title):
        ''' removes all managed episodes in specified show from library, and adds them to staged '''
        STR_MOVING_ALL_x_EPISODES_BACK_TO_STAGED = self.addon.getLocalizedString(32034) % show_title
        STR_ALL_x_EPISODES_MOVED_TO_STAGED = self.addon.getLocalizedString(32035) % show_title
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.STR_ADDON_NAME, STR_MOVING_ALL_x_EPISODES_BACK_TO_STAGED)
        managed_items = get_items('managed.pkl')
        for item in managed_items:
            if item.get_mediatype() == 'tvshow' and item.get_show_title() == show_title:
                pDialog.update(0, line2=item.get_title())
                item.add_to_staged_file()
                item.remove_from_library()
            else:
                pDialog.update(0, line2=' ')
        pDialog.close()
        xbmc.executebuiltin(
            'Notification("{0}", "{1}")'.format(
                self.STR_ADDON_NAME, STR_ALL_x_EPISODES_MOVED_TO_STAGED))

    def episode_options(self, item):
        ''' provides options for a single managed episode in a dialog window '''
        STR_REMOVE = self.addon.getLocalizedString(32017)
        STR_MOVE_BACK_TO_STAGED = self.addon.getLocalizedString(32018)
        STR_BACK = self.addon.getLocalizedString(32011)
        STR_MANAGED_EPISODE_OPTIONS = self.addon.getLocalizedString(32036)
        lines = [STR_REMOVE, STR_MOVE_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select('{0} - {1} - {2}'.format(
            self.STR_ADDON_NAME, STR_MANAGED_EPISODE_OPTIONS, item.get_title()), lines)
        if not ret < 0:
            if lines[ret] == STR_REMOVE:
                item.remove_from_library()
                return self.view_episodes(item.get_show_title())
            elif lines[ret] == STR_MOVE_BACK_TO_STAGED:
                item.add_to_staged_file()
                item.remove_from_library()
                return self.view_episodes(item.get_show_title())
            elif lines[ret] == STR_BACK:
                return self.view_episodes(item.get_show_title())
        else:
            return self.view_episodes(item.get_show_title())