import requests
import socket
import os
import subprocess
import sys
import abc


class NotSuccessException(Exception):
    pass


class UnknownHostException(Exception):
    pass


class PhantomjsCannotBeFoundException(Exception):
    pass


class ScriptCannotBeFoundException(Exception):
    pass


class ContentCrawler(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def get_source(url):
        """ abstract """


class StaticContentCrawler(object):
    @staticmethod
    def get_source(url):
        host = url.split('/')[2]
        if not _can_host_be_resolved(host):
            raise UnknownHostException('%s' % host)

        response = requests.get(url)

        if response.status_code != 200:
            raise NotSuccessException('%s - %s' % (response.status_code, url))

        return response.text


class DynamicContentCrawler:
    def __init__(self, phantomjs_bin='phantomjs'):
        if not _cmd_exists(phantomjs_bin):
            raise PhantomjsCannotBeFoundException(phantomjs_bin)

        self.phantomjs_bin = phantomjs_bin

    def get_source(self, url, script_filepath=None):
        script_filepath = self.__get_script_file_path(script_filepath)

        if not os.path.isfile(script_filepath):
            raise ScriptCannotBeFoundException(script_filepath)

        command = '%s %s %s' % (self.phantomjs_bin, script_filepath, url)

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()
        return str(out)

    def __get_script_file_path(self, script_filepath):
        if script_filepath is None:
            return "%s/resources/phantomjs_get_source.js" % os.path.dirname(os.path.realpath(__file__))

        if os.path.isabs(script_filepath):
            return script_filepath

        return self.__get_relative_script_file_path_at_child_class(script_filepath)

    def __get_relative_script_file_path_at_child_class(self, script_filepath):
        return os.path.join(os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__)), script_filepath)


def _can_host_be_resolved(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False


def _cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
